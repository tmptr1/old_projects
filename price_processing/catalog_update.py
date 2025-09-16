'''
Обновляет справочники в БД, формирует новые
'''
import time
import datetime
import psycopg2
import os
import math
import pandas as pd
import openpyxl
import shutil
from PyQt5 import QtCore
import requests
from info_module import info_module

import logging
from logger import configure_logging


logger = logging.getLogger(__name__)
configure_logging(logger, 'logs/catalog_update.log')


MODULE_NUM = 5
InfoModule = None

host = ''
user = ''
password = ''
db_name = ''
path_to_prices = ''
path_to_catalogs = ''
path_to_exit3 = ''


class catalog_update():
    def __init__(self, cls):
        self.main_ui = cls
        global host, user, password, db_name, path_to_prices, path_to_catalogs, path_to_exit3, InfoModule
        InfoModule = info_module(cls, module_num=MODULE_NUM)
        host = self.main_ui.host
        user = self.main_ui.user
        password = self.main_ui.password
        db_name = self.main_ui.db_name
        path_to_prices = self.main_ui.Dir
        path_to_catalogs = self.main_ui.path_to_catalogs
        path_to_exit3 = self.main_ui.path_to_exit3
        self.last_update_currency = None
        self.last_update_price_report = None
        self.last_update_base_price = None
        self.last_update_mass_offers = None

        # из БД подтягивается время обновления справочников [Справочник Базовая цена] и [Справочник Предложений в опте]
        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cur:
                time_list = [[self.main_ui.timeEdit, 'base_price_update'], [self.main_ui.timeEdit_2, 'mass_offers_update']]
                for te, prm in time_list:
                    cur.execute(f"select val from app_settings where param = '{prm}'")
                    res = cur.fetchone()[0]
                    h, m = res.split()
                    te.setTime(QtCore.QTime(int(h), int(m)))
            connection.close()
        except Exception as ex:
            logger.error(f"set app_settings error:", exc_info=ex)
            InfoModule.increase_error_count()

    def start(self):
        self.act = Action(self)
        self.t = QtCore.QThread()
        self.act.moveToThread(self.t)
        self.t.started.connect(self.act.mainCycle)
        self.main_ui.StartButton_5.setEnabled(False)

        self.act.finishSignal.connect(self.t.quit)
        self.act.finishSignal.connect(self.setOnStartButton)
        self.act.finishSignal.connect(self.setModuleStatusPause)

        self.main_ui.Module_status_6.setText("Работает")
        self.main_ui.Module_status_6.setStyleSheet(f"color: green;")
        self.t.start()
        self.t.quit()

    def create_base_price_report(self):
        self.act2 = Action(self)
        self.t2 = QtCore.QThread()
        self.act2.moveToThread(self.t2)
        self.t2.started.connect(self.act2.update_base_price)
        self.main_ui.base_price_button.setEnabled(False)
        self.act2.reportFinishSignal.connect(lambda _: self.main_ui.base_price_button.setEnabled(True))

        self.t2.start()
        self.t2.quit()

    def create_mass_offers_report(self):
        self.act3 = Action(self)
        self.t3 = QtCore.QThread()
        self.act3.moveToThread(self.t3)
        self.t3.started.connect(self.act3.update_mass_offers)
        self.main_ui.mass_offers_button.setEnabled(False)
        self.act3.reportFinishSignal.connect(lambda _: self.main_ui.mass_offers_button.setEnabled(True))

        self.t3.start()
        self.t3.quit()

    def setModuleStatusPause(self):
        self.main_ui.Module_status_6.setText("Пауза")
        self.main_ui.Module_status_6.setStyleSheet(f"color: red;")

    def setOnStartButton(self):
        self.main_ui.StartButton_5.setEnabled(True)

    def save_time(self):
        '''Сохранение в БД времени обновлений справочников [Справочник Базовая цена] и [Справочник Предложений в опте]'''
        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cur:
                t1 = self.main_ui.timeEdit.time()
                cur.execute(f"update app_settings set val = '{t1.hour()} {t1.minute()}' where param = 'base_price_update'")
                t2 = self.main_ui.timeEdit_2.time()
                cur.execute(f"update app_settings set val = '{t2.hour()} {t2.minute()}' where param = 'mass_offers_update'")
            connection.commit()
            connection.close()
        except Exception as ex:
            logger.error(f"update app_settings error:", exc_info=ex)
            InfoModule.increase_error_count()

class Action(QtCore.QThread):
    '''Класс для многопоточной работы в PyQt'''
    startSignal = QtCore.pyqtSignal(int)
    finishSignal = QtCore.pyqtSignal(int)
    reportFinishSignal = QtCore.pyqtSignal(int)
    def __init__(self, mainApp=None):
        super(Action, self).__init__()
        self.mainApp = mainApp

    def mainCycle(self):
        '''Основной цикл, обновляет информация из справочников в БД'''
        wait_sec = 60
        # if os.path.getsize('logs/catalog_update.log') / 1048576 > 20:
        #     os.rename('logs/catalog_update.log', 'logs/catalog_update.log.1')

        while True:
            now1 = datetime.datetime.now()
            try:
                if self.mainApp.main_ui.Pause_5.isChecked():
                    self.mainApp.main_ui.Pause_5.setChecked(False)
                    self.finishSignal.emit(1)
                    return
                InfoModule.set_update_time(MODULE_NUM, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # проверка курса валют
                try:
                    self.mainApp.last_update_currency = update_currency(self.mainApp.last_update_currency)
                except Exception as currency_error:
                    logger.error("currency error:", exc_info=currency_error)
                    InfoModule.increase_error_count()

                try:
                    self.mainApp.last_update_price_report = update_price_report(self.mainApp.last_update_price_report)
                except Exception as currency_error:
                    logger.error("create price report error:", exc_info=currency_error)
                    InfoModule.increase_error_count()

                path = fr"{path_to_catalogs}\Настройки прайса поставщика.xlsx"
                cols = ["Издержки", "Код поставщика", "Можем купить?", "Работаем", "Почта", "Условие имени файла", "Срок обновление не более",
                        "Имя файла", "Прайс оптовый", "Цену считать базовой", "В прайс", "Краткое наименование", "Закупка для оборотных средств",
                        "Разрешения ПП", "Лот поставщика", "К.Превышения базовой цены", "Лот удобный нам", "Обрабатываем",
                        "Стандартизируем", "Код прайса", "Сохраняем", "Наценка мин", "Наценка опт", "Наценка макс", "% Отгрузки", "Отсрочка",
                        "Наценка для ОС", "Допустимый процент изменения количества строк", "Допустимый процент изменения цены", "Рейтинг поставщика"]
                table_name = 'Настройки_прайса_поставщика'
                dgt_cols = (0, 6, 10, 11, 14, 15, 16, 21, 22, 23, 24, 25, 26, 27, 28, 29)
                char_limits = [0, 10, 20, 20, 256, 20, 0, 256, 20, 20, 0, 20, 20, 1000, 0, 0, 0, 20, 20, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                update_catalog(path, cols, table_name, dgt_cols, char_limits)

                path = fr"{path_to_catalogs}\Справочник расположения столбцов и условий.xlsx"
                cols = ["Прайс", "Пропуск сверху", "Пропуск снизу", "Сопоставление по", "R/C КлючП", "Название КлючП",
                        "R/C АртикулП", "Название АртикулП", "R/C БрендП", "Название БрендП", "R/C НаименованиеП",
                        "Название НаименованиеП", "R/C КоличествоП", "Название КоличествоП", "R/C ЦенаП", "Название ЦенаП",
                        "R/C КратностьП", "Название КратностьП", "Строка ПримечаниеП", "R/C ПримечаниеП", "R/C Валюта", "Название Валюта"]
                table_name = 'file_settings'
                dgt_cols = (1,2)
                char_limits = [20, 0, 0, 100, 50, 256, 50, 256, 50, 256, 50, 256, 50, 256, 50, 256, 50, 256, 50, 256, 50, 256]
                spc_cols = """(Прайс, Пропуск_сверху, Пропуск_снизу, Сопоставление_по, rc_КлючП, Название_КлючП, 
                    rc_АртикулП, Название_АртикулП, rc_БрендП, Название_БрендП, rc_НаименованиеП, Название_НаименованиеП, 
                    rc_КоличествоП, Название_КоличествоП, rc_ЦенаП, Название_ЦенаП, rc_КратностьП, Название_КратностьП, 
                    rc_ПримечаниеП, Название_ПримечаниеП, rc_Валюта, Название_Валюта)"""
                update_catalog(path, cols, table_name, dgt_cols, char_limits, special_cols=spc_cols)
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    rc_cols = [['Строка_КлючП', 'Столбец_КлючП', 'rc_КлючП'],
                               ['Строка_АртикулП', 'Столбец_АртикулП', 'rc_АртикулП'],
                               ['Строка_БрендП', 'Столбец_БрендП', 'rc_БрендП'],
                               ['Строка_НаименованиеП', 'Столбец_НаименованиеП', 'rc_НаименованиеП'],
                               ['Строка_КоличествоП', 'Столбец_КоличествоП', 'rc_КоличествоП'],
                               ['Строка_ЦенаП', 'Столбец_ЦенаП', 'rc_ЦенаП'],
                               ['Строка_КратностьП', 'Столбец_КратностьП', 'rc_КратностьП'],
                               ['Строка_ПримечаниеП', 'Столбец_ПримечаниеП', 'rc_ПримечаниеП'],
                               ['Строка_Валюта', 'Столбец_Валюта', 'rc_Валюта'],
                               ]
                    for r, c, rc in rc_cols:
                        cur.execute(f"update file_settings set {r} = (regexp_split_to_array({rc}, '[RC]'))[2]::INTEGER, "
                                    f"{c} = (regexp_split_to_array({rc}, '[RC]'))[3]::INTEGER where {rc} is not NULL;")
                connection.commit()
                connection.close()

                path = fr"{path_to_catalogs}\Справочник слов исключений.xlsx"
                cols = ["Код прайса", "Условие", "Столбец поиска", "Текст"]
                table_name = 'Справочник_слов_исключений'
                dgt_cols = set()
                char_limits = [10, 30, 50, 500]
                update_catalog(path, cols, table_name, dgt_cols, char_limits)

                path = fr"{path_to_catalogs}\Справочник проблемных товаров.xlsx"
                cols = ["Код прайса", "Артикул", "Бренд", "Разрешение покупателю"]
                table_name = 'Справочник_проблемных_товаров'
                dgt_cols = set()
                char_limits = [10, 256, 256, 1000]
                update_catalog(path, cols, table_name, dgt_cols, char_limits)

                path = fr"{path_to_catalogs}\Настройки прайса покупателя.xlsx"
                cols = ["Наименование", "Код покупателя", "Имя прайса", "Код прайса покупателя", "Включен?", "Уровень сервиса не ниже",
                        "Сайт", "Адрес для прайсов", "Итоговая наценка", "Короткое наименование", "Отсрочка дней", "КБ цены",
                        "Продаём для К.ОС", "Наценка для К.ОС", "Ограничение строк", "Ограничение размера", "Время рассылки прайса"]
                table_name = 'Настройки_прайса_покупателя'
                dgt_cols = (5, 8, 10, 11, 13, 14, 15)
                char_limits = [256, 20, 256, 20, 20, 0, 500, 500, 0, 10, 0, 0, 10, 0, 0, 0, 500]
                update_catalog(path, cols, table_name, dgt_cols, char_limits)

                path = fr"{path_to_catalogs}\Разрешения бренд & прайс в прайс.xlsx"
                cols = ["Код прайса", "Бренд", "Наценка ПБ", "Код ПБ_П"]
                table_name = 'Разрешения_бпп'
                dgt_cols = (2, )
                char_limits = [20, 256, 0, 1000]
                update_catalog(path, cols, table_name, dgt_cols, char_limits)

                path = fr"{path_to_catalogs}\Резерв.xlsx"
                cols = ["Код прайса", "Наш Бренд", "Артикул наш", "ШтР"]
                table_name = 'Резерв'
                dgt_cols = (3, )
                char_limits = [20, 256, 256, 0]
                update_catalog(path, cols, table_name, dgt_cols, char_limits, special_cols='(Код_прайса, Наш_Бренд, Артикул_наш, ШтР)')
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    cur.execute("update Резерв set Артикул_сравнение = upper(regexp_replace(Артикул_наш, '\W|_', '', 'g'))")
                connection.commit()
                connection.close()

                path = fr"{path_to_catalogs}\Справочник Бренды покупателя.xlsx"
                cols = ["Правильный Бренд", "Покупатель", "Бренд покупателя"]
                table_name = 'Справочник_Бренды_покупателя'
                dgt_cols = set()
                char_limits = [256, 256, 256]
                if update_catalog(path, cols, table_name, dgt_cols, char_limits):
                    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                    with connection.cursor() as cur:
                        cur.execute("update Справочник_Бренды_покупателя set Правильный_Бренд = upper(Правильный_Бренд)")
                    connection.commit()
                    connection.close()

                path = fr"{path_to_catalogs}\Справочник товаров поставщиков.xlsx"
                table_name = 'Справочник_товаров_поставщиков'
                cols = ["Прайс", "Ключ1", "АртикулПоставщика", "ПроизводительПоставщика", "НаименованиеПоставщика",
                        "Производитель",
                        "Артикул", "Наименование", "ЦенаПоставщика", "ЗапретПродажи", "ТоварныйВид", "УбратьШтуки",
                        "КратностьПоставщика"]
                dgt_cols = [8, 9, 10]
                char_limits = [50, 256, 256, 256, 256, 256, 256, 256, 0, 0, 0, 50, 50]
                update_catalog(path, cols, table_name, dgt_cols, char_limits)
                # update_supplier_product_catalog(path, table_name)
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    cur.execute("update Справочник_товаров_поставщиков set ПроизводительПоставщика = upper(ПроизводительПоставщика), "
                                "Производитель = upper(Производитель)")
                connection.commit()
                connection.close()

                brand_tables = [[fr"{path_to_catalogs}\Справочник Бренды.xlsx", 'correct_brands', ["Сюда правильное", "Можно использовать краткое наименование"]], #(0, )
                                [fr"{path_to_catalogs}\Справочник не правильные Бренды.xlsx", 'incorrect_brands', ["Правильный Бренд", "Некорретное наименование Бренда"]]] #(0, 1)

                for path, table_name, cols in brand_tables:
                    update_brand_catalog(path, table_name, cols)

                # self.mainApp.last_update_base_price = self.update_base_price(self.mainApp.last_update_base_price)
                # self.mainApp.last_update_mass_offers = self.update_mass_offers(self.mainApp.last_update_mass_offers)

                self.update_base_price(without_time_check=False)
                self.update_mass_offers(without_time_check=False)

                # Удаление неактуальных прайсов
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    cur.execute("delete from total where total.Код_поставщика not in (select Код_прайса from "
                                "Настройки_прайса_поставщика where Работаем = 'ДА')")
                connection.commit()
                connection.close()

                # проверка на паузу
                now2 = datetime.datetime.now()
                if wait_sec > (now2 - now1).seconds:
                    for _ in range(wait_sec - (now2 - now1).seconds):
                        if self.mainApp.main_ui.Pause_5.isChecked():
                            self.mainApp.main_ui.Pause_5.setChecked(False)
                            self.finishSignal.emit(1)
                            return
                        time.sleep(1)

            except Exception as ex:
                logger.error("mainCycle error:", exc_info=ex)
                InfoModule.increase_error_count()
                time.sleep(5)

    def update_base_price(self, without_time_check=True):
        '''Формирование справочника [Справочник Базовая цена]'''
        report_parts_count = 4
        try:
            if not self.mainApp.last_update_base_price:
                self.mainApp.last_update_base_price = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

            if self.mainApp.last_update_base_price < (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S") or without_time_check:
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    now = datetime.datetime.now()
                    cur.execute(f"select val from app_settings where param = 'base_price_update'")
                    res = cur.fetchone()[0]
                    h, m = res.split()
                    self.mainApp.last_update_base_price = (datetime.datetime(year=now.year, month=now.month, day=now.day, hour=int(h),
                                                                             minute=int(m)) + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

                    logger.info(f"Обновление Справочник Базовая цена ...")

                    cur.execute("delete from base_price")
                    cur.execute(f"ALTER SEQUENCE base_price_id_seq restart 1")

                    # cur.execute(
                    #     f"insert into base_price (Артикул, Бренд, ЦенаБ) select UPPER(total.Артикул), UPPER(total.Бренд), (max(Цена)-min(Цена))/2 + min(Цена) "
                    #     f"from total, Настройки_прайса_поставщика where total.Код_поставщика = Код_прайса and "
                    #     f"Цену_считать_базовой = 'ДА' group by Артикул, Бренд")
                    cur.execute(f"""insert into base_price (Артикул, Бренд, ЦенаБ, ЦенаМинПоставщик) select UPPER(total.Артикул), 
                        UPPER(total.Бренд), total.Цена, Настройки_прайса_поставщика.Код_поставщика from total, Настройки_прайса_поставщика where 
                        total.Код_поставщика = Код_прайса and Цену_считать_базовой = 'ДА' and Бренд is not NULL""")
                    cur.execute(f"""with min_supl_T as (with min_price_T as (select Артикул, Бренд, min(ЦенаБ) as min_price 
                        from base_price group by Артикул, Бренд having count(*) > 1) select base_price.Артикул as min_art, 
                        base_price.Бренд as min_brand, ЦенаМинПоставщик as min_supl from base_price, min_price_T 
                        where base_price.Артикул = min_price_T.Артикул and base_price.Бренд = min_price_T.Бренд and 
                        base_price.ЦенаБ = min_price_T.min_price) update base_price set ЦенаМинПоставщик = min_supl from min_supl_T 
                        where Артикул = min_art and Бренд = min_brand""")
                    cur.execute(f"""with avg_price as (select Артикул, Бренд, avg(ЦенаБ) as avg_ЦенаБ, min(ЦенаБ) as min_ЦенаБ 
                        from base_price group by Артикул, Бренд) update base_price set ЦенаБ = avg_price.avg_ЦенаБ, 
                        ЦенаМин = avg_price.min_ЦенаБ from avg_price where base_price.Артикул = avg_price.Артикул 
                        and base_price.Бренд = avg_price.Бренд""")
                    cur.execute(f"""with max_id_dupl as (select max(id) as max_id from base_price group by Артикул, Бренд) 
                        update base_price set duple = False where id in (select max_id from max_id_dupl)""")
                    cur.execute(f"delete from base_price where duple = True")


                    # cur.execute(f"delete from base_price where Бренд is NULL")
                connection.commit()
                connection.close()

                # Удаление старых данных
                delete_files_from_dir(fr"{path_to_catalogs}/pre Справочник Базовая цена")

                create_csv_catalog(path_to_catalogs + "/pre Справочник Базовая цена/Базовая цена - страница {}.csv",
                                   """SELECT base_price.Артикул as "Артикул", base_price.Бренд as "Бренд", 
                                        base_price.ЦенаБ as "ЦенаБ", base_price.ЦенаМин as "Мин. Цена", ЦенаМинПоставщик 
                                        as "Мин. Поставщик" FROM base_price ORDER BY Бренд OFFSET {} LIMIT {}""",
                                   host, user, password, db_name, report_parts_count)

                for i in range(1, report_parts_count + 1):
                    shutil.copy(path_to_catalogs + "/pre Справочник Базовая цена/Базовая цена - страница {}.csv".format(i),
                                path_to_catalogs + "/Справочник Базовая цена/Базовая цена - страница {}.csv".format(i))
                logger.info(f"Справочник Базовая цена обновлён")

            # return t
        except Exception as ex:
            logger.error(f"update_base_price error:", exc_info=ex)
            InfoModule.increase_error_count()
        finally:
            self.reportFinishSignal.emit(1)

    def update_mass_offers(self, without_time_check=True):
        '''Формирование справочника [Справочник Предложений в опте]'''
        report_parts_count = 4
        try:
            if not self.mainApp.last_update_mass_offers:
                self.mainApp.last_update_mass_offers = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

            if self.mainApp.last_update_mass_offers < (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S") or without_time_check:
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    now = datetime.datetime.now()
                    cur.execute(f"select val from app_settings where param = 'mass_offers_update'")
                    res = cur.fetchone()[0]
                    h, m = res.split()
                    self.mainApp.last_update_mass_offers = (datetime.datetime(year=now.year, month=now.month, day=now.day, hour=int(h),
                                           minute=int(m)) + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

                    logger.info(f"Обновление Справочник Предложений в опте ...")

                    cur.execute("delete from mass_offers")
                    cur.execute(f"ALTER SEQUENCE mass_offers_id_seq restart 1")

                    cur.execute(f"""insert into mass_offers (Артикул, Бренд, Код_прайса) select UPPER(Артикул), UPPER(Бренд), 
                            Код_прайса from total, Настройки_прайса_поставщика where total.Код_поставщика = Код_прайса and 
                            Прайс_оптовый = 'ДА' and Бренд is not NULL""")
                    # Замена 1MIK, 2MIK на MIK
                    cur.execute(f"""update mass_offers set Код_прайса = Код_поставщика from Настройки_прайса_поставщика 
                            where mass_offers.Код_прайса = Настройки_прайса_поставщика.Код_прайса""")
                    # Удаление дублей в разрезе MIK
                    cur.execute(f"update mass_offers set duple = False where id in (select max(id) from mass_offers group by Артикул, Бренд, Код_прайса)")
                    cur.execute(f"delete from mass_offers where duple = True")
                    cur.execute(f"update mass_offers set duple = True")
                    # Предложений_в_опте
                    cur.execute(f"""with cnt_price as (select Артикул, Бренд, count(*) as cnt from mass_offers group by 
                            Артикул, Бренд) update mass_offers set Предложений_в_опте = cnt_price.cnt from cnt_price where 
                            mass_offers.Артикул = cnt_price.Артикул and mass_offers.Бренд = cnt_price.Бренд""")
                    # Удаление дублей (Артикул, Бренд)
                    cur.execute(f"update mass_offers set duple = False where id in (select max(id) from mass_offers group by Артикул, Бренд)")
                    cur.execute(f"delete from mass_offers where duple = True")
                    cur.execute(f"delete from mass_offers where Предложений_в_опте <= 1 or Предложений_в_опте is NULL")

                    # cur.execute(
                    #     f"insert into mass_offers (Артикул, Бренд, Код_прайса) select UPPER(Артикул), UPPER(Бренд), Код_прайса "
                    #     f"from total, Настройки_прайса_поставщика where total.Код_поставщика = Код_прайса and Прайс_оптовый = 'ДА' "
                    #     f"and Бренд is not NULL")
                    #
                    # # Заменить 1MIK, 2MIK на MIK
                    # cur.execute("update mass_offers set Код_прайса = Код_поставщика from Настройки_прайса_поставщика "
                    #             "where mass_offers.Код_прайса = Настройки_прайса_поставщика.Код_прайса")
                    #
                    # # удаление повторений внутри прайсов поставщиков
                    # cur.execute("delete from mass_offers where id in (select id from mass_offers except select min(id) "
                    #             "from mass_offers group by Артикул, Бренд, Код_прайса)")
                    #
                    # cur.execute(
                    #     "update mass_offers set Предложений_в_опте = T.cn from (select Артикул, Бренд, min(id) as minId, "
                    #     "count(*) as cn from mass_offers group by Артикул, Бренд having count(*) > 1) as T where "
                    #     "mass_offers.Артикул = T.Артикул and mass_offers.Бренд = T.Бренд")
                    # cur.execute("delete from mass_offers where Предложений_в_опте <= 1 or Предложений_в_опте is NULL")
                    #
                    # cur.execute("delete from mass_offers where id in "
                    #             "(select id from mass_offers except select min(id) from mass_offers group by Артикул, Бренд)")
                connection.commit()
                connection.close()

                # Удаление старых данных
                delete_files_from_dir(fr"{path_to_catalogs}/pre Справочник Предложений в опте")

                create_csv_catalog(path_to_catalogs + "/pre Справочник Предложений в опте/Предложений в опте - страница {}.csv",
                                   """SELECT mass_offers.Артикул as "Артикул", mass_offers.Бренд as "Бренд",
                                             mass_offers.Предложений_в_опте as "Предложений в опте"
                                             FROM mass_offers ORDER BY id OFFSET {} LIMIT {}""",
                                   host, user, password, db_name, report_parts_count)

                for i in range(1, report_parts_count + 1):
                    shutil.copy(path_to_catalogs + "/pre Справочник Предложений в опте/Предложений в опте - страница {}.csv".format(i),
                                path_to_catalogs + "/Справочник Предложений в опте/Предложений в опте - страница {}.csv".format(i))

                logger.info(f"Справочник Предложений в опте обновлён")

            # return t
        except Exception as ex:
            logger.error(f"update_mass_offers error:", exc_info=ex)
            InfoModule.increase_error_count()
        finally:
            self.reportFinishSignal.emit(1)


def create_csv_catalog(csv_file, req, host, user, password, db_name, report_parts_count):
    df = pd.DataFrame(
        columns=["Ключ1 поставщика", "Артикул поставщика", "Производитель поставщика", "Наименование поставщика",
                 "Количество поставщика", "Цена поставщика", "Кратность поставщика", "Примечание поставщика",
                 "01Артикул",
                 "03Наименование", "05Цена", "06Кратность-", "07Код поставщика", "09Код + Поставщик + Товар",
                 "10Оригинал",
                 "13Градация", "14Производитель заполнен", "15КодТутОптТорг", "17КодУникальности",
                 "18КороткоеНаименование",
                 "19МинЦенаПоПрайсу", "20ИслючитьИзПрайса", "Отсрочка", "Продаём для ОС", "Наценка для ОС", "Наценка Р",
                 "Наценка ПБ", "Мин наценка", "Шаг градаци", "Шаг опт", "Разрешения ПП", "УбратьЗП", "Предложений опт",
                 "ЦенаБ", "Кол-во", "Код ПБ_П", "06Кратность", "Кратность меньше", "05Цена+", "Количество закупок",
                 "% Отгрузки"])

    for i in range(1, report_parts_count + 1):
        df.to_csv(csv_file.format(i), sep=';', decimal=',', encoding="windows-1251", index=False, errors='ignore')

    limit = 1_048_500

    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    sheet_num = 1
    # loaded = limit
    loaded = 0

    while True:
        df = pd.read_sql(req.format(loaded, limit), connection)
        if not len(df):
            break

        df.to_csv(csv_file.format(sheet_num), mode='w', sep=';', encoding="windows-1251",
                  index=False, header=True, errors='ignore')
        loaded += limit
        sheet_num += 1
    connection.close()

def update_currency(t):
    '''Обновление курса валют с сайта ЦБ'''
    if not t:
        t = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d-%b-%Y")

    if t < (datetime.datetime.now()).strftime("%d-%b-%Y"):
        t = (datetime.datetime.now()).strftime("%d-%b-%Y")
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            cur.execute(f"DELETE FROM exchange_rate")
            data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

            for i in data['Valute']:
                cur.execute(f"insert into exchange_rate values('{data['Valute'][i]['CharCode']}', {data['Valute'][i]['Value'] / data['Valute'][i]['Nominal']})")
            logger.info("Курс валюты обновлён")

        connection.commit()
        connection.close()
    return t

def update_price_report(t):
    '''Обновление отчёта о прайсах'''
    if not t:
        t = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d-%b-%Y")

    if t < (datetime.datetime.now()).strftime("%d-%b-%Y"):
        t = (datetime.datetime.now()).strftime("%d-%b-%Y")
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            df = pd.read_sql(
                """SELECT code as "Прайс", exit1 as "Первый этап обработки", exit2 as "Второй этап обработки", 
                loaded_rows as "Загружено", unloaded_rows as "Не загружено", 
                round(loaded_rows/round(loaded_rows+unloaded_rows, 2)*100, 2) as "Процент пройденных позиций" FROM price_report""",
                connection)
            df.to_csv(f"{path_to_catalogs}/Отчёт.csv", sep=';', encoding='windows-1251', index=False, errors='ignore')
            logger.info("Отчёт сформирован")
        connection.commit()
        connection.close()
    return t

def update_catalog(path, cols, table_name, dgt_cols, char_limits, special_cols=''):
    '''Перенос информации из справочников в БД'''
    try:
        t = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
        file_name = '.'.join(path.split('\\')[-1].split('.')[:-1])

        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            cur.execute(f"select Время_изменения from Время_изменений_справочники where Название_файла = '{file_name}'")
            res = cur.fetchone()

            add = False
            if res:
                if res[0] != t:
                    add = True
            else:
                add = True

            if not add:
                return False

            logger.info(f"Обновление {file_name} ...")
            cur.execute(f"delete from Время_изменений_справочники where Название_файла = '{file_name}'")
            cur.execute(f"delete from {table_name}")

            header = pd.read_excel(path, sheet_name=0, header=0, nrows=1)
            cols_num = {}
            for i, c in enumerate(header.columns):
                if c in cols:
                    cols_num[i] = c
            # print(header)
            # print(cols_num)
            sr = 1
            rows_limit = 50000
            while True:
                table = pd.read_excel(path, header=None, nrows=rows_limit, skiprows=sr, usecols=cols_num.keys(), sheet_name=0)
                table_size = len(table)
                if not table_size:
                    break
                # print(sr)
                # r += table_size
                # sr = range(1, r+1)
                sr += table_size
                table = table.rename(columns=cols_num)
                table = table.reindex(columns=cols)
                pool_req = f"insert into {table_name}{special_cols} values"
                for v_id, i in enumerate(table.values):
                    pool_req += f"({create_req(i, dgt_cols, char_limits)}), "
                    # отправка 500 объединённых запросов к БД за один раз
                    # try:
                    if (v_id % 500 == 0 or v_id == table_size - 1) and v_id >= 0:
                        try:
                            pool_req = pool_req[:-2]
                            pool_req += " ON CONFLICT DO NOTHING;"
                            # if file_name == "Настройки прайса поставщика":
                            # print(pool_req)
                            cur.execute(pool_req)
                        except Exception as ex1:
                            logger.error("insert error:", exc_info=ex1)
                            InfoModule.increase_error_count()
                        # finally:
                        pool_req = f"insert into {table_name}{special_cols} values"
                    # except Exception
            cur.execute(f"insert into Время_изменений_справочники values('{file_name}', '{t}')")
            logger.info(f"{file_name} обновлён")

        connection.commit()
        connection.close()
        return True
    except Exception as ex:
        logger.error(f"update_catalog error:", exc_info=ex)
        InfoModule.increase_error_count()


def fix_str(s):
    '''Изменение строки для её корректной записи в БД'''
    x1 = '\''
    x2 = '\'\''
    x3 = ";"
    return f"'{str(s).replace(x1, x2).replace(x3, ' ')}'"

def create_req(i, dgt_cols, char_limits):
    '''Обрабатывает значение в корректный для БД вид'''
    req = ''
    for id, r in enumerate(i):
        if id in dgt_cols:
            if not isinstance(r, str) and math.isnan(r):
                req += f"0, "

            elif isinstance(r, str):
                r = r.replace(',', '.')
                correct_num = ''
                for chr in r:
                    if chr.isdigit() or chr == '.':
                        correct_num += chr

                if len(correct_num) == 0:
                    r = '0'
                else:
                    r = correct_num
                req += f"{r}, "
            else:
                req += f"{r}, "
        elif isinstance(r, str):
            r = r.replace('\'', '\'\'').replace(";", " ")
            req += f"'{r[:char_limits[id]]}', "  # [:char_limit]
        elif not isinstance(r, str):
            if math.isnan(r):
                req += 'NULL, '
            else:
                req += f"'{str(r)[:char_limits[id]]}', "  # [:char_limit]
        else:
            req += 'NULL, '
    req = req[:-2]
    return req

# def update_supplier_product_catalog(path, table_name):
#     '''Обновляет данные о справочнике [Справочник товаров поставщиков] в БД'''
#     try:
#         t = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
#         file_name = '.'.join(path.split('\\')[-1].split('.')[:-1])
#
#         connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
#         with connection.cursor() as cur:
#             cur.execute(f"select Время_изменения from Время_изменений_справочники where Название_файла = '{file_name}'")
#             res = cur.fetchone()
#
#             add = False
#             if res:
#                 if res[0] != t:
#                     add = True
#             else:
#                 add = True
#
#             if not add:
#                 return
#
#             logger.info(f"Обновление {file_name} ...")
#
#             r = 0
#             sr = r
#             rows_limit = 100000
#             cols = ["Прайс", "Ключ1", "АртикулПоставщика", "ПроизводительПоставщика", "НаименованиеПоставщика", "Производитель",
#                     "Артикул", "Наименование", "ЦенаПоставщика", "ЗапретПродажи", "ТоварныйВид", "УбратьШтуки", "КратностьПоставщика"]
#             str_cols = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10]
#             dgtl_cols = [8, 11, 12]# [8, 12, 14]
#             brand_cols = [3, 5]
#
#             cur.execute(f"delete from Время_изменений_справочники where Название_файла = '{file_name}'")
#             cur.execute(f"delete from {table_name}")
#
#             while True:
#                 table = pd.read_excel(path, header=0, nrows=rows_limit, skiprows=sr, usecols=cols, sheet_name=0)
#                 table_size = len(table)
#                 if not table_size:
#                     break
#                 r += table_size
#                 sr = range(1, r + 1)
#                 table = table.reindex(columns=cols)
#                 pool_req = f"insert into {table_name}(Прайс, Ключ1, АртикулПоставщика, ПроизводительПоставщика, НаименованиеПоставщика, " \
#                                     f"Производитель, Артикул, Наименование, ЦенаПоставщика, Запрет_продажи, Товарный_вид, УбратьШтуки, " \
#                                     f"КратностьПоставщика) values"
#                 # Обрабатывает значение в корректный для БД вид
#                 for v_id, content in enumerate(table.values):
#                     req = ''
#                     for id, i in enumerate(content):
#                         if id in str_cols:
#                             if isinstance(i, str):
#                                 i = i.replace('\'', '\'\'').replace(";", " ")
#                                 if id in brand_cols:
#                                     i = i.upper()
#                                 req += f"'{i}', "
#                             elif not isinstance(i, str):
#                                 if math.isnan(i):
#                                     req += 'NULL, '
#                                 else:
#                                     i = str(i).upper()
#                                     req += f"'{i}', "
#                             else:
#                                 req += 'NULL, '
#
#                         elif id in dgtl_cols:
#                             if not isinstance(i, str) and math.isnan(i):
#                                 req += f"NULL, "
#                             elif isinstance(i, str):
#                                 i = i.replace(',', '.')
#                                 correct_num = ''
#                                 for chr in i:
#                                     if chr.isdigit() or chr == '.':
#                                         correct_num += chr
#
#                                 if len(correct_num) == 0:
#                                     i = 'NULL'
#                                 else:
#                                     i = correct_num
#                                 req += f"{i}, "
#                             else:
#                                 req += f"{i}, "
#                     req = req[:-2]
#                     pool_req += f"({req}), "
#
#                     # отправка 500 объединённых запросов к БД за один раз
#                     if (v_id % 500 == 0 or v_id == table_size - 1) and v_id > 0:
#                         try:
#                             pool_req = pool_req[:-2]
#                             pool_req += "ON CONFLICT DO NOTHING;"
#                             cur.execute(pool_req)
#
#                             pool_req = f"insert into {table_name}(Прайс, Ключ1, АртикулПоставщика, ПроизводительПоставщика, НаименованиеПоставщика, " \
#                                        f"Производитель, Артикул, Наименование, ЦенаПоставщика, Запрет_продажи, Товарный_вид, УбратьШтуки, " \
#                                        f"КратностьПоставщика) values"
#                         except Exception as ex1:
#                             logger.error("insert2 error:", exc_info=ex1)
#                             InfoModule.increase_error_count()
#
#             cur.execute(f"insert into Время_изменений_справочники values('{file_name}', '{t}')")
#             logger.info(f"{file_name} обновлён")
#         connection.commit()
#         connection.close()
#     except Exception as ex:
#         logger.error("update_supplier_product_catalog error:", exc_info=ex)
#         InfoModule.increase_error_count()

def delete_files_from_dir(dir):
    for file in os.listdir(dir):
        os.remove(fr"{dir}/{file}")


def update_brand_catalog(path, table_name, cols):
    '''Обновление данных о справочниках с правильными/неправильными Брендами'''
    try:
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            t = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
            file_name = '.'.join(path.split('\\')[-1].split('.')[:-1])
            cur.execute(f"select Время_изменения from Время_изменений_справочники where Название_файла = '{file_name}'")
            res = cur.fetchone()

            add = False
            if res:
                if res[0] != t:
                    add = True
            else:
                add = True

            if not add:
                return

            logger.info(f"Обновление {file_name} ...")
            cur.execute(f"delete from Время_изменений_справочники where Название_файла = '{file_name}'")
            cur.execute(f"delete from {table_name}")
            r = 0
            sr = r
            rows_limit = 100000
            while True:
                table = pd.read_excel(path, header=0, nrows=rows_limit, skiprows=sr, usecols=cols, sheet_name=0)
                table_size = len(table)

                if not table_size:
                    break
                r += table_size
                sr = range(1, r + 1)
                table = table.reindex(columns=cols)
                pool_req = f"insert into {table_name} values"
                for v_id, i in enumerate(table.values):
                    req = ''
                    try:
                        for content in i:
                            c = str(content).replace('\'', '\'\'').replace(";", " ").upper()
                            if c == 'NAN':
                                req += 'NULL, '
                            else:
                                req += f"'{c}', "
                        req = req[:-2]
                        pool_req += f"({req}), "

                        # отправка 500 объединённых запросов к БД за один раз
                        if (v_id % 500 == 0 or v_id == table_size-1) and v_id > 0:
                            try:
                                pool_req = pool_req[:-2]
                                pool_req += "ON CONFLICT DO NOTHING;"
                                cur.execute(pool_req)
                                pool_req = f"insert into {table_name} values"
                            except Exception as ex1:
                                logger.error("insert3 error:", exc_info=ex1)
                                InfoModule.increase_error_count()



                    except Exception as val_error:
                        logger.error("val error:", exc_info=val_error)
                        InfoModule.increase_error_count()

            cur.execute(f"insert into Время_изменений_справочники values('{file_name}', '{t}')")
        connection.commit()
        connection.close()
        logger.info(f"{file_name} обновлён")
    except Exception as ex:
        logger.error("update_brand_catalog error:", exc_info=ex)
        InfoModule.increase_error_count()