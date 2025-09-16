'''
Преобразовывает прайсы (выход 2) в итоговые прайсы, которые используются для формирования прайсов покупателей.
Выход 2 -> Выход 3
'''
import time
import datetime
import multiprocessing as mp
import os
import math
from decimal import Decimal
import pandas as pd
import psycopg2
from PyQt5 import QtCore
import logging
from logger import configure_logging
from info_module import info_module

logger = logging.getLogger(__name__)
configure_logging(logger, 'logs/price_proc.log')

logger_report = logging.getLogger('report2')
configure_logging(logger_report, 'logs/Отчёт - обработка прайсов.log')

logger_report_over = logging.getLogger('report3')
configure_logging(logger_report_over, 'logs/Отчёт - превышение допустимного процента изменения цены и кол-ва строк.log')

MODULE_NUM = 2
InfoModule = None

host = ''
user = ''
password = ''
db_name = ''
path_to_catalogs = ''
path_to_exit2 = ''
path_to_exit3 = ''
path_to_exp = ''

class price_proc():
    def __init__(self, cls):
        self.main_ui = cls
        global host, user, password, db_name, path_to_prices, path_to_catalogs, path_to_exit2, path_to_exit3, path_to_exp, InfoModule
        InfoModule = info_module(cls, module_num=MODULE_NUM)
        host = self.main_ui.host
        user = self.main_ui.user
        password = self.main_ui.password
        db_name = self.main_ui.db_name
        path_to_prices = self.main_ui.Dir
        path_to_catalogs = self.main_ui.path_to_catalogs
        path_to_exit2 = self.main_ui.path_to_exit2
        path_to_exit3 = self.main_ui.path_to_exit3
        path_to_exp = self.main_ui.path_to_exp

        mp.freeze_support()


    def StartProcess(self):
        self.act = Action(self)
        self.t = QtCore.QThread()
        self.act.moveToThread(self.t)
        self.main_ui.Start_1.setEnabled(False)
        self.t.started.connect(self.act.mainCircle)
        self.act.finishSignal.connect(self.setOnStartButton)
        self.act.finishSignal.connect(self.setModuleStatusPause)

        self.main_ui.Module_status_3.setText("Работает")
        self.main_ui.Module_status_3.setStyleSheet(f"color: green;")
        self.t.start()
        self.t.quit()

    def setModuleStatusPause(self):
        self.main_ui.Module_status_3.setText("Пауза")
        self.main_ui.Module_status_3.setStyleSheet(f"color: red;")

    def setOnStartButton(self):
        self.main_ui.Start_1.setEnabled(True)


class Action(QtCore.QThread):
    '''Класс для многопоточной работы в PyQt'''
    finishSignal = QtCore.pyqtSignal(int)
    def __init__(self, mainApp=None):
        super(Action, self).__init__()
        self.mainApp = mainApp

    def mainCircle(self):
        '''Основной цикл, проверяет новые файлы на выходе 2, обрабатывает их в несколько потоков'''
        wait_sec = 90

        while True:
            # logs = ['logs\price_proc.log', 'logs/Отчёт - обработка прайсов.log', 'logs/Отчёт - превышение допустимного процента изменения цены и кол-ва строк.log']
            # for l in logs:
            #     if os.path.getsize(l) / 1048576 > 20:
            #         os.rename(l,f"{l}.1")

            now1 = datetime.datetime.now()
            if self.mainApp.main_ui.Pause_1.isChecked():
                self.mainApp.main_ui.Pause_1.setChecked(False)
                self.finishSignal.emit(1)
                return

            try:
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    InfoModule.set_update_time(MODULE_NUM, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    # logger.info(f"")
                    # logger_report.info(f"")
                    # logger_report_over.info(f"")
                    price_list = set()
                    for f in os.listdir(path_to_exit2):
                        if f[0] == '~':
                            continue

                        file_name_ = f[:4]
                        t = datetime.datetime.fromtimestamp(os.path.getmtime(fr"{path_to_exit2}/{f}")).strftime("%Y-%m-%d %H:%M:%S")
                        cur.execute(f"select Время_изменения from Время_изменений_выход2 where Название_файла = '{file_name_}'")
                        res = cur.fetchone()

                        if res:
                            if res[0] != t:
                                price_list.add(f)
                        else:
                            price_list.add(f)

                    mng = mp.Manager()
                    error_counts = mng.Value('error_counts', 0)
                    fls = []
                    for i in price_list:
                        fls.append([i, host, user, password, db_name, path_to_exit2, path_to_exit3, path_to_exp, error_counts])

                    cur.execute(f"DELETE FROM res2")
                    cur.execute(f"delete from tmp_price_compare")
                    cur.execute(f"ALTER SEQUENCE res2_id_seq restart 1")
                    cur.execute(f"ALTER SEQUENCE tmp_price_compare_id_seq restart 1")
                connection.commit()
                connection.close()

                threads = self.mainApp.main_ui.ThreadSpinBox_1.value()
                with (mp.Pool(processes=threads)) as p:
                    p.map(update_files, fls)
                InfoModule.increase_error_count(count=error_counts.value)

                # проверка на паузу
                now2 = datetime.datetime.now()
                if wait_sec > (now2 - now1).seconds:
                    for _ in range(wait_sec - (now2 - now1).seconds):
                        if self.mainApp.main_ui.Pause_1.isChecked():
                            self.mainApp.main_ui.Pause_1.setChecked(False)
                            self.finishSignal.emit(1)
                            return
                        time.sleep(1)

            except Exception as ex:
                logger.error("mainCircle error:", exc_info=ex)
                InfoModule.increase_error_count()
                time.sleep(5)

def update_files(args):
    '''Обработка прайса с выхода 2 до выхода 3'''
    try:
        file_name, host, user, password, db_name, path_to_exit2, path_to_exit3, path_to_exp, error_counts = args

        file_name_ = file_name[:4]
        logger.info(f"{file_name_} ...")
        last_change_time = datetime.datetime.fromtimestamp(os.path.getmtime(fr"{path_to_exit2}/{file_name}")).strftime("%Y-%m-%d %H:%M:%S")

        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            cur.execute(f"DELETE FROM Время_изменений_выход2 WHERE Название_файла = '{file_name_}'")
            cur.execute(f"select Работаем from Настройки_прайса_поставщика where Код_прайса = '{file_name_}'")
            res = cur.fetchone()
            if not res:
                logger.info(f"Не работаем с {file_name_}")
                add_to_report(cur, file_name_, "Не работаем")
                con_close(cur, connection, file_name_, last_change_time)
                return
            if str(res[0]).upper() != 'ДА':
                logger.info(f"Не работаем с {file_name_}")
                add_to_report(cur, file_name_, "Не работаем")
                con_close(cur, connection, file_name_, last_change_time)
                return
            load_data_to_db(file_name, cur, path_to_exit2, error_counts)

            cur.execute(f"update res2 set ЦенаПотЦенаБ = Цена_поставщика_с_издержками/base_price.ЦенаБ, ЦенаБ = base_price.ЦенаБ "
                        f"from base_price where res2.Артикул = base_price.Артикул and res2.Бренд = base_price.Бренд "
                        f"and Код_поставщика = '{file_name_}'")
            cur.execute(f"select count(*) from res2 where ЦенаПотЦенаБ < 1 and Код_поставщика = '{file_name_}'")
            cnt = cur.fetchone()[0]
            if cnt > 0:
                logger_report.info(f"{file_name_}: {cnt} записей (Цена менее ЦенаБ)")

            cur.execute(f"select К_Превышения_базовой_цены from Настройки_прайса_поставщика where Код_прайса = '{file_name_}'")
            K_over_price = cur.fetchone()[0]
            cur.execute(f"update res2 set Превышение_базовой_цены = ЦенаПотЦенаБ/{K_over_price} "
                        f"where ЦенаПотЦенаБ > {K_over_price} and Код_поставщика = '{file_name_}'")

            if not check_change_percent(cur, file_name_):
                logger.info(f"Превышение допустимого процента изменения кол-ва строк {file_name_}")
                add_to_report(cur, file_name_, "Превышение допустимого процента изменения кол-ва строк")
                con_close(cur, connection, file_name_, last_change_time)
                return
            if not check_change_price(cur, file_name_):
                logger.info(f"Превышение допустимого процента изменения цены {file_name_}")
                add_to_report(cur, file_name_, "Превышение допустимого процента изменения цены")
                con_close(cur, connection, file_name_, last_change_time)
                return

            cur.execute(f"update res2 set Исключить = 'Недопустимое количество или цена' "
                        f"where (Количество < 1 or Цена_поставщика_с_издержками <= 0) and Код_поставщика = '{file_name_}'")
            cur.execute(f"update res2 set Исключить = 'Пустой артикул' "
                        f"where (Артикул is NULL or Артикул = '') and Код_поставщика = '{file_name_}'")
            cur.execute(f"update res2 set Исключить = 'Разрешение на продажу: НИКОМУ' "
                        f"where Разрешение_на_продажу = 'НИКОМУ' and Код_поставщика = '{file_name_}'")

            cur.execute(f"update res2 set Исключить = 'Превышение ЦеныБ' where Превышение_базовой_цены is not NULL and Код_поставщика = '{file_name_}'")

            remove_rep2(cur, file_name_)

            grad(cur, file_name_)

            cur.execute(f"update res2 set Предложений_в_опте = mass_offers.Предложений_в_опте from mass_offers "
                        f"where res2.Артикул = mass_offers.Артикул and res2.Бренд = mass_offers.Бренд "
                        f"and Исключить is NULL and Код_поставщика = '{file_name_}'")

            cur.execute(f"select Наценка_мин, Наценка_опт, Наценка_макс from Настройки_прайса_поставщика where Код_прайса = '{file_name_}'")
            markup_min, markup_opt, markup_max = cur.fetchone()

            for i in (markup_min, markup_opt, markup_max):
                if not isinstance(i, (int, float)):
                    logger.info(f"Некорректные наценки для {file_name_}")
                    add_to_report(cur, file_name_, "Некорректные наценки")
                    con_close(cur, connection, file_name_, last_change_time)
                    return
                if i < 0:
                    logger.info(f"Некорректные наценки для {file_name_}")
                    add_to_report(cur, file_name_, "Некорректные наценки")
                    con_close(cur, connection, file_name_, last_change_time)
                    return

            cur.execute(f"update res2 set Цена_с_наценкой = Цена_поставщика_с_издержками * ({markup_min} + (({markup_opt} - {markup_min}) * Градация/100) + 1) "
                        f"where Предложений_в_опте > 2 and Градация > 0 and Код_поставщика = '{file_name_}' and Исключить is NULL")
            cur.execute(f"update res2 set Цена_с_наценкой = Цена_поставщика_с_издержками * ({markup_min} + (({markup_max} - {markup_min}) * Градация/100) + 1) "
                        f"where Цена_с_наценкой is NULL and Градация > 0 and Код_поставщика = '{file_name_}' and Исключить is NULL")
            cur.execute(f"update res2 set Цена_с_наценкой = Цена_поставщика_с_издержками "
                        f"where Градация = 0 and Код_поставщика = '{file_name_}' and Исключить is NULL")

            set_multiplicity(cur, file_name_, error_counts)

        connection.commit()
        connection.close()

        # создание csv файла на выход 3
        req = """SELECT res2.КлючП as "КлючП", res2.АртикулП as "АртикулП", res2.БрендП as "БрендП", 
                 res2.НаименованиеП as "НаименованиеП", res2.КоличествоП as "КоличествоП", res2.ЦенаП as "ЦенаП", 
                 res2.Валюта as "ВалютаП", res2.КратностьП as "КратностьП", res2.ПримечаниеП as "ПримечаниеП", 
                 res2.Артикул as "Артикул", res2.Бренд as "БрендН", res2.Бренд_заполнен as "Бренд заполнен", 
                 res2.Наименование as "Наименование", res2.Количество as "Количество", res2.Цена as "Цена закупки", 
                 res2.Кратность as "КратностьН", res2.Код_поставщика as "Код прайса", 
                 res2.Разрешение_на_продажу as "Разрешение на продажу проблемной позиции", 
                 res2.Кратность_лота as "Кратность лота", res2.Цена_поставщика_с_издержками as "Цена поставщика с издержками", 
                 res2.ЦенаБ as "ЦенаБ", res2.ЦенаПотЦенаБ as "ЦенаП с издержками от ЦеныБ", 
                 res2.Исключить as "Причины исключения", res2.Градация as "Градация", res2.Предложений_в_опте as "Предложений в опте", 
                 res2.Цена_с_наценкой as "Цена с наценкой на прайс поставщика" FROM res2 
                 where Код_поставщика = '{}' and res2.Исключить is NULL ORDER BY id OFFSET {} LIMIT {}"""
        create_csv(file_name_, host, user, password, db_name, path_to_exit3, req, f"{file_name_}_3")

        # создание csv файла на выход 3 с позициями, где поле Исключить НЕ пустое
        req = """SELECT res2.КлючП as "КлючП", res2.АртикулП as "АртикулП", res2.БрендП as "БрендП", 
                         res2.НаименованиеП as "НаименованиеП", res2.КоличествоП as "КоличествоП", res2.ЦенаП as "ЦенаП", 
                         res2.Валюта as "ВалютаП", res2.КратностьП as "КратностьП", res2.ПримечаниеП as "ПримечаниеП", 
                         res2.Артикул as "Артикул", res2.Бренд as "БрендН", res2.Бренд_заполнен as "Бренд заполнен", 
                         res2.Наименование as "Наименование", res2.Количество as "Количество", res2.Цена as "Цена закупки", 
                         res2.Кратность as "КратностьН", res2.Код_поставщика as "Код прайса", 
                         res2.Разрешение_на_продажу as "Разрешение на продажу проблемной позиции", 
                         res2.Кратность_лота as "Кратность лота", res2.Цена_поставщика_с_издержками as "Цена поставщика с издержками", 
                         res2.ЦенаБ as "ЦенаБ", res2.ЦенаПотЦенаБ as "ЦенаП с издержками от ЦеныБ", 
                         res2.Исключить as "Причины исключения", res2.Градация as "Градация", res2.Предложений_в_опте as "Предложений в опте", 
                         res2.Цена_с_наценкой as "Цена с наценкой на прайс поставщика" FROM res2 
                         where Код_поставщика = '{}' and res2.Исключить is not NULL ORDER BY id OFFSET {} LIMIT {}"""
        create_csv(file_name_, host, user, password, db_name, path_to_exp, req, f"{file_name_}_исключение")

        # добавление обработанного файла в итоговую таблицу в БД
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            cur.execute(f"DELETE FROM total WHERE Код_поставщика = '{file_name_}'")
            cur.execute(f"insert into total(КлючП, АртикулП, БрендП, НаименованиеП, КоличествоП, ЦенаП, Валюта, КратностьП, "
                        f"ПримечаниеП, Артикул, Бренд, Бренд_заполнен, Наименование, Количество, "
                        f"Цена, Кратность, Код_поставщика, Разрешение_на_продажу, Кратность_лота, Цена_поставщика_с_издержками, "
                        f"ЦенаБ, Исключить, Градация, Предложений_в_опте, Цена_с_наценкой) "
                        f"select КлючП, АртикулП, БрендП, НаименованиеП, КоличествоП, ЦенаП, Валюта, КратностьП, "
                        f"ПримечаниеП, Артикул, Бренд, Бренд_заполнен, Наименование, Количество, "
                        f"Цена, Кратность, Код_поставщика, Разрешение_на_продажу, Кратность_лота, Цена_поставщика_с_издержками, "
                        f"ЦенаБ, Исключить, Градация, Предложений_в_опте, Цена_с_наценкой from res2 where "
                        f"res2.Код_поставщика = '{file_name_}' and Исключить is NULL")

            # данные для отчёта
            cur.execute(f"update price_report set loaded_rows = (select count(*) from res2 "
                        f"where Код_поставщика = '{file_name_}' and Исключить is NULL) where code = '{file_name_}'")
            cur.execute(f"update price_report set unloaded_rows = (select count(*) from res2 "
                        f"where Код_поставщика = '{file_name_}' and Исключить is not NULL) where code = '{file_name_}'")

            cur.execute(f"DELETE FROM res2 WHERE Код_поставщика = '{file_name_}'")
            cur.execute(f"INSERT INTO Время_изменений_выход2 VALUES('{file_name_}', '{last_change_time}')")

            add_to_report(cur, file_name_, "Ок")
        connection.commit()
        connection.close()

        logger.info(f"{file_name_} is done")
    except Exception as ex:
        logger.error("error:", exc_info=ex)
        error_counts.value += 1

def add_to_report(cur, file_name_, reason):
    cur.execute(f"insert into price_report(code) values('{file_name_}') on conflict do nothing")
    cur.execute(f"update price_report set exit2 = '{reason}' where code = '{file_name_}'")
    cur.execute(f"update price_report set update_time = '{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}' where code = '{file_name_}'")
    if reason != "Ок":
        cur.execute(f"update price_report set loaded_rows = null, unloaded_rows = null where code = '{file_name_}'")

def con_close(cur, connection, file_name_, last_change_time):
    '''Закрытие соединения и занесение в БД информации о времени изменении файла'''
    cur.execute(f"INSERT INTO Время_изменений_выход2 VALUES('{file_name_}', '{last_change_time}')")
    connection.commit()
    connection.close()

def load_data_to_db(file_name, cur, path_to_exit2, error_counts):
    '''Загрузка данных в БД из csv файла на выходе 2'''
    loaded_rows = 1
    rows_limit = 100000
    while True:
        try:
            table = pd.read_csv(fr"{path_to_exit2}\{file_name}", header=None, sep=';',
                                encoding='windows-1251',
                                usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21], nrows=rows_limit, skiprows=loaded_rows,
                                encoding_errors='ignore')
            table_size = len(table)
        except pd.errors.EmptyDataError:
            break

        if not table_size:
            break
        loaded_rows += table_size

        req_text = (
            f"insert into res2(КлючП, АртикулП, БрендП, НаименованиеП, КоличествоП, ЦенаП, Валюта, КратностьП, ПримечаниеП, "
            f"Артикул, Бренд, Бренд_заполнен, Наименование, Количество, Цена, Кратность, Код_поставщика, Исключить, "
            f"Разрешение_на_продажу, Кратность_лота, Цена_поставщика_с_издержками) values")
        pool_req = req_text
        dgt_val = [4, 5, 7, 13, 14, 15, 19, 20]
        for v_id, content in enumerate(table.values):
            pool_req += '('
            for i in range(21):
                if i in dgt_val:
                    pool_req += f"{content[i]}, "
                else:
                    pool_req += f"{fix_str(content[i])}, "
            pool_req = pool_req[:-2]
            pool_req += '), '

            # отправка 500 объединённых запросов к БД за один раз
            if (v_id % 500 == 0 or v_id == table_size - 1) and v_id > 0:
                try:
                    pool_req = pool_req[:-2]
                    pool_req += "ON CONFLICT DO NOTHING;"
                    cur.execute(pool_req)
                    pool_req = req_text
                except Exception as ex1:
                    logger.error("insert_1 error:", exc_info=ex1)
                    error_counts.value += 1

def fix_str(s):
    '''Изменение строки для её корректной записи в БД'''
    if not isinstance(s, str):
        if math.isnan(s):
            return 'NULL'
    x1 = '\''
    x2 = '\'\''
    x3 = ";"
    return f"'{str(s).replace(x1, x2).replace(x3, ' ')}'"

def check_change_percent(cur, file_name_):
    '''Проверка изменения процента количества позиций в предыдущем прайсе (данные из общей таблицы total) и текущей версии прайса'''
    cur.execute(f"select count(*) from total where Код_поставщика = '{file_name_}'")
    n_rows = cur.fetchone()[0]
    if not n_rows:
        return True

    cur.execute(f"select count(*) from res2 where Код_поставщика = '{file_name_}'")
    n_rows2 = cur.fetchone()[0]
    cur.execute(f"select Процент_изменения_строк from Настройки_прайса_поставщика where Код_прайса = '{file_name_}'")
    perc = cur.fetchone()[0]
    perc *= 100
    real_pers = abs((n_rows2-n_rows)/(n_rows/100))

    if real_pers > perc:
        logger_report_over.info(f"{file_name_}: превышение кол-ва строк ({real_pers}%)")
        return False
    return True

def check_change_price(cur, file_name_):
    '''Проверка изменения процента цены каждой десятой позиций в предыдущем прайсе (данные из общей таблицы total) и текущей версии прайса'''
    cur.execute(f"select count(*) from total where Код_поставщика = '{file_name_}'")
    n_rows = cur.fetchone()[0]
    if not n_rows:
        return True

    cur.execute(f"insert into tmp_price_compare(Артикул, Бренд, Цена, Код_поставщика) "
                f"select АртикулП, БрендП, ЦенаП, '{file_name_}' from total where Код_поставщика = '{file_name_}'")
    cur.execute(f"delete from tmp_price_compare where id % 10 != 0 and Код_поставщика = '{file_name_}'")

    cur.execute(f"select avg(res2.Цена/tmp_price_compare.Цена) from res2, tmp_price_compare where "
                f"res2.Артикул = tmp_price_compare.Артикул and res2.Бренд = tmp_price_compare.Бренд "
                f"and res2.Код_поставщика = '{file_name_}' and res2.Код_поставщика = tmp_price_compare.Код_поставщика")
    real_pers = cur.fetchone()[0]
    real_pers = abs(real_pers - 1)

    cur.execute(f"select Процент_изменения_цены from Настройки_прайса_поставщика where Код_прайса = '{file_name_}'")
    perc = cur.fetchone()[0]
    cur.execute(f"delete from tmp_price_compare where Код_поставщика = '{file_name_}'")
    if real_pers > perc:
        logger_report_over.info(f"{file_name_}: превышение цены ({real_pers}%)")
        return False
    return True


# def remove_rep(cur, file_name_):
#     '''Удаление повторяющихся позиций (Артикул, Бренд_заполнен)'''
#     cur.execute(f"select Бренд_заполнен from res2 where Код_поставщика = '{file_name_}' and Исключить is NULL "
#                 f"group by Артикул, Бренд_заполнен HAVING COUNT(*) > 1")
#     rep_count = cur.fetchall()
#     if not rep_count:
#         return
#
#     logger.info(f"Удаление дублей {file_name_}...")
#     cur.execute(f"""select Артикул, Бренд_заполнен from res2 where Код_поставщика = '{file_name_}' and Исключить is NULL
#             group by Артикул, Бренд_заполнен HAVING COUNT(*) > 1""")
#     reps = cur.fetchall()
#     # print(reps)
#
#
#     step_count = 20
#     next_step = 20
#     total_reps = len(reps)
#     counter = 1
#     print(total_reps)
#     for art, brand in reps:
#         current_loaded_percent = int(counter / total_reps * 100)
#         counter += 1
#         if current_loaded_percent >= next_step:
#             logger.info(f"Процесс удаление дублей {file_name_}: {current_loaded_percent}%")
#             next_step += step_count
#
#         print(f"{art=} {brand=} {counter}/{total_reps}")
#         if art:
#             art = art.replace('\'', '\'\'')
#         if brand:
#             brand = brand.replace('\'', '\'\'')
#         # DEL для всех повторений
#         cur.execute(f"""update res2 as mainT set Исключить = 'DEL' from (select res2.id, res2.Артикул, res2.Бренд_заполнен from res2
#                 join (select Артикул, Бренд_заполнен, count(*) from res2 where Исключить is NULL and Код_поставщика = '{file_name_}'
#                 and Артикул = '{art}' and Бренд_заполнен = '{brand}' group by Артикул, Бренд_заполнен HAVING COUNT(*) > 1) as T
#                 on res2.Артикул = T.Артикул and res2.Бренд_заполнен = T.Бренд_заполнен and res2.Исключить is NULL and res2.Код_поставщика = '{file_name_}' and
#                 res2.Артикул = '{art}' and res2.Бренд_заполнен = '{brand}') as T2 where mainT.id = T2.id""")
#         # Убирается DEL в каждой группе повторения, если цена в группе минимальная
#         cur.execute(f"""update res2 set Исключить = NULL from (select Артикул, Бренд_заполнен, count(*), min(Цена_поставщика_с_издержками)
#                 as min_price from res2 where Исключить = 'DEL' and Код_поставщика = '{file_name_}' and Артикул = '{art}' and
#                 Бренд_заполнен = '{brand}' group by Артикул, Бренд_заполнен HAVING COUNT(*) > 1) as T where res2.Артикул = T.Артикул and
#                 res2.Бренд_заполнен = T.Бренд_заполнен and res2.Код_поставщика = '{file_name_}' and res2.Артикул = '{art}'
#                 and res2.Бренд_заполнен = '{brand}' and res2.Цена_поставщика_с_издержками = T.min_price""")
#         # Среди записей с убранным DEL ищутся записи не с максимальным кол-вом и на них устанавливается DEL
#         cur.execute(f"""update res2 as mainT set Исключить = 'DEL' from (select res2.id, res2.Артикул, res2.Бренд_заполнен,
#                 res2.Количество, res2.Цена_поставщика_с_издержками from res2 join (select Артикул, Бренд_заполнен, count(*) as cnt,
#                 max(Количество) as max_count, min(Цена_поставщика_с_издержками) as min_price from res2 where Исключить is NULL
#                 and Код_поставщика = '{file_name_}' and Артикул = '{art}' and Бренд_заполнен = '{brand}'
#                 group by Артикул, Бренд_заполнен HAVING COUNT(*) > 1) as T on res2.Артикул = T.Артикул and res2.Бренд_заполнен = T.Бренд_заполнен
#                 and res2.Количество != T.max_count and res2.Цена_поставщика_с_издержками = T.min_price
#                 and res2.Код_поставщика = '{file_name_}' and res2.Артикул = '{art}' and res2.Бренд_заполнен = '{brand}'
#                 and res2.Исключить is NULL) as T2 where mainT.id = T2.id""")
#         # В оставшихся группах, где совпадает мин. цена и макс. кол-вл, остаются лишь записи с максимальным id
#         cur.execute(f"""update res2 set Исключить = 'DEL' from (select res2.id, res2.Артикул, res2.Бренд_заполнен, res2.Количество,
#                 res2.Цена_поставщика_с_издержками from res2 join (select Артикул, Бренд_заполнен, count(*), max(id) as max_id from res2
#                 where Исключить is NULL and Код_поставщика = '{file_name_}' and Артикул = '{art}' and Бренд_заполнен = '{brand}'
#                 group by Артикул, Бренд_заполнен HAVING COUNT(*) > 1) as T on res2.id != T.max_id and res2.Артикул = T.Артикул
#                 and res2.Бренд_заполнен = T.Бренд_заполнен where res2.Исключить is NULL and Код_поставщика = '{file_name_}' and res2.Артикул = '{art}'
#                 and res2.Бренд_заполнен = '{brand}') as T2 where res2.id = T2.id""")
#     logger.info(f"Дубли удалены {file_name_}")

def remove_rep2(cur, file_name_):
    '''Удаление повторяющихся позиций (Артикул, Бренд_заполнен)'''
    cur.execute(f"select Бренд_заполнен from res2 where Код_поставщика = '{file_name_}' and Исключить is NULL "
                f"group by Артикул, Бренд_заполнен HAVING COUNT(*) > 1")
    rep_count = cur.fetchall()
    if not rep_count:
        return

    logger.info(f"Удаление дублей {file_name_}...")
    cur.execute(f"""select Артикул, Бренд_заполнен from res2 where Код_поставщика = '{file_name_}' and Исключить is NULL 
            group by Артикул, Бренд_заполнен HAVING COUNT(*) > 1""")
    reps = cur.fetchall()
    # print(reps)


    # step_count = 20
    # next_step = 20
    # total_reps = len(reps)
    # counter = 1
    # print(total_reps)
    for art, brand in reps:
        # current_loaded_percent = int(counter / total_reps * 100)
        # counter += 1
        # if current_loaded_percent >= next_step:
        #     logger.info(f"Процесс удаление дублей {file_name_}: {current_loaded_percent}%")
        #     next_step += step_count

        # print(f"{art=} {brand=} {counter}/{total_reps}")
        if art:
            art = art.replace('\'', '\'\'')
        if brand:
            brand = brand.replace('\'', '\'\'')
        # DEL для всех повторений
        cur.execute(f"""update res2 set Исключить = 'DEL' where Код_поставщика = '{file_name_}' and Исключить is NULL 
                    and Артикул = '{art}' and Бренд_заполнен = '{brand}'""")
        # Убирается DEL в каждой группе повторения, если цена в группе минимальная
        cur.execute(f"""update res2 set Исключить = NULL where Код_поставщика = '{file_name_}' and Исключить = 'DEL' 
                    and Артикул = '{art}' and Бренд_заполнен = '{brand}' and Цена_поставщика_с_издержками = 
                    (select min(Цена_поставщика_с_издержками) from res2 where Код_поставщика = '{file_name_}' and 
                    Исключить = 'DEL' and Артикул = '{art}' and Бренд_заполнен = '{brand}')""")
        # Среди записей с убранным DEL ищутся записи не с максимальным кол-вом и на них устанавливается DEL
        cur.execute(f"""update res2 set Исключить = 'DEL' where Код_поставщика = '{file_name_}' and Исключить is NULL
                    and Артикул = '{art}' and Бренд_заполнен = '{brand}' and Количество != (select max(Количество) 
                    from res2 where Код_поставщика = '{file_name_}' and Исключить is NULL and Артикул = '{art}' and Бренд_заполнен = '{brand}')""")
        # В оставшихся группах, где совпадает мин. цена и макс. кол-вл, остаются лишь записи с максимальным id
        cur.execute(f"""update res2 set Исключить = 'DEL' where Код_поставщика = '{file_name_}' and Исключить is NULL
                    and Артикул = '{art}' and Бренд_заполнен = '{brand}' and id != (select max(id) 
                    from res2 where Код_поставщика = '{file_name_}' and Исключить is NULL and Артикул = '{art}' and Бренд_заполнен = '{brand}')""")
    logger.info(f"Дубли удалены {file_name_}")

def grad(cur, file_name_):
    '''Расчёт градации'''
    cur.execute(f"select sum(Цена) from res2 where Код_поставщика = '{file_name_}' and Исключить is NULL and Цена > 0")
    total_price = cur.fetchone()[0]
    step = total_price / 100
    grad_limit = 100000
    loaded_rows = 0
    while True:
        cur.execute(f"select id, Цена from res2 where Код_поставщика = '{file_name_}' "
                    f"and Исключить is NULL and Цена > 0 order by Цена ASC limit {grad_limit} offset {loaded_rows}")
        res = cur.fetchall()
        if not res:
            break

        len_res = len(res)
        last_grad = int(total_price / step)
        pool_req = f"update res2 set Градация = {last_grad} where id in ("
        len_pool_req = 0
        for e_id, i in enumerate(res):
            total_price -= i[1]
            cur_grad = int(total_price / step)
            # отправка 500 объединённых запросов к БД за один раз
            if (e_id % 500 == 0 and e_id > 0 or cur_grad != last_grad) and len_pool_req > 0:
                pool_req = pool_req[:-2]
                pool_req += ')'
                cur.execute(pool_req)
                len_pool_req = 0
                last_grad = cur_grad
                pool_req = f"update res2 set Градация = {last_grad} where id in ("
            elif e_id == len_res - 1:
                pool_req += f"{i[0]})"
                cur.execute(pool_req)

            pool_req += f"{i[0]}, "
            len_pool_req += 1

        # if len_pool_req == 1:
        #     cur.execute(pool_req)

        loaded_rows += len_res

    cur.execute(f"update res2 set Градация = 99 where Градация > 99 and Код_поставщика = '{file_name_}'")
    cur.execute(f"update res2 set Градация = 0 where Код_поставщика = '{file_name_}' and Исключить is NULL and Градация is NULL")


def set_multiplicity(cur, file_name_, error_counts):
    '''Расчёт кратности'''
    cur.execute(f"select Лот_удобный_нам from Настройки_прайса_поставщика where Код_прайса = '{file_name_}'")
    min_price = Decimal(cur.fetchone()[0])

    limit = 100000
    loaded_rows = 0
    while True:
        cur.execute(
            f"select id, Количество, Цена_с_наценкой, Кратность_лота from res2 where Код_поставщика = '{file_name_}' and Исключить is NULL "
            f"order by id limit {limit} offset {loaded_rows}")
        res = cur.fetchall()
        if not res:
            break

        res_len = len(res)
        loaded_rows += res_len
        pool_req = ''
        pool_req_len = 0

        for r_id, i in enumerate(res):
            id, count, price, mult = i
            if price * mult < min_price:
                new_mult = math.ceil(min_price / price)
                if new_mult <= count:
                    pool_req += f"update res2 set Кратность_лота = {new_mult} where id = {id};"
                    pool_req_len += 1
                elif count > 0:
                    new_price = math.ceil(min_price / count)
                    pool_req += f"update res2 set Кратность_лота = {count}, Цена_с_наценкой = {new_price}  where id = {id};"
                    pool_req_len += 1

            # отправка 500 объединённых запросов к БД за один раз
            if (pool_req_len % 500 == 0 or r_id == res_len - 1) and pool_req_len > 0:
                try:
                    if pool_req:
                        cur.execute(pool_req)
                    pool_req = ''
                except Exception as ex1:
                    logger.error("update_rows error (set_multiplicity):", exc_info=ex1)
                    error_counts.value += 1

def create_csv(file_name_, host, user, password, db_name, path_to, req, new_name):
    '''Формирование csv файла'''
    limit = 100000

    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    df = pd.read_sql(req.format(file_name_, 0, limit), connection)
    df.to_csv(f"{path_to}/{new_name}.csv", sep=';', encoding='windows-1251', index=False, errors='ignore') # utf-8-sig, float_format="%.2f"

    loaded = limit
    while True:
        df = pd.read_sql(req.format(file_name_, loaded, limit), connection)
        if not len(df):
            break
        df.to_csv(f"{path_to}/{new_name}.csv", mode='a', sep=';', encoding="windows-1251", index=False, # utf-8-sig
                  header=False, errors='ignore')
        loaded += limit

    connection.close()
