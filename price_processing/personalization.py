'''
Формирует прайсы покупателей из прайсов на выход 3.
'''
import time
import multiprocessing as mp
import os
import shutil
import datetime
from datetime import timedelta

import pandas as pd
import numpy as np
import psycopg2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import sys
import logging
from logger import configure_logging
from info_module import info_module

logger = logging.getLogger(__name__)
configure_logging(logger, 'logs/personalization.log')

MODULE_NUM = 3
InfoModule = None

host = ''
user = ''
password = ''
db_name = ''
path_to_exit3 = ''
path_to_final = ''
path_to_info = ''

class personalization():
    def __init__(self, cls):
        self.main_ui = cls
        global host, user, password, db_name, path_to_exit3, path_to_final, path_to_info, InfoModule
        InfoModule = info_module(cls, module_num=MODULE_NUM)
        host = self.main_ui.host
        user = self.main_ui.user
        password = self.main_ui.password
        db_name = self.main_ui.db_name
        path_to_exit3 = self.main_ui.path_to_exit3
        path_to_final = self.main_ui.path_to_final
        path_to_info = self.main_ui.path_to_info

        mp.freeze_support()

    def StartProcess(self):
        '''Запуск основного цикла'''
        self.act = Action(self)
        self.t = QtCore.QThread()
        self.act.moveToThread(self.t)
        self.main_ui.StartButton_6.setEnabled(False)
        self.main_ui.UpdateButton_all.setEnabled(False)
        self.main_ui.UpdateButton_selected.setEnabled(False)
        self.t.started.connect(self.act.mainCircle)
        self.act.finishSignal.connect(self.setOnStartButton)
        self.act.finishSignal.connect(self.setModuleStatusPause)

        self.main_ui.Module_status_4.setText("Работает")
        self.main_ui.Module_status_4.setStyleSheet(f"color: green;")
        self.t.start()
        self.t.quit()

    def UpdateTable(self):
        '''Обновление таблицы с прайсами покупателей для последующей возможности выбрать и обновить необходимые'''
        headers = ['Имя прайса', 'Код', 'Обновить']
        self.main_ui.PricesTable_6.setColumnCount(len(headers))
        self.main_ui.PricesTable_6.setHorizontalHeaderLabels(headers)

        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cur:
                cur.execute(
                    "select Имя_прайса, Код_прайса_покупателя from Настройки_прайса_покупателя")
                data = cur.fetchall()
            connection.close()

            self.main_ui.PricesTable_6.setRowCount(len(data))
            for id, d in enumerate(data):
                self.main_ui.PricesTable_6.setItem(id, 0, QTableWidgetItem(str(d[0]))) # name
                self.main_ui.PricesTable_6.setItem(id, 1, QTableWidgetItem(str(d[1]))) # code
                sb = QtWidgets.QCheckBox()
                sb.setStyleSheet("QCheckBox::indicator { width: 70px; height: 70px;}")
                self.main_ui.PricesTable_6.setCellWidget(id, 2, sb)

        except Exception as ex:
            logger.error("[UpdateTable error]:", exc_info=ex)
            InfoModule.increase_error_count()

    def UpdateSelected(self):
        '''Обновление выбранных в таблице прайсов'''
        self.act2 = Action(self)
        self.t2 = QtCore.QThread()
        self.act2.moveToThread(self.t2)
        self.main_ui.StartButton_6.setEnabled(False)
        self.main_ui.UpdateButton_all.setEnabled(False)
        self.main_ui.UpdateButton_selected.setEnabled(False)
        self.t2.started.connect(self.act2.UpdateSelected)
        self.act2.finishSignal.connect(self.setOnStartButton)
        self.act2.finishSignal.connect(self.setModuleStatusPause)

        self.main_ui.Module_status_4.setText("Работает")
        self.main_ui.Module_status_4.setStyleSheet(f"color: green;")
        self.t2.start()
        self.t2.quit()

    def UpdateAll(self):
        '''Обновление всех прайсов'''
        self.act3 = Action(self)
        self.t3 = QtCore.QThread()
        self.act3.moveToThread(self.t3)
        self.main_ui.StartButton_6.setEnabled(False)
        self.main_ui.UpdateButton_all.setEnabled(False)
        self.main_ui.UpdateButton_selected.setEnabled(False)
        self.t3.started.connect(self.act3.UpdateAll)
        self.act3.finishSignal.connect(self.setOnStartButton)
        self.act3.finishSignal.connect(self.setModuleStatusPause)

        self.main_ui.Module_status_4.setText("Работает")
        self.main_ui.Module_status_4.setStyleSheet(f"color: green;")
        self.t3.start()
        self.t3.quit()

    def setModuleStatusPause(self):
        self.main_ui.Module_status_4.setText("Пауза")
        self.main_ui.Module_status_4.setStyleSheet(f"color: red;")

    def setOnStartButton(self):
        self.main_ui.StartButton_6.setEnabled(True)
        self.main_ui.UpdateButton_all.setEnabled(True)
        self.main_ui.UpdateButton_selected.setEnabled(True)


class Action(QtCore.QThread):
    '''Класс для многопоточной работы в PyQt'''
    finishSignal = QtCore.pyqtSignal(int)
    def __init__(self, mainApp=None):
        super(Action, self).__init__()
        self.mainApp = mainApp

    def mainCircle(self):
        '''Основной цикл, начинает обновлять прайсы покупателей за пол часа до их отправки'''
        wait_sec = 60

        while True:
            now1 = datetime.datetime.now()
            try:
                if self.mainApp.main_ui.Pause_6.isChecked():
                    self.mainApp.main_ui.Pause_6.setChecked(False)
                    self.finishSignal.emit(1)
                    return
                InfoModule.set_update_time(MODULE_NUM, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                self.delete_unnecessary_prices()
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    cur.execute("delete from price_list")
                    cur.execute("ALTER SEQUENCE price_list_id_seq restart 1")

                    cur.execute(f"select Код_прайса_покупателя from Настройки_прайса_покупателя where upper(Включен) = 'ДА'")
                    price_list = cur.fetchall()
                connection.commit()
                connection.close()

                if price_list:
                    mng = mp.Manager()
                    error_counts = mng.Value('error_counts', 0)
                    tsk = []
                    for p in price_list:
                        tsk.append([p[0], host, user, password, db_name, path_to_final, path_to_info, error_counts, False])

                    threads = self.mainApp.main_ui.ThreadSpinBox_4.value()

                    with (mp.Pool(processes=threads)) as p:
                        p.map(cerate_files, tsk)
                    InfoModule.increase_error_count(count=error_counts.value)

                # проверка на паузу
                now2 = datetime.datetime.now()
                if wait_sec > (now2 - now1).seconds:
                    for _ in range(wait_sec - (now2 - now1).seconds):
                        if self.mainApp.main_ui.Pause_6.isChecked():
                            self.mainApp.main_ui.Pause_6.setChecked(False)
                            self.finishSignal.emit(1)
                            return
                        time.sleep(1)

            except Exception as ex:
                logger.error("mainCycle error:", exc_info=ex)
                InfoModule.increase_error_count()
                time.sleep(5)


    def delete_unnecessary_prices(self):
        '''Удаляет неактуальные(удаленные и тд) прайсы из общей таблицы с прайсами total'''
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            cur.execute(f"select distinct(Код_поставщика) from total where Код_поставщика not in "
                        f"(select Код_прайса from Настройки_прайса_поставщика where Сохраняем = 'ДА')")
            res = cur.fetchall()
            if not res:
                return

            for p in res:
                cur.execute(f"delete from total where Код_поставщика = '{p[0]}'")
        connection.commit()
        connection.close()


    def UpdateSelected(self):
        '''Обновление выбранных в таблице прайсов'''
        try:
            price_list = list()
            for i in range(self.mainApp.main_ui.PricesTable_6.rowCount()):
                if self.mainApp.main_ui.PricesTable_6.cellWidget(i, 2).checkState():
                    price_list.append(self.mainApp.main_ui.PricesTable_6.item(i, 1).text())

            if price_list:
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    cur.execute("delete from price_list")
                    cur.execute("ALTER SEQUENCE price_list_id_seq restart 1")
                connection.commit()
                connection.close()

                mng = mp.Manager()
                error_counts = mng.Value('error_counts', 0)
                tsk = []
                for p in price_list:
                    tsk.append([p, host, user, password, db_name, path_to_final, path_to_info, error_counts, True])

                threads = self.mainApp.main_ui.ThreadSpinBox_4.value()

                with (mp.Pool(processes=threads)) as p:
                    p.map(cerate_files, tsk)
                InfoModule.increase_error_count(count=error_counts.value)

        except Exception as ex:
            logger.error("[UpdateSelected error]:", exc_info=ex)
            InfoModule.increase_error_count()
        finally:
            self.finishSignal.emit(1)


    def UpdateAll(self):
        '''Обновление всех прайсов'''
        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cur:
                cur.execute("delete from price_list")
                cur.execute("ALTER SEQUENCE price_list_id_seq restart 1")

                cur.execute(f"select Код_прайса_покупателя from Настройки_прайса_покупателя") # where upper(Включен) = 'ДА'
                price_list = cur.fetchall()
            connection.commit()
            connection.close()

            if price_list:
                mng = mp.Manager()
                error_counts = mng.Value('error_counts', 0)
                tsk = []
                for p in price_list:
                    tsk.append([p[0], host, user, password, db_name, path_to_final, path_to_info, error_counts, True])

                threads = self.mainApp.main_ui.ThreadSpinBox_4.value()

                with (mp.Pool(processes=threads)) as p:
                    p.map(cerate_files, tsk)
                InfoModule.increase_error_count(count=error_counts.value)

        except Exception as ex:
            logger.error("[UpdateAll error]:", exc_info=ex)
            InfoModule.increase_error_count()
        finally:
            self.finishSignal.emit(1)


def cerate_files(args):
    '''Формирует прайсы для покупателей'''
    try:
        price_code, host, user, password, db_name, path_to_final, path_to_info, error_counts, cont = args

        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            cur.execute(f"select Код_покупателя, Имя_прайса,Уровень_сервиса_не_ниже, Наименование, Короткое_наименование, Продаём_для_К_ОС, "
                        f"Отсрочка_дней, Наценка_для_К_ОС, Итоговая_наценка, КБ_цены, Ограничение_строк, Ограничение_размера, Время_рассылки_прайса "
                        f"from Настройки_прайса_покупателя where Код_прайса_покупателя = '{price_code}'")
            res = cur.fetchone()
            if not res:
                return
            buyer_code, price_name, percent, name, short_name, sell_oc, delay, markup_os, final_markup, KB_price, lines_limit, size_limit, send_time= res

            if not cont:
                cont = check_continue(cur, price_code, send_time)
        connection.commit()
        connection.close()

        if cont == False:
            return

        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            logger.info(f"{price_code} ...")

            # Загрузка позиций из total
            cur.execute(f"insert into price_list(КлючП, АртикулП, БрендП, НаименованиеП, КоличествоП, ЦенаП, Валюта, КратностьП, "
                        f"ПримечаниеП, Артикул, АртикулР, Бренд, Бренд_заполнен, Наименование, Количество, "
                        f"Цена, Кратность, Код_поставщика, Разрешение_на_продажу, Кратность_лота, Цена_поставщика_с_издержками, "
                        f"ЦенаБ, Исключить, Градация, Предложений_в_опте, Цена_с_наценкой, Имя_прайса, Код_покупателя, Код_прайсаП) "
                        f"select total.КлючП, total.АртикулП, total.БрендП, total.НаименованиеП, total.КоличествоП, total.ЦенаП, "
                        f"total.Валюта, total.КратностьП, total.ПримечаниеП, total.Артикул, upper(regexp_replace(total.Артикул, '\W|_', '', 'g')), total.Бренд, "
                        f"total.Бренд_заполнен, total.Наименование, total.Количество, total.Цена, total.Кратность, "
                        f"total.Код_поставщика, total.Разрешение_на_продажу, total.Кратность_лота, total.Цена_поставщика_с_издержками, "
                        f"total.ЦенаБ, total.Исключить, total.Градация, total.Предложений_в_опте, total.Цена_с_наценкой, "
                        f"'{price_name}', '{buyer_code}', '{price_code}' "
                        f"from total, (select Разрешения_бпп.Код_прайса, Разрешения_бпп.Бренд from Разрешения_бпп, "
                        f"(select Код_прайса from Настройки_прайса_поставщика where Код_прайса in "
                        f"(select distinct(Код_поставщика) from total) and Разрешения_ПП like '%{buyer_code}%') as T "
                        f"where Разрешения_бпп.Код_прайса = T.Код_прайса) as T2 "
                        f"where total.Код_поставщика = T2.Код_прайса and total.Бренд = T2.Бренд")

            cur.execute(f"update price_list set Исключить = 'Разрешение на продажу' "
                        f"where Разрешение_на_продажу is not NULL and Разрешение_на_продажу not like '%{buyer_code}%' and Код_прайсаП = '{price_code}'")

            # Отнять КоличествоР
            cur.execute(f"update price_list set Количество = Количество - ШтР from Резерв where "
                        f"Код_поставщика = Резерв.Код_прайса and Бренд_заполнен = Наш_Бренд and АртикулР = Артикул_сравнение and Код_прайсаП = '{price_code}'")

            # Обрезание %
            cur.execute(f"update price_list set Количество = trunc(Количество * Процент_отгрузки) from "
                        f"Настройки_прайса_поставщика where Процент_отгрузки < {percent} and Настройки_прайса_поставщика.Код_прайса = price_list.Код_поставщика and Код_прайсаП = '{price_code}'")

            cur.execute(f"delete from price_list where Количество <= 0 and Код_прайсаП = '{price_code}'")

            if str(short_name).upper() == 'ДА':
                cur.execute(f"update price_list set Наименование = left(price_list.Наименование, T2.Краткое_наименование) from "
                            f"(select Краткое_наименование, Код_прайса from Настройки_прайса_поставщика, "
                            f"(select distinct(Код_поставщика) from price_list) as T where Код_прайса = T.Код_поставщика) as T2, "
                            f"(select Наименование from correct_brands where Короткое_наименование = 'ДА') as T3 "
                            f"where T2.Код_прайса = price_list.Код_поставщика and T2.Краткое_наименование > 0 and price_list.Бренд_заполнен = T3.Наименование "
                            f"and Код_прайсаП = '{price_code}'")

            cur.execute(f"update price_list set Бренд_итог = Бренд_покупателя from Справочник_Бренды_покупателя "
                        f"where Покупатель = '{name}' and Правильный_Бренд = Бренд and Код_прайсаП = '{price_code}'")
            cur.execute(f"update price_list set Бренд_итог = Бренд_заполнен where Бренд_итог is NULL and Код_прайсаП = '{price_code}'")

            if str(sell_oc).upper() == 'ДА':
                cur.execute(f"update price_list set Цена_итог = Цена_поставщика_с_издержками * (({markup_os} + 1) - (Наценка_для_ОС * ({delay} - C.Отсрочка))) "
                            f"from (select Код_прайса, Наценка_для_ОС, Отсрочка from Настройки_прайса_поставщика where Закупка_для_оборотных_средств = 'ДА' "
                            f"and {delay} > Отсрочка) as C where Код_поставщика = C.Код_прайса and Код_прайсаП = '{price_code}'")

            cur.execute(f"update price_list set Цена_итог = Цена_поставщика_с_издержками * ({final_markup} + 1) where Цена_итог is NULL and Код_прайсаП = '{price_code}'")

            remove_rep(cur, price_code)

            cur.execute(f"update price_list set Превышение_базовой_цены = Цена_итог/ЦенаБ where ЦенаБ is not NULL and Код_прайсаП = '{price_code}'")
            cur.execute(f"update price_list set Исключить = 'Превышение КБ Цена' where Превышение_базовой_цены > {KB_price} and Код_прайсаП = '{price_code}'")

            cur.execute(f"update price_list set Рейтинг_в_прайс = Рейтинг_поставщика + Превышение_базовой_цены "
                        f"from Настройки_прайса_поставщика where price_list.Код_поставщика = Настройки_прайса_поставщика.Код_прайса and Код_прайсаП = '{price_code}'")
            cur.execute(f"update price_list set Рейтинг_в_прайс = Рейтинг_в_прайс + 1 where Бренд is NULL and Код_прайсаП = '{price_code}'")
        connection.commit()
        connection.close()

        # формирует итоговые прайсы учитывая их лимиты на размер файла или количество строк
        if size_limit:
            create_csv_with_size_limit(host, user, password, db_name, path_to_info, size_limit, price_code, price_name)
        elif lines_limit:
            create_csv_with_row_limit(host, user, password, db_name, path_to_info, lines_limit, price_code, price_name)
        else:
            create_csv(host, user, password, db_name, path_to_info, price_code, price_name)

        # перенос полностью сформированного прайса
        shutil.copy(fr"tmp_/{price_name}.csv", fr"{path_to_final}/{price_name}.csv")

        creare_csv_except(host, user, password, db_name, path_to_info, price_code, price_name)

        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            cur.execute(f"update Время_отправки_прайсов set last_update_time = '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}' where Код_прайса_покупателя = '{price_code}'")
            cur.execute(f"delete from price_list where Код_прайсаП = '{price_code}'")
        connection.commit()
        connection.close()

        logger.info(f'{price_code} готов')
    except Exception as ex:
        logger.error(f"create error:", exc_info=ex)
        error_counts.value += 1


def remove_rep(cur, price_code):
    '''Удаление повторяющихся позиций (Артикул, Бренд)'''
    cur.execute(f"select count(*) from (select from price_list group by Артикул, Бренд having count(*) > 1)")
    rep_count = cur.fetchone()[0]
    if rep_count != 0:
        logger.info(f"Удаление дублей в {price_code} ...")
        # DEL для всех повторений
        cur.execute(f"update price_list as mainT set Исключить = 'DEL' where (mainT.Артикул, mainT.Бренд) in "
                    f"(select Артикул, Бренд from price_list where Исключить is NULL and Код_прайсаП = '{price_code}' group by Артикул, Бренд having count(*) > 1)")
        # Убирается DEL в каждой группе повторения, если Цена_итог в группе минимальная
        cur.execute(
            f"update price_list set Исключить = NULL from (select Артикул, Бренд, count(*), min(Цена_итог) as min_price "
            f"from price_list where Исключить = 'DEL' and Код_прайсаП = '{price_code}' group by Артикул, Бренд HAVING COUNT(*) > 1) as T "
            f"where price_list.Артикул = T.Артикул and price_list.Бренд = T.Бренд and price_list.Код_прайсаП = '{price_code}' and price_list.Цена_итог = T.min_price")
        # Среди записей с убранным DEL ищутся записи не с максимальным кол-вом и на них устанавливается DEL
        cur.execute(f"update price_list as mainT set Исключить = 'DEL' from (select Артикул, Бренд, count(*), max(Количество) "
                    f"as max_count from price_list where Исключить = NULL and Код_прайсаП = '{price_code}' group by Артикул, Бренд having count(*) > 1) "
                    f"as T where (mainT.Артикул, mainT.Бренд) = (T.Артикул, T.Бренд) and Количество != T.max_count")
        # В оставшихся группах, где совпадает мин. Цена_итог и макс. кол-вл, остаются лишь записи с максимальным id
        cur.execute(f"update price_list as mainT set Исключить = 'DEL' from (select Артикул, Бренд, max(id) as maxId "
                    f"from price_list where Код_прайсаП = '{price_code}' group by Артикул, Бренд having count(*) > 1) as T "
                    f"where (mainT.Артикул, mainT.Бренд) = (T.Артикул, T.Бренд) and mainT.id != T.maxId")

        logger.info(f"Удаление дублей в {price_code} завершено.")


def create_csv(host, user, password, db_name, path_to_info, price_code, price_name):
    '''Создание csv файла без лимитов'''
    limit = 100000

    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    req = """SELECT КлючП as "КлючП", АртикулП as "АртикулП", БрендП as "БрендП",
                     НаименованиеП as "НаименованиеП", КоличествоП as "КоличествоП", ЦенаП as "ЦенаП",
                     Валюта as "ВалютаП", КратностьП as "КратностьП", ПримечаниеП as "ПримечаниеП",
                     Артикул as "Артикул", Бренд as "БрендН",
                     Наименование as "Наименование", Количество as "Количество", Цена as "Цена закупки",
                     Кратность as "КратностьН", Код_поставщика as "Код прайса",
                     Разрешение_на_продажу as "Разрешение на продажу проблемной позиции",
                     Кратность_лота as "Кратность лота", Цена_поставщика_с_издержками as "Цена поставщика с издержками",
                     Исключить as "Причины исключения", Градация as "Градация", Предложений_в_опте as "Предложений в опте",
                     Цена_с_наценкой as "Цена с наценкой на прайс поставщика", Код_покупателя as "Код покупателя",
                     Код_прайсаП as "Код прайса покупателя", Бренд_итог as "Бренд", Цена_итог as "Цена", Превышение_базовой_цены as "Превышение базовой цены",
                     Рейтинг_в_прайс as "Рейтинг в прайс" FROM price_list
                     where Код_прайсаП = '{}' and Исключить is NULL ORDER BY Рейтинг_в_прайс OFFSET {} LIMIT {}"""

    req2 = """SELECT Артикул as "Артикул", Наименование as "Наименование", Количество as "Количество", Кратность_лота as "Кратность", 
                     Бренд_итог as "Бренд", Цена_итог as "Цена" FROM price_list 
                     where Код_прайсаП = '{}' and Исключить is NULL ORDER BY Рейтинг_в_прайс OFFSET {} LIMIT {}"""

    df = pd.read_sql(req.format(price_code, 0, limit), connection)
    df.to_csv(fr"{path_to_info}/{price_name}_.csv", sep=';', encoding='windows-1251', index=False,
              errors='ignore')

    df = pd.read_sql(req2.format(price_code, 0, limit), connection)
    df.to_csv(fr"tmp_/{price_name}.csv", sep=';', encoding='windows-1251', index=False,
              errors='ignore')

    loaded = limit
    while True:
        df = pd.read_sql(req.format(price_code, loaded, limit), connection)
        if not len(df):
            break
        df.to_csv(fr"{path_to_info}/{price_name}_.csv", mode='a', sep=';', encoding="windows-1251", index=False,
                  header=False, errors='ignore')

        df = pd.read_sql(req2.format(price_code, loaded, limit), connection)
        df.to_csv(fr"tmp_/{price_name}.csv", mode='a', sep=';', encoding="windows-1251", index=False,
                  header=False, errors='ignore')

        loaded += limit
    connection.close()

def create_csv_with_row_limit(host, user, password, db_name, path_to_info, local_limit, price_code, price_name):
    '''Создание csv файла с лимитом на количество строк'''
    limit = 100000

    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    req = """SELECT КлючП as "КлючП", АртикулП as "АртикулП", БрендП as "БрендП",
                     НаименованиеП as "НаименованиеП", КоличествоП as "КоличествоП", ЦенаП as "ЦенаП",
                     Валюта as "ВалютаП", КратностьП as "КратностьП", ПримечаниеП as "ПримечаниеП",
                     Артикул as "Артикул", Бренд as "БрендН",
                     Наименование as "Наименование", Количество as "Количество", Цена as "Цена закупки",
                     Кратность as "КратностьН", Код_поставщика as "Код прайса",
                     Разрешение_на_продажу as "Разрешение на продажу проблемной позиции",
                     Кратность_лота as "Кратность лота", Цена_поставщика_с_издержками as "Цена поставщика с издержками",
                     Исключить as "Причины исключения", Градация as "Градация", Предложений_в_опте as "Предложений в опте",
                     Цена_с_наценкой as "Цена с наценкой на прайс поставщика", Код_покупателя as "Код покупателя",
                     Код_прайсаП as "Код прайса покупателя", Бренд_итог as "Бренд", Цена_итог as "Цена", Превышение_базовой_цены as "Превышение базовой цены",
                     Рейтинг_в_прайс as "Рейтинг в прайс" FROM price_list
                     where Код_прайсаП = '{}' and Исключить is NULL ORDER BY Рейтинг_в_прайс OFFSET {} LIMIT {}"""

    req2 = """SELECT Артикул as "Артикул", Наименование as "Наименование", Количество as "Количество", Кратность_лота as "Кратность", 
                     Бренд_итог as "Бренд", Цена_итог as "Цена" FROM price_list 
                     where Код_прайсаП = '{}' and Исключить is NULL ORDER BY Рейтинг_в_прайс OFFSET {} LIMIT {}"""

    if limit > local_limit:
        limit = local_limit
    df = pd.read_sql(req.format(price_code, 0, limit), connection)
    df.to_csv(fr"{path_to_info}/{price_name}_.csv", sep=';', encoding='windows-1251', index=False,
              errors='ignore')

    df = pd.read_sql(req2.format(price_code, 0, limit), connection)
    df.to_csv(fr"tmp_/{price_name}.csv", sep=';', encoding='windows-1251', index=False,
              errors='ignore')

    loaded = limit
    while True:
        if loaded + limit > local_limit:
            limit = local_limit - loaded
        df = pd.read_sql(req.format(price_code, loaded, limit), connection)
        if not len(df):
            break
        df.to_csv(fr"{path_to_info}/{price_name}_.csv", mode='a', sep=';', encoding="windows-1251", index=False,
                  header=False, errors='ignore')

        df = pd.read_sql(req2.format(price_code, loaded, limit), connection)
        df.to_csv(fr"tmp_/{price_name}.csv", mode='a', sep=';', encoding="windows-1251", index=False,
                  header=False, errors='ignore')

        loaded += limit
    connection.close()


def create_csv_with_size_limit(host, user, password, db_name, path_to_info, size_limit, price_code, price_name):
    '''Создание csv файла с лимитом на размер файла'''
    limit = 1000

    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    req = """SELECT КлючП as "КлючП", АртикулП as "АртикулП", БрендП as "БрендП",
                     НаименованиеП as "НаименованиеП", КоличествоП as "КоличествоП", ЦенаП as "ЦенаП",
                     Валюта as "ВалютаП", КратностьП as "КратностьП", ПримечаниеП as "ПримечаниеП",
                     Артикул as "Артикул", Бренд as "БрендН",
                     Наименование as "Наименование", Количество as "Количество", Цена as "Цена закупки",
                     Кратность as "КратностьН", Код_поставщика as "Код прайса",
                     Разрешение_на_продажу as "Разрешение на продажу проблемной позиции",
                     Кратность_лота as "Кратность лота", Цена_поставщика_с_издержками as "Цена поставщика с издержками",
                     Исключить as "Причины исключения", Градация as "Градация", Предложений_в_опте as "Предложений в опте",
                     Цена_с_наценкой as "Цена с наценкой на прайс поставщика", Код_покупателя as "Код покупателя",
                     Код_прайсаП as "Код прайса покупателя", Бренд_итог as "Бренд", Цена_итог as "Цена", Превышение_базовой_цены as "Превышение базовой цены",
                     Рейтинг_в_прайс as "Рейтинг в прайс" FROM price_list
                     where Код_прайсаП = '{}' and Исключить is NULL ORDER BY Рейтинг_в_прайс OFFSET {} LIMIT {}"""

    req2 = """SELECT Артикул as "Артикул", Наименование as "Наименование", Количество as "Количество", Кратность_лота as "Кратность", 
                     Бренд_итог as "Бренд", Цена_итог as "Цена" FROM price_list 
                     where Код_прайсаП = '{}' and Исключить is NULL ORDER BY Рейтинг_в_прайс OFFSET {} LIMIT {}"""

    df = pd.read_sql(req.format(price_code, 0, limit), connection)
    df.to_csv(fr"{path_to_info}/{price_name}_.csv", sep=';', encoding='windows-1251', index=False,
              errors='ignore')

    df = pd.read_sql(req2.format(price_code, 0, limit), connection)
    df.to_csv(fr"tmp_/{price_name}.csv", sep=';', encoding='windows-1251', index=False,
              errors='ignore')

    loaded = limit
    while True:
        if os.path.getsize(fr"tmp_/{price_name}.csv") / 1024 / 1024 > size_limit:
            break
        df = pd.read_sql(req.format(price_code, loaded, limit), connection)
        if not len(df):
            break
        df.to_csv(fr"{path_to_info}/{price_name}_.csv", mode='a', sep=';', encoding="windows-1251", index=False,
                  header=False, errors='ignore')

        df = pd.read_sql(req2.format(price_code, loaded, limit), connection)
        df.to_csv(fr"tmp_/{price_name}.csv", mode='a', sep=';', encoding="windows-1251", index=False,
                  header=False, errors='ignore')

        loaded += limit
    connection.close()

def creare_csv_except(host, user, password, db_name, path_to_info, price_code, price_name):
    '''Создание csv файла с позициями, где поле Исключить НЕ пустое'''
    limit = 100000

    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    req = """SELECT КлючП as "КлючП", АртикулП as "АртикулП", БрендП as "БрендП",
                         НаименованиеП as "НаименованиеП", КоличествоП as "КоличествоП", ЦенаП as "ЦенаП",
                         Валюта as "ВалютаП", КратностьП as "КратностьП", ПримечаниеП as "ПримечаниеП",
                         Артикул as "Артикул", Бренд as "БрендН",
                         Наименование as "Наименование", Количество as "Количество", Цена as "Цена закупки",
                         Кратность as "КратностьН", Код_поставщика as "Код прайса",
                         Разрешение_на_продажу as "Разрешение на продажу проблемной позиции",
                         Кратность_лота as "Кратность лота", Цена_поставщика_с_издержками as "Цена поставщика с издержками",
                         Исключить as "Причины исключения", Градация as "Градация", Предложений_в_опте as "Предложений в опте",
                         Цена_с_наценкой as "Цена с наценкой на прайс поставщика", Код_покупателя as "Код покупателя",
                         Код_прайсаП as "Код прайса покупателя", Бренд_итог as "Бренд", Цена_итог as "Цена", Превышение_базовой_цены as "Превышение базовой цены",
                         Рейтинг_в_прайс as "Рейтинг в прайс" FROM price_list
                         where Код_прайсаП = '{}' and Исключить is not NULL ORDER BY Рейтинг_в_прайс OFFSET {} LIMIT {}"""

    df = pd.read_sql(req.format(price_code, 0, limit), connection)
    df.to_csv(fr"{path_to_info}/{price_name}_исключения.csv", sep=';', encoding='windows-1251', index=False,
              errors='ignore')

    loaded = limit

    while True:
        df = pd.read_sql(req.format(price_code, loaded, limit), connection)
        if not len(df):
            break
        df.to_csv(fr"{path_to_info}/{price_name}_исключения.csv", mode='a', sep=';', encoding="windows-1251", index=False,
                  header=False, errors='ignore')

        loaded += limit
    connection.close()

def check_continue(cur, price_code, send_time):
    '''Проверка времени обновления прайса, прайс начинает формироваться 'за пол часа до отправки'''
    cur.execute(
        f"select last_update_time, last_send_time from Время_отправки_прайсов where Код_прайса_покупателя = '{price_code}'")
    res = cur.fetchone()
    if not res:
        cur.execute(f"insert into Время_отправки_прайсов(Код_прайса_покупателя) values('{price_code}')")

    cur.execute(
        f"select last_update_time, last_send_time from Время_отправки_прайсов where Код_прайса_покупателя = '{price_code}'")
    times = cur.fetchone()

    now = datetime.datetime.now()
    new_last_time_upd = False
    if not times[0]:
        last_update_time = now
        new_last_time_upd = True
    else:
        last_update_time = times[0]

    time_list = list()
    for t in send_time.split():
        h, m = t.split('-')
        h = int(h)
        m = int(m)
        file_creation_time = datetime.datetime.strptime(f"{str(now.strftime('%Y-%m-%d'))} {h}:{m}", '%Y-%m-%d %H:%M') - timedelta(minutes=30)

        if file_creation_time <= now:
            time_list.append(file_creation_time)

    if not time_list:
        if new_last_time_upd:
            return True
        return False

    actual_time = max(time_list)
    if not new_last_time_upd:
        if actual_time < last_update_time:
            return False
    return True