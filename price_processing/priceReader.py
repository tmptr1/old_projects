'''
Преобразовывает скаченные прайсы с почты в прайсы одного шаблона.
Выход 1 -> Выход 2
'''
import time
import datetime
import pandas as pd
import numpy as np
import xlrd
from python_calamine.pandas import pandas_monkeypatch
import openpyxl
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QColor
import re
import sys
import os
import psycopg2
import math
from decimal import Decimal
import multiprocessing as mp
import logging
from logger import configure_logging
import holidays
import warnings
from info_module import info_module
warnings.filterwarnings('ignore')


logger = logging.getLogger(__name__)
configure_logging(logger, 'logs/price_reader.log')

logger_report = logging.getLogger('report')
configure_logging(logger_report, 'logs/Отчёт о просрочке.log')

MODULE_NUM = 1
InfoModule = None

host = ''
user = ''
password = ''
db_name = ''
path_to_prices = ''
path_to_catalogs = ''
path_to_exit2 = ''
char_limit = 256


class price_reader():
    headers = ['id', 'Файл', 'Пропуск сверху', 'Пропуск снизу', 'Сопоставление по']
    headers2 = ['id', 'R', 'C', 'Название ячейки', 'Тип проверки', 'Столбец', 'Новое значение']

    items_db = {0: ['Ключ1 поставщика', 'КлючП', 0], 1: ['Артикул поставщика', 'АртикулП', 0],
                    2: ['Бренд поставщика', 'БрендП', 0], 3: ['Наименование поставщика', 'НаименованиеП', 0],
                    4: ['Количество поставщика', 'КоличествоП', 1], 5: ['Цена поставщика', 'ЦенаП', 1],
                    6: ['Кратность поставщика', 'КратностьП', 1], 7: ['Примечание поставщика', 'ПримечаниеП', 0],
                    8: ['Валюта', 'Валюта', 0]}

    #КлючП, АртикулП, БрендП, НаименованиеП, КоличествоП, ЦенаП, КратностьП, ПримечаниеП, Валюта
    def __init__(self, cls):
        self.main_ui = cls
        global host, user, password, db_name, path_to_prices, path_to_catalogs, path_to_exit2, InfoModule
        InfoModule = info_module(cls, module_num=MODULE_NUM)
        host = self.main_ui.host
        user = self.main_ui.user
        password = self.main_ui.password
        db_name = self.main_ui.db_name
        path_to_prices = self.main_ui.Dir2
        path_to_catalogs = self.main_ui.path_to_catalogs
        path_to_exit2 = self.main_ui.path_to_exit2

        mp.freeze_support()
        pandas_monkeypatch()

        self.items = [self.items_db[i][0] for i in range(len(self.items_db))]

        # self.main_ui.FilesTable_3.setColumnCount(len(self.headers))
        # self.main_ui.FilesTable_3.setHorizontalHeaderLabels(self.headers)
        # self.main_ui.FilesTable_3.setColumnWidth(0, 40)
        # self.main_ui.FilesTable_3.setColumnWidth(1, 100)
        # self.main_ui.FilesTable_3.setColumnWidth(2, 60)
        # self.main_ui.FilesTable_3.setColumnWidth(3, 60)
        # self.main_ui.FilesTable_3.setColumnWidth(4, 200)
        #
        # self.main_ui.SettingsTable_3.setColumnCount(len(self.headers2))
        # self.main_ui.SettingsTable_3.setHorizontalHeaderLabels(self.headers2)
        # self.main_ui.SettingsTable_3.setColumnWidth(0, 30)
        # self.main_ui.SettingsTable_3.setColumnWidth(1, 20)
        # self.main_ui.SettingsTable_3.setColumnWidth(2, 20)
        # self.main_ui.SettingsTable_3.setColumnWidth(3, 120)
        # self.main_ui.SettingsTable_3.setColumnWidth(4, 90)
        # self.main_ui.SettingsTable_3.setColumnWidth(5, 60)
        # self.main_ui.SettingsTable_3.setColumnWidth(6, 200)
        #
        # self.main_ui.FilesTable_3.cellClicked.connect(self.ShowSettings)


    # def add_FilesTable(self):
    #     '''Добавление строки в таблицу [Правила загрузки]'''
    #     try:
    #         self.main_ui.FilesTable_3.cellChanged.disconnect(self.setWhiteRow)
    #     except:
    #         pass
    #     row_count = self.main_ui.FilesTable_3.rowCount()
    #     self.main_ui.FilesTable_3.setRowCount(row_count + 1)
    #     self.main_ui.FilesTable_3.selectRow(row_count)
    #
    #     tx = QtWidgets.QLabel('')
    #     self.main_ui.FilesTable_3.setCellWidget(row_count, 0, tx)
    #
    #     self.main_ui.FilesTable_3.setItem(row_count, 1, QTableWidgetItem(''))
    #
    #     sR = QtWidgets.QSpinBox()
    #     self.main_ui.FilesTable_3.setCellWidget(row_count, 2, sR)
    #     sR.valueChanged.connect(self.setWhiteRow)
    #
    #     sF = QtWidgets.QSpinBox()
    #     self.main_ui.FilesTable_3.setCellWidget(row_count, 3, sF)
    #     sF.valueChanged.connect(self.setWhiteRow)
    #
    #     cb = QtWidgets.QComboBox()
    #     cb.addItems(['Ключ', 'Артикул + Бренд', 'Артикул + Наименование'])
    #     self.main_ui.FilesTable_3.setCellWidget(row_count, 4, cb)
    #     cb.currentIndexChanged.connect(self.setWhiteRow)
    #
    #     self.main_ui.FilesTable_3.cellChanged.connect(self.setWhiteRow)

    # def preRemove(self):
    #     '''Подтверждение удаления строки'''
    #     MsgB = QMessageBox()
    #     MsgB.setWindowTitle('Удаление записи')
    #     MsgB.setText('Вы действительно хотите удалить запись?')
    #     MsgB.setIcon(QMessageBox.Question )
    #     MsgB.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    #     MsgB.setDefaultButton(QMessageBox.Yes)
    #     MsgB.buttonClicked.connect(self.Remove)
    #
    #     MsgB.exec_()

    # def Remove(self, btn):
    #     '''Удаление строки из таблицы [Правила загрузки]'''
    #     if btn.text() != '&Yes':
    #         return
    #     id = self.main_ui.FilesTable_3.cellWidget(self.main_ui.FilesTable_3.currentRow(), 0).text()
    #     if id:
    #         connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    #         with connection.cursor() as cur:
    #             cur.execute(f"DELETE FROM file_property WHERE id = '{id}'")
    #         connection.commit()
    #         connection.close()
    #     self.main_ui.FilesTable_3.removeRow(self.main_ui.FilesTable_3.currentRow())


    # def ShowSettings(self, *args):
    #     '''Загрузка данных в таблицу [Параметры загрузки] при выборе прайса в таблице [Правила загрузки]'''
    #     try:
    #         id = self.main_ui.FilesTable_3.cellWidget(args[0], 0).text()
    #         if id:
    #             try:
    #                 self.main_ui.SettingsTable_3.cellChanged.disconnect(self.setWhiteRow2)
    #             except:
    #                 pass
    #             connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    #             with connection.cursor() as cur:
    #                 cur.execute(f"SELECT file_name FROM file_property WHERE id = '{id}'")
    #                 name = cur.fetchone()
    #                 self.main_ui.label_3.setText(f'Параметры загрузки для {name[0]}:')
    #                 cur.execute(f"SELECT id_property, id_row, id_col, name, check_type, col, conv_col FROM headers WHERE id_property = '{id}'")
    #                 data = cur.fetchall()
    #             connection.close()
    #             self.main_ui.SettingsTable_3.clear()
    #             self.main_ui.SettingsTable_3.setHorizontalHeaderLabels(self.headers2)
    #
    #             self.main_ui.SettingsTable_3.setRowCount(len(data))
    #
    #             for r, d in enumerate(data):
    #                 tx = QtWidgets.QLabel(str(d[0]))
    #                 tx.setStyleSheet("padding-left: 2px; background-color: rgb(169, 252, 187);")
    #                 self.main_ui.SettingsTable_3.setCellWidget(r, 0, tx)
    #
    #                 self.main_ui.SettingsTable_3.setItem(r, 3, QTableWidgetItem(str(d[3])))
    #                 self.main_ui.SettingsTable_3.item(r, 3).setBackground(QColor(169, 252, 187))
    #
    #                 cb = QtWidgets.QComboBox()
    #                 cb.addItems(['Совпадает', 'Включает'])
    #                 cb.setCurrentIndex(int(d[4]))
    #                 self.main_ui.SettingsTable_3.setCellWidget(r, 4, cb)
    #                 cb.currentIndexChanged.connect(self.setWhiteRow2)
    #
    #                 cb2 = QtWidgets.QComboBox()
    #                 cb2.addItems(self.items)
    #                 cb2.setCurrentIndex(d[6])
    #                 self.main_ui.SettingsTable_3.setCellWidget(r, 6, cb2)
    #                 cb2.currentIndexChanged.connect(self.setWhiteRow2)
    #
    #                 for c in (1, 2, 5):
    #                     sb = QtWidgets.QSpinBox()
    #                     sb.setProperty("value", d[c])
    #                     self.main_ui.SettingsTable_3.setCellWidget(r, c, sb)
    #                     sb.valueChanged.connect(self.setWhiteRow2)
    #
    #             self.main_ui.SettingsTable_3.cellChanged.connect(self.setWhiteRow2)
    #     except Exception as ex:
    #         logger.error("ShowSettings error:", exc_info=ex)
    #         InfoModule.increase_error_count()

    # def add_SettingsTable(self):
    #     '''Добавление строки в таблицу [Параметры загрузки]'''
    #     try:
    #         self.main_ui.SettingsTable_3.cellChanged.disconnect(self.setWhiteRow2)
    #     except:
    #         pass
    #
    #     if self.main_ui.FilesTable_3.currentRow() == -1:
    #         return
    #     id = self.main_ui.FilesTable_3.cellWidget(self.main_ui.FilesTable_3.currentRow(), 0).text()
    #     if not id:
    #         return
    #
    #     row_count = self.main_ui.SettingsTable_3.rowCount()
    #     self.main_ui.SettingsTable_3.setRowCount(row_count + 1)
    #     self.main_ui.SettingsTable_3.selectRow(row_count)
    #
    #     tx = QtWidgets.QLabel(id)
    #     tx.setStyleSheet("padding-left: 2px;")
    #     self.main_ui.SettingsTable_3.setCellWidget(row_count, 0, tx)
    #
    #     self.main_ui.SettingsTable_3.setItem(row_count, 3, QTableWidgetItem(''))
    #
    #     cb = QtWidgets.QComboBox()
    #     cb.addItems(['Совпадает', 'Включает'])
    #     self.main_ui.SettingsTable_3.setCellWidget(row_count, 4, cb)
    #
    #     cb2 = QtWidgets.QComboBox()
    #     cb2.addItems(self.items)
    #     self.main_ui.SettingsTable_3.setCellWidget(row_count, 6, cb2)
    #
    #     for c in (1, 2, 5):
    #         sb = QtWidgets.QSpinBox()
    #         self.main_ui.SettingsTable_3.setCellWidget(row_count, c, sb)
    #
    #     self.main_ui.SettingsTable_3.cellChanged.connect(self.setWhiteRow2)


    # def remove_SettingsTable(self):
    #     self.main_ui.SettingsTable_3.removeRow(self.main_ui.SettingsTable_3.currentRow())

    # def save_SettingsTable(self):
    #     '''Сохранение данных в таблице [Параметры загрузки], проверка корректности заполненых полей'''
    #     try:
    #         if not self.main_ui.SettingsTable_3.rowCount():
    #             return
    #         try:
    #             self.main_ui.SettingsTable_3.cellChanged.disconnect(self.setWhiteRow2)
    #         except:
    #             pass
    #         id = self.main_ui.SettingsTable_3.cellWidget(0, 0).text()
    #         connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    #         with connection.cursor() as cur:
    #             cur.execute(f"DELETE FROM headers WHERE id_property = '{id}'")
    #             for r in range(self.main_ui.SettingsTable_3.rowCount()):
    #                 id_row = self.main_ui.SettingsTable_3.cellWidget(r, 1).value()
    #                 id_col = self.main_ui.SettingsTable_3.cellWidget(r, 2).value()
    #                 name = self.main_ui.SettingsTable_3.item(r, 3).text()
    #                 check_type = self.main_ui.SettingsTable_3.cellWidget(r, 4).currentIndex()
    #                 col = self.main_ui.SettingsTable_3.cellWidget(r, 5).value()
    #                 conv_col = self.main_ui.SettingsTable_3.cellWidget(r, 6).currentIndex()
    #
    #                 cur.execute(f"SELECT * FROM headers WHERE id_property = '{id}' AND col = {col}")
    #                 res = cur.fetchall()
    #                 cur.execute(f"SELECT * FROM headers WHERE id_property = '{id}' AND conv_col = {conv_col}")
    #                 res2 = cur.fetchall()
    #                 if res or res2:
    #                     logger.info(f"Повторяющийся столбец у записи {id} id ({id}, {id_row}, {id_col}, {name}, {check_type}, {col}, {conv_col})")
    #                     self.setRowColor2(r, 240, 120, 84)
    #                 else:
    #                     cur.execute(f"INSERT INTO headers VALUES('{id}', {id_row}, {id_col}, '{name}', {check_type}, {col}, {conv_col})")
    #                     self.setRowColor2(r, 169, 252, 187)
    #
    #         connection.commit()
    #         connection.close()
    #         logger.info(f"Настройки для записи {id} id сохранены")
    #         self.main_ui.SettingsTable_3.cellChanged.connect(self.setWhiteRow2)
    #     except Exception as ex:
    #         logger.error("save_SettingsTable error:", exc_info=ex)
    #         InfoModule.increase_error_count()

    # Перекраска строк в таблицах [Правила загрузки] и [Параметры загрузки]
    # Белый - при только что добавленной строке или ранее сохранённой строке, куда пользователь внёс изменения и не сохранил
    # Зелёный - сохранённая строка, данные которой подтянуты из БД
    # Красный - строка с ошибкой
    # def setWhiteRow(self, *args):
    #     self.setRowColor(self.main_ui.FilesTable_3.currentRow(), 255, 255, 255)

    # def setWhiteRow2(self, *args):
    #     self.setRowColor2(self.main_ui.SettingsTable_3.currentRow(), 255, 255, 255)


    # def setRowColor(self, row, r, g, b):
    #     self.main_ui.FilesTable_3.cellWidget(row, 0).setStyleSheet(f"background-color: rgb({r}, {g}, {b}); padding-left: 2px;")
    #     self.main_ui.FilesTable_3.item(row, 1).setBackground(QColor(r, g, b))

    # def setRowColor2(self, row, r, g, b):
    #     self.main_ui.SettingsTable_3.cellWidget(row, 0).setStyleSheet(f"background-color: rgb({r}, {g}, {b}); padding-left: 2px;")
    #     self.main_ui.SettingsTable_3.item(row, 3).setBackground(QColor(r, g, b))


    # def save(self):
    #     '''Сохранение всех строк в таблице [Параметры загрузки]'''
    #     try:
    #         logger.info('Сохранение...')
    #         connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    #         with connection.cursor() as cur:
    #
    #             try:
    #                 self.main_ui.FilesTable_3.cellChanged.disconnect(self.setWhiteRow)
    #             except:
    #                 pass
    #             for r in range(self.main_ui.FilesTable_3.rowCount()):
    #
    #                 isOk = True
    #                 id = self.main_ui.FilesTable_3.cellWidget(r, 0).text()
    #                 name = self.main_ui.FilesTable_3.item(r, 1).text()
    #                 skipR = self.main_ui.FilesTable_3.cellWidget(r, 2).value()
    #                 skipF = self.main_ui.FilesTable_3.cellWidget(r, 3).value()
    #                 check_type = self.main_ui.FilesTable_3.cellWidget(r, 4).currentIndex()
    #
    #                 if name == '':
    #                     isOk = False
    #
    #                 if isOk:
    #                     if id:
    #                         cur.execute(f"UPDATE file_property SET (file_name, skiprows, skipfooter, check_type) = "
    #                                     f"('{name}', {skipR}, {skipF}, {check_type}) WHERE id = '{id}'")
    #                     else:
    #                         cur.execute(f"INSERT INTO file_property (file_name, skiprows, skipfooter, check_type) "
    #                                     f"VALUES('{name}', {skipR}, {skipF}, {check_type}) RETURNING id")
    #                         id = cur.fetchone()
    #                         for col_num in range(1, 6):
    #                             cur.execute(f"insert into headers values('{id[0]}', 0, 0, '', 0, 0, {col_num})")
    #                         tx = QtWidgets.QLabel(str(id[0]))
    #                         self.main_ui.FilesTable_3.setCellWidget(r, 0, tx)
    #
    #                     self.setRowColor(r, 169, 252, 187)
    #                 else:
    #                     logger.info(f'Запись номер {r+1}: [{id, name, skipR, skipF}] заполнена некорректно')
    #                     self.setRowColor(r, 240, 120, 84)
    #
    #             self.main_ui.FilesTable_3.cellChanged.connect(self.setWhiteRow)
    #
    #         connection.commit()
    #         connection.close()
    #         logger.info('Сохранение завершено')
    #     except Exception as ex:
    #         logger.error("[save error]:", exc_info=ex)
    #         InfoModule.increase_error_count()

    def StartMainProc(self):
        '''Запуск основного цикла в отдельном потоке'''
        self.act = Action(self)
        self.t = QtCore.QThread()
        self.act.moveToThread(self.t)
        self.main_ui.Select_price_3.setEnabled(False)
        self.t.started.connect(self.act.mainCircle)
        self.act.finishSignal.connect(self.setOnStartButton)
        self.act.finishSignal.connect(self.setModuleStatusPause)

        self.main_ui.Module_status_2.setText("Работает")
        self.main_ui.Module_status_2.setStyleSheet(f"color: green;")
        self.t.start()
        self.t.quit()

    def setModuleStatusPause(self):
        self.main_ui.Module_status_2.setText("Пауза")
        self.main_ui.Module_status_2.setStyleSheet(f"color: red;")

    def setOnStartButton(self):
        self.main_ui.Select_price_3.setEnabled(True)

    # def load_db(self):
    #     '''Загрузка данных в таблицу [Правила загрузки]'''
    #     self.act2 = Action(self)
    #     self.t2 = QtCore.QThread()
    #     self.act2.moveToThread(self.t2)
    #     self.t2.started.connect(self.act2.load_db)
    #     self.act2.rowSignal.connect(self.set_up_row)
    #     self.act2.end_signal.connect(self.file_table_color_change_connect)
    #
    #     self.t2.start()
    #     self.t2.quit()

    # def set_up_row(self, r_id, id, name, up, down, compare):
    #     '''Заполнение строки в таблице [Правила загрузки]'''
    #     try:
    #         try:
    #             self.main_ui.FilesTable_3.cellChanged.disconnect(self.setWhiteRow)
    #         except:
    #             pass
    #
    #         tx = QtWidgets.QLabel(str(id))
    #         tx.setStyleSheet("padding-left: 2px;background-color: rgb(169, 252, 187);")
    #         self.main_ui.FilesTable_3.setCellWidget(r_id, 0, tx)
    #
    #         self.main_ui.FilesTable_3.setItem(r_id, 1, QTableWidgetItem(str(name)))
    #         self.main_ui.FilesTable_3.item(r_id, 1).setBackground(QColor(169, 252, 187))
    #
    #         sR = QtWidgets.QSpinBox()
    #         sR.setProperty("value", up)
    #         self.main_ui.FilesTable_3.setCellWidget(r_id, 2, sR)
    #         sR.valueChanged.connect(self.setWhiteRow)
    #
    #         sF = QtWidgets.QSpinBox()
    #         sF.setProperty("value", down)
    #         self.main_ui.FilesTable_3.setCellWidget(r_id, 3, sF)
    #         sF.valueChanged.connect(self.setWhiteRow)
    #
    #         cb = QtWidgets.QComboBox()
    #         cb.addItems(['Ключ', 'Артикул + Бренд', 'Артикул + Наименование'])
    #         cb.setCurrentIndex(int(compare))
    #         self.main_ui.FilesTable_3.setCellWidget(r_id, 4, cb)
    #         cb.currentIndexChanged.connect(self.setWhiteRow)
    #
    #         self.file_table_color_change_connect()
    #     except Exception as ex:
    #         logger.error("set_up_row error:", exc_info=ex)
    #         InfoModule.increase_error_count()

    # def file_table_color_change_connect(self):
    #     try:
    #         self.main_ui.FilesTable_3.cellChanged.disconnect(self.setWhiteRow)
    #     except:
    #         pass
    #     self.main_ui.FilesTable_3.cellChanged.connect(self.setWhiteRow)


class Action(QtCore.QThread):
    '''Класс для многопоточной работы в PyQt'''
    finishSignal = QtCore.pyqtSignal(int)
    rowSignal = QtCore.pyqtSignal(int, str, str, int, int, int)
    end_signal = QtCore.pyqtSignal()
    def __init__(self, mainApp=None):
        super(Action, self).__init__()
        self.mainApp = mainApp

    # def load_db(self):
    #     '''Заполняет талблицу [Правила загрузки] данными из БД'''
    #     try:
    #         connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    #         with connection.cursor() as cur:
    #             cur.execute(
    #                 "SELECT id, file_name, skiprows, skipfooter, check_type FROM file_property ORDER BY file_name ASC")
    #             data = cur.fetchall()
    #         connection.close()
    #
    #         self.mainApp.main_ui.FilesTable_3.setRowCount(len(data))
    #
    #         for id, d in enumerate(data):
    #             self.rowSignal.emit(id, d[0], d[1], d[2], d[3], d[4])
    #
    #         self.end_signal.emit()
    #     except Exception as ex:
    #         logger.error("[load_db error]:", exc_info=ex)
    #         InfoModule.increase_error_count()

    def mainCircle(self):
        # try:
        #     table = pd.read_excel(r"D:\other\price_processing\mail_2\1APR Прайс Армтек Краснодар.xlsx", header=None,
        #                           engine='calamine', nrows=1)
        #     print(table)
        # except Exception as ex:
        #     print(ex)
        # return
        '''Основной цикц, проверяет наличие новых файлов скаченных из почты и запускает их обработку в несколько потоков'''
        wait_sec = 90
        # logs = ['logs/price_reader.log', 'logs/Отчёт о просрочке.log']
        # for l in logs:
        #     print(l, os.path.getsize(l) / 1048576)
        #     if os.path.getsize(l) / 1048576 > 19:
        #         os.rename(l, f"{l}.1")

        while True:
            now1 = datetime.datetime.now()
            if self.mainApp.main_ui.Pause_3.isChecked():
                self.mainApp.main_ui.Pause_3.setChecked(False)
                self.finishSignal.emit(1)
                return

            try:
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    # logger.info(f"")
                    # logger_report.info(f"")
                    InfoModule.set_update_time(MODULE_NUM, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    price_list = set()
                    # проверка времени последнего изменения файла и этой же информации в БД, при несовпадении обновляет прайс
                    for f in os.listdir(path_to_prices):
                        if f[0] == '~':
                            continue

                        file_name_ = f[:4] # первые 4 символа - код прайса
                        t = datetime.datetime.fromtimestamp(os.path.getmtime(fr"{path_to_prices}/{f}")).strftime("%Y-%m-%d %H:%M:%S")
                        # cur.execute(f"select Время_изменения from Время_изменений_почта where Название_файла = '{file_name_}'")
                        cur.execute(f"select Время_изменения from Время_изменений_почта where Полное_название = "
                                    f"'{f.replace('\'', '\'\'').replace(";", " ")}'")
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
                        fls.append([i, self.mainApp.items_db, host, user, password, db_name, path_to_prices, path_to_exit2, error_counts])
                    cur.execute(f"DELETE FROM pre_res")
                    cur.execute(f"ALTER SEQUENCE pre_res_id_seq restart 1")
                connection.commit()
                connection.close()

                threads = self.mainApp.main_ui.ThreadSpinBox_3.value()

                with (mp.Pool(processes=threads)) as p:
                    p.map(update_file, fls)
                InfoModule.increase_error_count(count=error_counts.value)

                # проверка на паузу
                now2 = datetime.datetime.now()
                if wait_sec > (now2 - now1).seconds:
                    for _ in range(wait_sec - (now2 - now1).seconds):
                        if self.mainApp.main_ui.Pause_3.isChecked():
                            self.mainApp.main_ui.Pause_3.setChecked(False)
                            self.finishSignal.emit(1)
                            return
                        time.sleep(1)

            except Exception as ex:
                logger.error("mainCircle error:", exc_info=ex)
                InfoModule.increase_error_count()
                time.sleep(5)

def update_file(args):
    '''Обработка сырого прайса до выхода 2'''
    try:
        file_name, items_db, host, user, password, db_name, path_to_prices, path_to_exit2, error_counts = args

        logger.info(f"{file_name} ...")

        file_name_ = file_name[:4]
        frmt = file_name.split('.')[-1]
        time_update = datetime.datetime.fromtimestamp(os.path.getmtime(fr"{path_to_prices}/{file_name}")).strftime("%Y-%m-%d %H:%M:%S")

        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            # cur.execute(f"DELETE FROM Время_изменений_почта WHERE Название_файла = '{file_name_}'")
            cur.execute(f"DELETE FROM Время_изменений_почта WHERE Полное_название = '{file_name.replace('\'', '\'\'').replace(";", " ")}'")

            cur.execute(f"select Стандартизируем from Настройки_прайса_поставщика where Код_прайса = '{file_name_}'")
            s = cur.fetchone()
            if s:
                if s[0] != 'ДА':
                    logger.info(f"Для прайса {file_name_} не указано сохранение")
                    add_to_report(cur, file_name_, "Не указано сохранение")
                    close_con(cur, file_name, file_name_, time_update, connection)
                    return
            else:
                logger.info(f"Для прайса {file_name_} не указано сохранение")
                add_to_report(cur, file_name_, "Не указано сохранение")
                close_con(cur, file_name, file_name_, time_update, connection)
                return

            if not check_price_time(cur, file_name, file_name_, path_to_prices):
                logger.info(f"Прайс {file_name_} не подходит по сроку обновления")
                add_to_report(cur, file_name_, "Не подходит по сроку обновления")

                close_con(cur, file_name, file_name_, time_update, connection)
                return
                # pass

            # new_compare_table_settings(cur, path_to_prices, file_name_, file_name, frmt, items_db)
            # return
            # res = compare_table_settings(cur, path_to_prices, file_name_, file_name, frmt, items_db)
            res = new_compare_table_settings(cur, path_to_prices, file_name_, file_name, frmt)
            # return
            if not res:
                logger.info(f"Для прайса {file_name_} нет подходящих настроек")
                logger_report.info(f"Для прайса {file_name_} нет подходящих настроек")
                add_to_report(cur, file_name_, "Нет подходящих настроек")
                close_con(cur, file_name, file_name_, time_update, connection)
                return

            skipR, skipF, check_type, m, conv_cols, digit_cols, brand_col, name_col, count_col = res

            conv_cols_list = ''
            for n, i in enumerate(conv_cols):
                conv_cols_list += f"{items_db[i][1]}, "

            conv_cols_list += "Код_поставщика"

            loaded_rows = skipR # пропускаются указанное кол-во строк
            r_limit = 100000
            method = None
            # обработка файла частями по r_limit строк за итерацию
            while True:
                if frmt in ('xls', 'xlsx'):
                    pandas_monkeypatch()

                    table = pd.DataFrame
                    try:
                        table = pd.read_excel(fr"{path_to_prices}\{file_name}", usecols=[*m], header=None,
                                              nrows=r_limit, skiprows=loaded_rows, engine='calamine')
                        method = 1
                    except:
                        pass

                    if table.empty and method != 1:
                        table = pd.read_excel(fr"{path_to_prices}\{file_name}", usecols=[*m], header=None, nrows=r_limit, skiprows=loaded_rows)


                elif frmt == 'csv':
                    try:
                        table = pd.read_csv(fr"{path_to_prices}\{file_name}", header=None, sep=';', encoding='windows-1251',
                                            usecols=[*m], nrows=r_limit, skiprows=loaded_rows, encoding_errors='ignore')
                    except pd.errors.EmptyDataError:
                        break
                table_size = len(table)
                if not table_size:
                    break

                loaded_rows += table_size

                # удаление последний строк в соотвествии с параметром "Пропуск снизу" (skipF)
                if table_size == r_limit:
                    if frmt in ('xls', 'xlsx'):
                        pandas_monkeypatch()
                        # last = pd.read_excel(fr"{path_to_prices}\{file_name}", usecols=[*m], header=None,
                        #                       nrows=skipF, skiprows=loaded_rows, engine='calamine')
                        last = pd.DataFrame
                        try:
                            last = pd.read_excel(fr"{path_to_prices}\{file_name}", usecols=[*m], header=None,
                                                 nrows=skipF, skiprows=loaded_rows, engine='calamine')
                        except:
                            pass
                        if last.empty:
                            last = pd.read_excel(fr"{path_to_prices}\{file_name}", usecols=[*m], header=None,
                                                 nrows=skipF, skiprows=loaded_rows)

                        last = len(last)
                    elif frmt == 'csv':
                        last = 0
                        try:
                            last_t = pd.read_csv(fr"{path_to_prices}\{file_name}", header=None, sep=';',
                                               encoding='windows-1251', usecols=[*m], nrows=skipF, skiprows=loaded_rows,
                                                 encoding_errors='ignore')
                            last = len(last_t)
                        except pd.errors.EmptyDataError:
                            pass

                    if last < skipF:
                        n = skipF - last
                        table = table[:-n]
                elif skipF:
                    table = table[:-skipF]

                load_rows_from_price_to_db(cur, table, digit_cols, brand_col, name_col, count_col, file_name_, conv_cols_list, error_counts, connection)

            logger.info(f"{file_name_} загружен в БД")

            catalog_compare(cur, file_name_, check_type)

            # Валюта
            cur.execute(f"update pre_res set Цена = ЦенаП * exchange_rate.rate from exchange_rate where "
                        f"Код_поставщика = '{file_name_}' and Цена is NULL and pre_res.Валюта is not NULL and "
                        f"upper(pre_res.Валюта) = exchange_rate.сode")
            # Отсальные цены
            cur.execute(f"update pre_res set Цена = ЦенаП where Код_поставщика = '{file_name_}' and Цена is NULL")

            exclude_marked(cur, file_name_, error_counts)

            cur.execute(
                f"update pre_res set Разрешение_на_продажу = Справочник_проблемных_товаров.Разрешение_покупателю "
                f"from Справочник_проблемных_товаров where pre_res.Код_поставщика = '{file_name_}' and "
                f"Справочник_проблемных_товаров.Код_прайса = '{file_name_}' and "
                f"Справочник_проблемных_товаров.Артикул = pre_res.Артикул and Справочник_проблемных_товаров.Бренд = pre_res.Бренд")

            cur.execute(
                f"update pre_res set Разрешение_на_продажу = Справочник_проблемных_товаров.Разрешение_покупателю "
                f"from Справочник_проблемных_товаров where pre_res.Код_поставщика = '{file_name_}' and "
                f"Справочник_проблемных_товаров.Код_прайса is not NULL and "
                f"Справочник_проблемных_товаров.Артикул = pre_res.Артикул and Справочник_проблемных_товаров.Бренд = pre_res.Бренд "
                f"and Разрешение_на_продажу is NULL")

            set_multiplicity(cur, file_name_, error_counts)

            # Цена поставщика с издержками
            cur.execute(f"select Издержки from Настройки_прайса_поставщика where Код_прайса = '{file_name_}'")
            costs = cur.fetchone()[0]
            cur.execute(f"update pre_res set Цена_поставщика_с_издержками = Цена * {costs} where Код_поставщика = '{file_name_}'")

        connection.commit()
        connection.close()

        req = """SELECT pre_res.КлючП as "КлючП", pre_res.АртикулП as "АртикулП", pre_res.БрендП as "БрендП", 
                     pre_res.НаименованиеП as "НаименованиеП", pre_res.КоличествоП as "КоличествоП", pre_res.ЦенаП as "ЦенаП", 
                     pre_res.Валюта as "ВалютаП", pre_res.КратностьП as "КратностьП", pre_res.ПримечаниеП as "ПримечаниеП", 
                     pre_res.Артикул as "Артикул", pre_res.Бренд as "БрендН", pre_res.Производитель_заполнен as "Бренд заполнен", 
                     pre_res.Наименование as "Наименование", pre_res.Количество as "Количество", pre_res.Цена as "Цена закупки", 
                     pre_res.Кратность as "КратностьН", pre_res.Код_поставщика as "Код прайса", pre_res.ИслючитьИзПрайса as "Исключить", 
                     pre_res.Разрешение_на_продажу as "Разрешение на продажу проблемной позиции", pre_res.Цена_Л as "Цена с учётом лота закупки", 
                     pre_res.Кратность_лота as "Кратность лота", pre_res.Цена_поставщика_с_издержками as "Цена поставщика с издержками" 
                     FROM pre_res where Код_поставщика = '{}' ORDER BY id OFFSET {} LIMIT {}"""

        create_csv(file_name_, host, user, password, db_name, path_to_exit2, req)

        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            cur.execute(f"DELETE FROM pre_res WHERE Код_поставщика = '{file_name_}'")
            # cur.execute(f"INSERT INTO Время_изменений_почта VALUES('{file_name_}', '{time_update}')")
            cur.execute(f"INSERT INTO Время_изменений_почта VALUES('{file_name.replace('\'', '\'\'').replace(";", " ")}', "
                        f"'{file_name_}', '{time_update}')")
            cur.execute(f"update price_report set loaded_rows = NULL, unloaded_rows = NULL where code = '{file_name_}'")
            add_to_report(cur, file_name_, "Ок")
        connection.commit()
        connection.close()

        logger.info(f"{file_name} готов")
    except Exception as ex:
        logger.error("update error:", exc_info=ex)
        error_counts.value += 1

def add_to_report(cur, file_name_, reason):
    # cur.execute(f"delete from price_report_1 where code = '{file_name_}'")
    cur.execute(f"insert into price_report(code) values('{file_name_}') on conflict do nothing")
    cur.execute(f"update price_report set exit1 = '{reason}' where code = '{file_name_}'")
    cur.execute(f"update price_report set update_time = '{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}' where code = '{file_name_}'")
    if reason != "Ок":
        cur.execute(f"update price_report set exit2 = '', loaded_rows = null, unloaded_rows = null where code = '{file_name_}'")


def close_con(cur, file_name, file_name_, time_update, connection):
    '''Закрытие соединения и занесение в БД информации о времени изменении файла'''
    cur.execute(f"INSERT INTO Время_изменений_почта VALUES('{file_name.replace('\'', '\'\'').replace(";", " ")}', '{file_name_}', '{time_update}')")
    connection.commit()
    connection.close()

def check_price_time(cur, file_name, file_name_, path_to_prices):
    '''Расчёт рабочих дней с последнего изменения прайса'''
    d1 = datetime.datetime.fromtimestamp(os.path.getmtime(fr"{path_to_prices}\{file_name}"))
    d2 = datetime.datetime.today()
    days = (d2 - d1)
    days = days.days + days.seconds / 86400

    if days > 50: # если прошло больше 50 дней, кол-во рабочих дней считается 'грубо'
        days -= (((d2 - d1) // 7) * 2).days
    else:
        tmp_d = d1
        for i in range(int(days)):  # расчёт рабочих дней
            tmp_d += datetime.timedelta(days=1)
            if tmp_d.weekday() in (5, 6):
                days -= 1

        holidays_list = holidays.RU(years=d2.year).items()
        date_list = set()
        for i in holidays_list:  # выборка праздников, которые НЕ выпадают на субботу/воскресенье
            if i[0].weekday() not in (5, 6):
                date_list.add(i[0])

        now = datetime.date.today()

        tmp_d = d1.date()
        for i in date_list:  # отнять праздники
            if tmp_d <= i and now >= i:
                days -= 1

    cur.execute(f"select Срок_обновление_не_более from Настройки_прайса_поставщика where Код_прайса = '{file_name_}'")
    days2 = cur.fetchone()
    if not days2:
        logger.info(f"Для прайса {file_name_} нет срока обновления")
        return 0
    if days > days2[0]:
        logger.info(f"{file_name_} не подходит по сроку обновления")
        logger_report.info(f"{file_name_} не подходит по сроку обновления")
        return 0
    return 1


def compare_table_settings(cur, path_to_prices, file_name_, file_name, frmt, items_db):
    '''Сверка сырого прайса и настроек для его обработки'''
    cur.execute(f"select id, skiprows, skipfooter, file_property.check_type, count(*) as cnt from file_property "
                f"join (select * from headers) as h on file_name = '{file_name_}' and file_property.id = h.id_property "
                f"group by id order by cnt desc")
    total_res = cur.fetchall()
    if not total_res:
        return 0
    isOk = False

    for res in total_res:
        id = res[0]
        skipR = res[1]
        skipF = res[2]
        check_type = res[3]
        max_cols = res[4]
        cur.execute(f"select id_row, id_col, name, check_type, col, conv_col from headers where id_property = '{id}'")
        res_h = cur.fetchall()
        if not res_h:
            logger.info(f"Нет настройки у прайса {file_name_} с id: {id}")
            continue
        m = [i[4] - 1 for i in res_h]
        max_rows_to_check = max([i[0] for i in res_h])
        max_cols_to_check = max([i[1] for i in res_h])

        if frmt in ('xls', 'xlsx'):
            pandas_monkeypatch()
            table = pd.read_excel(fr"{path_to_prices}\{file_name}", header=None, engine='calamine',
                                  nrows=max_rows_to_check)
        elif frmt == 'csv':
            table = pd.read_csv(fr"{path_to_prices}\{file_name}", header=None, sep=';', encoding='windows-1251',
                                nrows=max_rows_to_check, encoding_errors='ignore')
        else:
            logger.info(f"Неизвестный формат: {file_name}, ({frmt})")
            return 0

        if len(table.columns) < max_cols_to_check:
            continue

        cols = list()
        conv_cols = list()
        digit_set = set()

        br = False
        for n in res_h:
            if n[2]:
                if n[3] == '1':
                    if not n[2] in table.loc[n[0] - 1, n[1] - 1]:
                        logger.info(f"Не совпадает название ячейки {n[2]}, id: {id}")
                        br = True
                        break
                else:
                    if table.loc[n[0] - 1, n[1] - 1] != n[2]:
                        logger.info(f"Не совпадает название ячейки {n[2]}, id: {id}")
                        br = True
                        break

            cols.append(n[4] - 1)
            conv_cols.append(n[5])
            if items_db[n[5]][2]:
                digit_set.add(int(n[5]))

        if br == True:
            continue

        transposition = True
        while transposition:
            transposition = False
            for i in range(1, len(cols)):
                if cols[i - 1] > cols[i]:
                    cols[i - 1], cols[i] = cols[i], cols[i - 1]
                    conv_cols[i - 1], conv_cols[i] = conv_cols[i], conv_cols[i - 1]
                    transposition = True

        digit_cols = list()
        brand_col = None
        name_col = None
        count_col = None
        for i in range(len(cols)):
            if conv_cols[i] in digit_set:
                digit_cols.append(i)
            if conv_cols[i] == 2:
                brand_col = i
            elif conv_cols[i] == 3:
                name_col = i
            elif conv_cols[i] == 4:
                count_col = i

        isOk = True
        break

    if isOk: # если хотя бы одна настройка подошла
        # print(skipR, skipF, check_type, m, conv_cols, digit_cols, brand_col, name_col, count_col)
        # 1 1 0 [0, 1, 2, 3, 4, 5] [0, 2, 1, 3, 5, 4] [4, 5] 1 3 5
        return skipR, skipF, check_type, m, conv_cols, digit_cols, brand_col, name_col, count_col
    else:
        return 0

def new_compare_table_settings(cur, path_to_prices, file_name_, file_name, frmt):
    try:
        check_types = {'Ключ': 0, 'Артикул + Бренд': 1, 'Артикул + Наименование': 2}
        # items_db = {0: ['Ключ1 поставщика', 'КлючП', 0], 1: ['Артикул поставщика', 'АртикулП', 0],
        #             2: ['Бренд поставщика', 'БрендП', 0], 3: ['Наименование поставщика', 'НаименованиеП', 0],
        #             4: ['Количество поставщика', 'КоличествоП', 1], 5: ['Цена поставщика', 'ЦенаП', 1],
        #             6: ['Кратность поставщика', 'КратностьП', 1], 7: ['Примечание поставщика', 'ПримечаниеП', 0],
        #             8: ['Валюта', 'Валюта', 0]}
        dgt = [4, 5, 6]
        brand_c = 2
        name_c = 3
        count_c = 4

        cur.execute(f"select id from file_settings where Прайс = '{file_name_}'")
        total_res = cur.fetchall()
        if not total_res:
            return 0
        isOk = False
        for i in total_res:
            cur.execute(f"select Пропуск_сверху, Пропуск_снизу, Сопоставление_по ,Строка_КлючП, Столбец_КлючП, Название_КлючП, "
                        f"Строка_АртикулП, Столбец_АртикулП, Название_АртикулП, Строка_БрендП, Столбец_БрендП, Название_БрендП, "
                        f"Строка_НаименованиеП, Столбец_НаименованиеП, Название_НаименованиеП, Строка_КоличествоП, Столбец_КоличествоП, "
                        f"Название_КоличествоП, Строка_ЦенаП, Столбец_ЦенаП, Название_ЦенаП, Строка_КратностьП, Столбец_КратностьП, "
                        f"Название_КратностьП, Строка_ПримечаниеП, Столбец_ПримечаниеП, Название_ПримечаниеП, Строка_Валюта, "
                        f"Столбец_Валюта, Название_Валюта from file_settings where id = '{i[0]}'")
            skipR, skipF, check_type, *res = cur.fetchone()
            if not check_type:
                return 0
            check_type = check_types[check_type]
            # print(skipR, skipF, check_type)
            # cols = {"Key": [], "Article": [], "Brand": [], "Name": [], "Count": [], "Price": [], "Mult": [], "Note": [], "Currency": []}
            # for ind, k in enumerate(cols.keys()):
            #     cols[k] = res[(ind*3):((ind+1)*3)]
            max_rows_to_check = 1
            max_cols_to_check = 1
            m = []
            conv_cols = []
            digit_cols = []
            brand_c_return = None
            name_c_return = None
            count_c_return = None
            for k in range(9):
                r, c, name = res[(k*3):((k+1)*3)]
                # print(r, c, name)
                if c == 0 or c == None:
                    continue
                if r > max_rows_to_check: max_rows_to_check = r
                if c > max_cols_to_check: max_cols_to_check = c

                conv_cols.append(k)
                m.append(c - 1)
                if k in dgt:
                    digit_cols.append(c - 1)
                elif k == brand_c:
                    brand_c_return = c - 1
                elif k == name_c:
                    name_c_return = c - 1
                if k == count_c:
                    count_c_return = c - 1

            if frmt in ('xls', 'xlsx'):
                pandas_monkeypatch()
                table = pd.DataFrame
                try:
                    table = pd.read_excel(fr"{path_to_prices}\{file_name}", header=None, engine='calamine',
                                          nrows=max_rows_to_check)
                except:
                    pass
                if table.empty:
                    table = pd.read_excel(fr"{path_to_prices}\{file_name}", header=None, nrows=max_rows_to_check)

            elif frmt == 'csv':
                table = pd.read_csv(fr"{path_to_prices}\{file_name}", header=None, sep=';', encoding='windows-1251',
                                    nrows=max_rows_to_check, encoding_errors='ignore')
            else:
                logger.info(f"Неизвестный формат: {file_name}, ({frmt})")
                return 0

            if len(table.columns) < max_cols_to_check:
                continue

            bk = False # delete from Время_изменений_почта where Название_файла = '1ROS';

            for ind, k in enumerate(m):
                if not res[(conv_cols[ind]*3)+2]:
                    # print(res[conv_cols[ind]*3]-1, k, 'Empty')
                    continue
                # print(res[conv_cols[ind]*3]-1, k, f'({conv_cols[ind]*3})', table.loc[res[conv_cols[ind]*3]-1, k], res[(conv_cols[ind]*3)+2],
                #       res[(conv_cols[ind]*3)+2] in table.loc[res[conv_cols[ind]*3]-1, k])
                if not res[(conv_cols[ind]*3)+2] in table.loc[res[conv_cols[ind]*3]-1, k]:
                    bk = True
                    break
            if bk:
                continue
            # print(m)
            # print(conv_cols)
            # print(digit_cols)
            # print(brand_c_return, name_c_return, count_c_return)
            transposition = True
            while transposition:
                transposition = False
                for j in range(1, len(m)):
                    if m[j - 1] > m[j]:
                        m[j - 1], m[j] = m[j], m[j - 1]
                        conv_cols[j - 1], conv_cols[j] = conv_cols[j], conv_cols[j - 1]
                        transposition = True


            for ind, j in enumerate(m):
                for ind2, k in enumerate(digit_cols):
                    if k == j:
                        digit_cols[ind2] = ind
                        break
                if j == brand_c_return:
                    brand_c_return = ind
                elif j == name_c_return:
                    name_c_return = ind
                elif j == count_c_return:
                    count_c_return = ind

            # print(m)
            # print(conv_cols)
            # print(digit_cols)
            # print(brand_c_return, name_c_return, count_c_return)

            isOk = True
            break

        if isOk:  # если хотя бы одна настройка подошла
            # print(skipR, skipF, check_type, m, conv_cols, digit_cols, brand_c_return, name_c_return, count_c_return)
            # 1 1 0 [0, 1, 2, 3, 4, 5] [0, 2, 1, 3, 5, 4] [4, 5] 1 3 5
            # 1 0 0 [0, 1, 2, 3, 5, 6, 8] [0, 2, 1, 3, 6, 5, 4] [4, 5, 6] 1 3 6 (0 2 1 3 6 5 4)
            # по счёту - 1 3 6, при загрузке будет условно 1-2 2-5 ... 6-9
            # сортировка по conv_cols
            # понять тонкость переменных

            return skipR, skipF, check_type, m, conv_cols, digit_cols, brand_c_return, name_c_return, count_c_return
        else:
            return 0
    except Exception as comp_ex:
        logger.error("compare error:", exc_info=comp_ex)
        return 0



def compare_table_settings2(cur, path_to_prices, file_name_, file_name, frmt, items_db):
    '''Сверка сырого прайса и настроек для его обработки'''
    cur.execute(f"select id, skiprows, skipfooter, file_property.check_type, count(*) as cnt from file_property "
                f"join (select * from headers) as h on file_name = '{file_name_}' and file_property.id = h.id_property "
                f"group by id order by cnt desc")
    total_res = cur.fetchall()
    if not total_res:
        return 0
    isOk = False

    for res in total_res:
        id = res[0]
        skipR = res[1]
        skipF = res[2]
        check_type = res[3]
        max_cols = res[4]
        cur.execute(f"select id_row, id_col, name, check_type, col, conv_col from headers where id_property = '{id}'")
        res_h = cur.fetchall()
        if not res_h:
            logger.info(f"Нет настройки у прайса {file_name_} с id: {id}")
            continue
        m = [i[4] - 1 for i in res_h]
        max_rows_to_check = max([i[0] for i in res_h])
        max_cols_to_check = max([i[1] for i in res_h])

        if frmt in ('xls', 'xlsx'):
            pandas_monkeypatch()
            table = pd.read_excel(fr"{path_to_prices}\{file_name}", header=None, engine='calamine',
                                  nrows=max_rows_to_check)
        elif frmt == 'csv':
            table = pd.read_csv(fr"{path_to_prices}\{file_name}", header=None, sep=';', encoding='windows-1251',
                                nrows=max_rows_to_check, encoding_errors='ignore')
        else:
            logger.info(f"Неизвестный формат: {file_name}, ({frmt})")
            return 0

        if len(table.columns) < max_cols_to_check:
            continue

        cols = list()
        conv_cols = list()
        digit_set = set()

        br = False
        for n in res_h:
            if n[2]:
                if n[3] == '1':
                    if not n[2] in table.loc[n[0] - 1, n[1] - 1]:
                        logger.info(f"Не совпадает название ячейки {n[2]}, id: {id}")
                        br = True
                        break
                else:
                    if table.loc[n[0] - 1, n[1] - 1] != n[2]:
                        logger.info(f"Не совпадает название ячейки {n[2]}, id: {id}")
                        br = True
                        break

            cols.append(n[4] - 1)
            conv_cols.append(n[5])
            if items_db[n[5]][2]:
                digit_set.add(int(n[5]))

        if br == True:
            continue

        transposition = True
        while transposition:
            transposition = False
            for i in range(1, len(cols)):
                if cols[i - 1] > cols[i]:
                    cols[i - 1], cols[i] = cols[i], cols[i - 1]
                    conv_cols[i - 1], conv_cols[i] = conv_cols[i], conv_cols[i - 1]
                    transposition = True

        digit_cols = list()
        brand_col = None
        name_col = None
        count_col = None
        for i in range(len(cols)):
            if conv_cols[i] in digit_set:
                digit_cols.append(i)
            if conv_cols[i] == 2:
                brand_col = i
            elif conv_cols[i] == 3:
                name_col = i
            elif conv_cols[i] == 4:
                count_col = i

        isOk = True
        break

    if isOk: # если хотя бы одна настройка подошла
        return skipR, skipF, check_type, m, conv_cols, digit_cols, brand_col, name_col, count_col
    else:
        return 0

def exclude_marked(cur, file_name_, error_counts):
    '''Помечает позиции в прайсе в соответствии с [Справочник слов исключений]'''
    cur.execute(f"select Условие, Столбец_поиска, Текст from Справочник_слов_исключений where Код_прайса = '{file_name_}'")
    res = cur.fetchall()
    for i in res:
        try:
            if i[0] == "Содержит":
                text = f"Содержит {i[2]}"
                cur.execute(f"update pre_res set ИслючитьИзПрайса = '{text[:80]}' where Код_поставщика = '{file_name_}' and {i[1]} LIKE '%{i[2]}%'")
            elif i[0] == "Начинается":
                text = f"Начинается c {i[2]}"
                cur.execute(f"update pre_res set ИслючитьИзПрайса = '{text[:80]}' where Код_поставщика = '{file_name_}' and {i[1]} LIKE '{i[2]}%'")
            elif i[0] == "Не начинается с":
                text = f"Не начинается с {i[2]}"
                cur.execute(f"update pre_res set ИслючитьИзПрайса = '{text[:80]}' where Код_поставщика = '{file_name_}' and {i[1]} NOT LIKE '{i[2]}%'")
        except Exception as ex:
            logger.error("exclude_marked error:", exc_info=ex)
            error_counts.value += 1

def load_rows_from_price_to_db(cur, table, digit_cols, brand_col, name_col, count_col, file_name_, conv_cols_list, error_counts, conn):
    '''Загрузка данных из сырого прайса в БД, запросы на добавление данных в БД объединяются по 500 штук и разово отправляются'''
    table_size = len(table)
    pool_req = f"INSERT INTO pre_res({conv_cols_list}) VALUES"
    for v_id, row in enumerate(table.values):
        req = ''
        for id, r in enumerate(row):

            if id in digit_cols:  # digit_set:
                if not isinstance(r, str) and math.isnan(r):
                    req += f"0, "

                elif isinstance(r, str):
                    r = r.replace(',', '.')
                    if id == count_col:
                        d_list = re.findall(r'\d+', r)
                        if len(d_list) == 0:
                            r = '0'
                        elif len(d_list) >= 1:
                            r = d_list[0]
                    else:
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
                if id == brand_col:
                    r = str(r).upper()
                elif id == name_col:
                    r = r.replace('·', '').replace('°', '').replace('¶', '').replace('→', '').replace('¤', '')
                    r = ' '.join(r.split())
                req += f"'{r[:char_limit]}', "
            elif not isinstance(r, str):
                if math.isnan(r):
                    req += 'NULL, '
                else:
                    if id == brand_col:
                        r = str(r).upper()
                    elif id == name_col:
                        r = r.replace('·', '').replace('°', '').replace('¶', '').replace('→', '').replace('¤', '')
                        r = ' '.join(r.split())
                    req += f"'{str(r)[:char_limit]}', "
            else:
                req += 'NULL, '
        req += f"'{file_name_}'"
        pool_req += f"({req}), "

        # отправка 500 объединённых запросов к БД за один раз
        if (v_id % 500 == 0 or v_id == table_size - 1) and v_id > 0:
            try:
                pool_req = pool_req[:-2]
                pool_req += " ON CONFLICT DO NOTHING;"
                cur.execute(pool_req)
                # pool_req = f"INSERT INTO pre_res({conv_cols_list}) VALUES"
            except Exception as ex1:
                conn.rollback()
                logger.error("load_rows_from_price_to_db error:", exc_info=ex1)
                error_counts.value += 1
                return
            finally:
                pool_req = f"INSERT INTO pre_res({conv_cols_list}) VALUES"

def set_multiplicity(cur, file_name_, error_counts):
    '''Расчёт кратности'''
    cur.execute(f"select Лот_поставщика from Настройки_прайса_поставщика where Код_прайса = '{file_name_}'")
    min_price = Decimal(cur.fetchone()[0])

    cur.execute(f"update pre_res set Цена_Л = Цена, Кратность_лота = Кратность where Код_поставщика = '{file_name_}'")

    limit = 100000
    loaded_rows = 0
    while True:
        cur.execute(
            f"select id, Количество, Цена, Кратность from pre_res where Код_поставщика = '{file_name_}' "
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

            if price * mult < min_price and price > 0:
                new_mult = math.ceil(min_price / price)
                if new_mult <= count:
                    pool_req += f"update pre_res set Кратность_лота = {new_mult} where id = {id};"
                    pool_req_len += 1
                elif count > 0:
                    new_price = math.ceil(min_price / count)
                    pool_req += f"update pre_res set Кратность_лота = {count}, Цена_Л = {new_price} where id = {id};"
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

def catalog_compare(cur, file_name_, check_type):
    '''Сравнение позиций с [Справочник товаров поставщиков], сравнение Бренда со справочниками брендов'''
    types = {0: 'pre_res.КлючП is not NULL and pre_res.КлючП = Справочник_товаров_поставщиков.Ключ1',
             1: 'pre_res.АртикулП is not NULL and pre_res.АртикулП = Справочник_товаров_поставщиков.АртикулПоставщика and '
                'pre_res.БрендП is not NULL and pre_res.БрендП = Справочник_товаров_поставщиков.ПроизводительПоставщика',
             2: 'pre_res.АртикулП is not NULL and pre_res.АртикулП = Справочник_товаров_поставщиков.АртикулПоставщика and '
                'pre_res.НаименованиеП is not NULL and pre_res.НаименованиеП = Справочник_товаров_поставщиков.НаименованиеПоставщика'}
    check_type = types[check_type]
    cur.execute(f"update pre_res set Артикул = Справочник_товаров_поставщиков.Артикул, Бренд = Справочник_товаров_поставщиков.Производитель, "
                f"Наименование = Справочник_товаров_поставщиков.Наименование, Количество = Справочник_товаров_поставщиков.УбратьШтуки, "
                f"Цена = Справочник_товаров_поставщиков.ЦенаПоставщика, Кратность = Справочник_товаров_поставщиков.КратностьПоставщика, "
                f"Товарный_вид = Справочник_товаров_поставщиков.Товарный_вид, Запрет_продаж = Справочник_товаров_поставщиков.Запрет_продажи "
                f"from Справочник_товаров_поставщиков where Код_поставщика = '{file_name_}' and Справочник_товаров_поставщиков.Прайс = '{file_name_}' and {check_type}")

    cur.execute(f"update pre_res set Бренд = correct_brands.Наименование from correct_brands "
                f"where Код_поставщика = '{file_name_}' and Бренд IS NULL and БрендП = correct_brands.Наименование")
    cur.execute(f"update pre_res set Бренд = incorrect_brands.Правильное_наименование from incorrect_brands "
                f"where Код_поставщика = '{file_name_}' and Бренд IS NULL and БрендП = incorrect_brands.Некорректное_наименование")
    cur.execute(f"update pre_res set Бренд = incorrect_brands.Правильное_наименование from incorrect_brands where "
                f"Код_поставщика = '{file_name_}' and Бренд IS NULL and БрендП is NULL and incorrect_brands.Некорректное_наименование is NULL")

    cur.execute(f"update pre_res set Артикул = АртикулП where Код_поставщика = '{file_name_}' and Артикул is NULL")
    cur.execute(f"update pre_res set Наименование = НаименованиеП where Код_поставщика = '{file_name_}' and Наименование is NULL")
    cur.execute(f"update pre_res set Кратность = КратностьП where Код_поставщика = '{file_name_}' and Кратность is NULL")
    cur.execute(f"update pre_res set Кратность = 1 where Код_поставщика = '{file_name_}' and (Кратность is NULL or Кратность <= 0)")

    cur.execute(f"update pre_res set Количество = Количество - КоличествоП where Код_поставщика = '{file_name_}' and Количество is not NULL")
    cur.execute(f"update pre_res set Количество = КоличествоП where Код_поставщика = '{file_name_}' and Количество is NULL")

    cur.execute(f"update pre_res set Производитель_заполнен = Бренд where Код_поставщика = '{file_name_}' and Бренд is not NULL")
    cur.execute(f"update pre_res set Производитель_заполнен = БрендП where Код_поставщика = '{file_name_}' and Производитель_заполнен is NULL")


def create_csv(file_name_, host, user, password, db_name, path_to_exit2, req):
    '''Формирование csv файла с готовыми данными на Выход 2'''
    limit = 100000

    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    df = pd.read_sql(req.format(file_name_, 0, limit), connection)
    df.to_csv(f"{path_to_exit2}/{file_name_}.csv", sep=';', encoding='windows-1251', index=False, errors='ignore')

    loaded = limit
    while True:
        df = pd.read_sql(req.format(file_name_, loaded, limit), connection)
        if not len(df):
            break
        df.to_csv(f"{path_to_exit2}/{file_name_}.csv", mode='a', sep=';', encoding="windows-1251", index=False,
                  header=False, errors='ignore')
        loaded += limit

    connection.close()