import os
import time
import pandas as pd
import openpyxl
import datetime
import warnings
import psycopg2
from psycopg2 import errors
from sqlalchemy import create_engine
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
import smtplib
from email.header import Header
from email.mime.text import MIMEText

warnings.filterwarnings('ignore')
import sys
import csv
import shutil
import logging
from logging.handlers import RotatingFileHandler

import multiprocessing as mp

# logger = logging.getLogger(__name__)
# log_format = logging.Formatter("[%(asctime)s] %(module)7s:%(levelname)s - %(message)s",
#                                datefmt="%Y-%m-%d %H:%M:%S")
# handler = RotatingFileHandler('Logs.log', maxBytes=20 * 1024 * 1024, backupCount=2, errors='ignore')
# handler.setFormatter(log_format)
# logger.setLevel(logging.INFO)
# logger.addHandler(handler)


logger = mp.get_logger()
# logger = logging.getLogger('logs.log')
# q_handler = logging.handlers.QueueHandler()
logger.setLevel(21)
# logging.basicConfig(level=logging.INFO)
formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
# handler = logging.FileHandler('mult_logs.log')
f_handler = RotatingFileHandler('Logs.log', maxBytes=20 * 1024 * 1024, backupCount=2, errors='ignore',)
f_handler.setFormatter(formater)
s_handler = logging.StreamHandler()
s_handler.setFormatter(formater)

logger.addHandler(f_handler)
logger.addHandler(s_handler)

class Logs:
    def __init__(self, l):
        self.logget = l

    def add(self, text:str):
        self.logget.log(21, f"{text}")

    def error(self, exc, er_text):
        self.logget.error(f"{er_text}", exc_info=exc)

Log = Logs(logger)


# mail_login = ''
# mail_password = ''
mail_login = ""
mail_password = ""

unnecessary_fields_for_form = [8, 16, 19, 20, 24]
path_to_conditions = ''
path_to_files = ''
host = "127.0.0.1"
user = "postgres"
password = ""
db_name = ""
report_row_limit = 100_000
stop = False
autostart = False

db_url = None
engine = None

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(333, 394)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(17, 17, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Start = QtWidgets.QPushButton(self.centralwidget)
        self.Start.setObjectName("Start")
        self.verticalLayout.addWidget(self.Start)
        self.Pause = QtWidgets.QCheckBox(self.centralwidget)
        self.Pause.setObjectName("Pause")
        self.verticalLayout.addWidget(self.Pause)
        spacerItem1 = QtWidgets.QSpacerItem(17, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem1)
        self.Update = QtWidgets.QPushButton(self.centralwidget)
        self.Update.setObjectName("Update")
        self.verticalLayout.addWidget(self.Update)
        self.CheckContinue = QtWidgets.QCheckBox(self.centralwidget)
        self.CheckContinue.setObjectName("CheckContinue")
        self.verticalLayout.addWidget(self.CheckContinue)
        self.CheckForceUpdate = QtWidgets.QCheckBox(self.centralwidget)
        self.CheckForceUpdate.setObjectName("CheckForceUpdate")
        self.verticalLayout.addWidget(self.CheckForceUpdate)
        spacerItem2 = QtWidgets.QSpacerItem(17, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(17, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem4)
        self.ReportButton = QtWidgets.QPushButton(self.centralwidget)
        self.ReportButton.setObjectName("ReportButton")
        self.verticalLayout.addWidget(self.ReportButton)
        spacerItem5 = QtWidgets.QSpacerItem(17, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem5)
        self.CatalogsUpdateButton = QtWidgets.QPushButton(self.centralwidget)
        self.CatalogsUpdateButton.setObjectName("CatalogsUpdateButton")
        self.verticalLayout.addWidget(self.CatalogsUpdateButton)
        spacerItem6 = QtWidgets.QSpacerItem(17, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem6)
        self.PriceListButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.PriceListButton.setFont(font)
        self.PriceListButton.setObjectName("PriceListButton")
        self.verticalLayout.addWidget(self.PriceListButton)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 2, 1)
        spacerItem7 = QtWidgets.QSpacerItem(17, 17, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 1, 2, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(17, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout.addItem(spacerItem8, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 333, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # NEW
        self.spinBox.setProperty("value", 2)

        self.add_functions()
        self.Pause.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Start.setText(_translate("MainWindow", "Запуск"))
        self.Pause.setText(_translate("MainWindow", "Пауза"))
        self.Update.setText(_translate("MainWindow", "Принудительное обновление"))
        self.CheckContinue.setText(_translate("MainWindow", "Запуск после обновления"))
        self.CheckForceUpdate.setText(_translate("MainWindow", "Обнулить данные в БД"))
        self.label_2.setText(_translate("MainWindow", "Потоки"))
        self.ReportButton.setText(_translate("MainWindow", "Создание отчёта"))
        self.CatalogsUpdateButton.setText(_translate("MainWindow", "Обновить csv справочники"))
        self.PriceListButton.setText(_translate("MainWindow", "Создание итоговой таблицы"))

    def add_functions(self):
        self.Pause.clicked.connect(self.Stop)
        self.Start.clicked.connect(self.StartProcess)
        self.Update.clicked.connect(self.UpdateDB)
        self.ReportButton.clicked.connect(self.Create_report)
        self.PriceListButton.clicked.connect(self.Create_total_price_list)
        self.CatalogsUpdateButton.clicked.connect(self.Update_csv_catalogs)
        # self.RefreshButton.clicked.connect(self.RefreshTable_async) #RefreshTable)

        # AUTO START
        if os.path.exists('autostart.txt'): # autostart:#
            self.StartProcess()


    def Stop(self):
        global stop
        stop = not stop

    def UpdateDB(self):
        self.act = Action(self)
        self.act.startSignal.connect(self.setOffButtons)

        self.t = QtCore.QThread()
        self.act.moveToThread(self.t)
        self.t.started.connect(self.act.update)
        self.act.finishSignal.connect(self.t.quit)

        self.t.start()

        # if self.CheckContinue.isChecked() == True:
        self.act.finishSignal.connect(self.CheckContAfterUpdate)
        self.act.finishSignal.connect(self.setOnButtons)


    def CheckContAfterUpdate(self):
        if self.CheckContinue.isChecked():
            self.StartProcess()
    def StartProcess(self):
        self.act2 = Action(self)
        self.act2.startSignal.connect(self.setOffButtons)
        self.t2 = QtCore.QThread()
        self.act2.moveToThread(self.t2)
        self.t2.started.connect(self.act2.start)
        self.act2.finishSignal.connect(self.t2.quit)

        self.t2.start()
        self.act2.finishSignal.connect(self.setOnButtons)


    def Create_report(self):
        self.act3 = Action(self)
        self.act3.startSignal.connect(self.setOffReportButton)
        self.t3 = QtCore.QThread()
        self.act3.moveToThread(self.t3)
        self.t3.started.connect(self.act3.Create_report)
        self.act3.finishSignal.connect(self.t3.quit)

        self.t3.start()
        self.act3.finishSignal.connect(self.setOnReportButton)


    def Create_total_price_list(self):
        self.act4 = Action(self)
        self.act4.startSignal.connect(self.setOffPriceListButton)
        self.t4 = QtCore.QThread()
        self.act4.moveToThread(self.t4)
        self.t4.started.connect(self.act4.Create_price_list)
        self.act4.finishSignal.connect(self.t4.quit)

        self.t4.start()
        self.act4.finishSignal.connect(self.setOnPriceListButton)

    def Update_csv_catalogs(self):
        self.act5 = Action(self)
        self.act5.startSignal.connect(self.setOffCatalogsUpdateButton)
        self.t5 = QtCore.QThread()
        self.act5.moveToThread(self.t5)
        self.t5.started.connect(self.act5.Update_csv_catalogs)
        self.act5.finishSignal.connect(self.t5.quit)

        self.t5.start()
        self.act5.finishSignal.connect(self.setOnCatalogsUpdateButton)


    # def RefreshTable_async(self):
    #     self.act3 = Action(self)
    #     self.t3 = QtCore.QThread()
    #     self.act3.moveToThread(self.t3)
    #     self.t3.started.connect(self.act3.RefreshTable2)
    #     self.act3.finishSignal.connect(self.t3.quit)
    #
    #     self.t3.start()

    def setOffReportButton(self):
        self.ReportButton.setEnabled(False)

    def setOnReportButton(self):
        self.ReportButton.setEnabled(True)

    def setOffPriceListButton(self):
        self.PriceListButton.setEnabled(False)

    def setOnPriceListButton(self):
        self.PriceListButton.setEnabled(True)

    def setOffCatalogsUpdateButton(self):
        self.CatalogsUpdateButton.setEnabled(False)

    def setOnCatalogsUpdateButton(self):
        self.CatalogsUpdateButton.setEnabled(True)

    def setOffButtons(self):
        self.Start.setEnabled(False)
        self.Update.setEnabled(False)
        self.Pause.setEnabled(True)

    def setOnButtons(self):
        self.Start.setEnabled(True)
        self.Update.setEnabled(True)
        self.Pause.setEnabled(False)

    # def RefreshTable(self):
    #     try:
    #         connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    #         data = []
    #         with connection.cursor() as cur:
    #             # cur.execute("SELECT * FROM Время_изменений ORDER BY Название_файла ASC")
    #             cur.execute("SELECT Название_файла FROM Время_изменений WHERE Название_файла NOT LIKE '%Условия%' GROUP BY Название_файла ORDER BY Название_файла ASC")
    #             data = cur.fetchall()
    #             # print(data)
    #             prices_dict = dict()
    #             for i in data:
    #                 prices_dict[i[0]] = '-'
    #
    #             cur.execute("SELECT Название_файла, COUNT(*) FROM res GROUP BY Название_файла")
    #             data2 = cur.fetchall()
    #
    #             for i in data2:
    #                 prices_dict[i[0]] = i[1]
    #
    #         connection.close()
    #         headers = ['Файл', 'Кол-во записей']
    #
    #         self.tableWidget.setColumnCount(len(headers))
    #         self.tableWidget.setHorizontalHeaderLabels(headers)
    #         self.tableWidget.setColumnWidth(0, 100)
    #         self.tableWidget.setColumnWidth(1, 150)
    #         self.tableWidget.setRowCount(len(data))
    #
    #         for id, d in enumerate(prices_dict):
    #             self.tableWidget.setItem(id, 0, QTableWidgetItem(str(d)))
    #             self.tableWidget.setItem(id, 1, QTableWidgetItem(str(prices_dict[d])))
    #     except Exception as ex:
    #         print('tableWidget error:', ex)


class Action(QtCore.QObject):
    startSignal = QtCore.pyqtSignal(int)
    finishSignal = QtCore.pyqtSignal(int)
    wait_sec = 300
    loadValue = 0
    loadStep = 0

    def __init__(self, mainApp=None):
        super(Action, self).__init__()
        self.mainApp = mainApp
        self.dba = DBAction(mainApp)

    def start(self):
        global stop
        self.startSignal.emit(1)
        now = datetime.datetime.now()
        time_to_update = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=23)

        try:
            if self.dba.update_conditions():
                # time_to_update += datetime.timedelta(days=1)
                self.Update_csv_catalogs()
                self.dba.SilentUpdateConditions()
                # self.dba.force_global_update(not_all=True)
                self.dba.CreateTotal()
                self.dba.Check_files()
        except Exception as ex:
            # logger.error("start error:", exc_info=ex)
            # print(ex)
            Log.error(ex, "start ERROR")
            ex = input('Error')
            exit(0)

        while True:
            try:
                if stop == True:
                    # print(datetime.datetime.now().strftime(f"[%X]"), 'Пауза. Выход из цикла')
                    # logger.info('Пауза. Выход из цикла')
                    Log.add("Пауза. Выход из цикла")
                    self.finishSignal.emit(1)
                    self.mainApp.Pause.setChecked(False)
                    stop = False
                    return

                now = datetime.datetime.now()
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                res = None
                with connection.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM res")
                    res = int(*cur.fetchone())
                connection.close()
                # log_text = now.strftime(f"[%X] Кол-во записей: {res}")
                # Log.add(log_text)
                # print(now.strftime(f"[%X] Кол-во записей: {res}"))
                # logger.info(f"Кол-во записей: {res}")
                Log.add(f"Кол-во записей: {res}")

                if now > time_to_update:
                    time_to_update += datetime.timedelta(days=1)
                    if self.dba.update_conditions() or self.dba.CheckSilentUpdateConditions():
                        Log.add('Обновление.')

                        # logger.info('Обновление.')
                        self.Update_csv_catalogs()
                        self.dba.force_global_update(not_all=True)

                else:
                    if self.dba.update_conditions():
                        self.dba.SilentUpdateConditions()
                        # self.dba.force_global_update(not_all=True)
                        self.dba.CreateTotal()
                # Поиск новых прайсов
                self.dba.Check_files()

                now2 = datetime.datetime.now()
                if self.wait_sec > (now2 - now).seconds:
                    for s in range(self.wait_sec - (now2 - now).seconds):
                        time.sleep(1)
                        if stop == True:
                            # print(datetime.datetime.now().strftime(f"[%X]"), 'Пауза. Выход из цикла')
                            # logger.info('Пауза. Выход из цикла')
                            Log.add("Пауза. Выход из цикла")
                            self.finishSignal.emit(1)
                            self.mainApp.Pause.setChecked(False)
                            stop = False
                            return
            except Exception as ex:
                # logger.error("main circle error:", exc_info=ex)
                # print(datetime.datetime.now().strftime(f"[%X]"), "ERROR:", ex)
                Log.error(ex, "main circle ERROR")
            finally:
                self.finishSignal.emit(1)

    def update(self):
        self.startSignal.emit(1)
        try:
            self.dba.force_global_update(not_all=not self.mainApp.CheckForceUpdate.isChecked())
            self.dba.CreateTotal()
        except Exception as ex:
            # logger.error("update error:", exc_info=ex)
            # print(ex)
            Log.error(ex, "update ERROR")
        finally:
            self.finishSignal.emit(1)

    def Create_report(self):
        self.startSignal.emit(1)
        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            df = pd.read_sql(
                """select Название_файла as "Название файла", Инфо as "Кол-во записей/Статус", Время_загрузки as
                 "Дата изменения файла" from info_tab order by Название_файла""",
                connection)
            df.to_csv(f"Отчёт.csv", sep=';', encoding='windows-1251', index=False, errors='ignore')
            connection.close()
            Log.add("Отчёт сформирован")
        except Exception as ex:
            # logger.error("create report error:", exc_info=ex)
            # print('create report error:', ex)
            Log.error(ex, "create report ERROR")
        finally:
            self.finishSignal.emit(1)

    def Create_price_list(self, email=True):
        self.startSignal.emit(1)
        self.dba.CreateTotal()
        self.finishSignal.emit(1)


        # self.startSignal.emit(1)
        # Log.add("Формирование итогового прайса ...")
        # report_parts_count = 4
        # nt = datetime.datetime.now()
        # connection = None
        # try:
        #     connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        #     with connection.cursor() as cur:
        #         cur.execute(
        #             f"UPDATE res SET ШтР = Резерв_да.ШтР FROM Резерв_да WHERE res._09Код_Поставщик_Товар = Резерв_да._09Код")
        #
        #         cur.execute(f"UPDATE res SET Кол_во = _04Количество - ШтР")
        #
        #         cur.execute(f"update res set _06Кратность = 1 where _06Кратность is null")
        #
        #         cur.execute(f"update res set Кратность_меньше = '-' where Кол_во < _06Кратность")
        #
        #         cur.execute(f"update res set Разрешения_ПП = null where Разрешения_ПП = 'nan'")
        #         # cur.execute(f"UPDATE res SET ШтР = NULL WHERE ШтР = 0;")
        #         # cur.execute(f"UPDATE res SET Кол_во = _04Количество WHERE Низкая_цена IS NULL AND ШтР IS NULL")  # ШтР = ''
        #         # cur.execute(f"UPDATE res SET Кол_во = _04Количество - ШтР WHERE Низкая_цена IS NULL AND ШтР IS NOT NULL AND Кол_во IS NULL;")  # ШтР != '' AND Низкая_цена IS NULL
        #         # cur.execute(f"UPDATE res SET Кол_во = 0 WHERE Низкая_цена IS NOT NULL AND Низкая_цена < Макс_снижение_от_базовой_цены AND Кол_во IS NULL")
        #         # cur.execute(f"UPDATE res SET Кол_во = _04Количество WHERE Низкая_цена IS NOT NULL AND ШтР IS NULL AND Кол_во IS NULL")
        #         # cur.execute(f"UPDATE res SET Кол_во = _04Количество - ШтР WHERE Низкая_цена IS NOT NULL AND ШтР IS NOT NULL AND Кол_во IS NULL")
        #
        #         # cur.execute(
        #         #     f"UPDATE res SET Кратность_меньше = '-' WHERE Кол_во < GREATEST(_06Кратность_, _06Кратность)")
        #     # connection.commit()
        #     # connection.close()
        #
        #     # path = r'Итог.xlsx'
        #     # отчистка файла
        #     # df = pd.DataFrame()
        #     # df.to_excel(path, sheet_name="Результат1")
        #         path_to_res = r'pre Итог'
        #         for file in os.listdir(path_to_res):
        #             if file.startswith('Страница'):
        #                 os.remove(fr"{path_to_res}/{file}")
        #         file_csv = path_to_res + "/Страница {}.csv"
        #
        #         df = pd.DataFrame(columns=["Ключ1 поставщика", "Артикул поставщика", "Производитель поставщика", "Наименование поставщика",
        #             "Количество поставщика", "Цена поставщика", "Кратность поставщика", "Примечание поставщика", "01Артикул",
        #             "03Наименование", "05Цена", "06Кратность-", "07Код поставщика", "09Код + Поставщик + Товар", "10Оригинал",
        #             "13Градация", "14Производитель заполнен", "15КодТутОптТорг", "17КодУникальности", "18КороткоеНаименование",
        #             "19МинЦенаПоПрайсу", "20ИслючитьИзПрайса", "Отсрочка", "Продаём для ОС", "Наценка для ОС", "Наценка Р",
        #             "Наценка ПБ",  "Мин наценка", "Шаг градаци", "Шаг опт", "Разрешения ПП", "УбратьЗП", "Предложений опт",
        #             "ЦенаБ", "Кол-во", "Код ПБ_П", "06Кратность", "Кратность меньше", "05Цена+", "Количество закупок", "% Отгрузки",
        #             "Мин. Цена", "Мин. Поставщик"])
        #
        #         for i in range(1, report_parts_count+1):
        #             df.to_csv(file_csv.format(i), sep=';', decimal=',', encoding="windows-1251", index=False, errors='ignore')
        #
        #         row_limit = 100_000
        #         list_limit = 1_048_500
        #         loaded_rows = 0
        #         page_num = 1
        #         # header = True
        #         # sr = 0
        #
        #         # connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        #
        #         while True:
        #             if loaded_rows > 0:
        #                 if int(loaded_rows / list_limit) >= page_num:
        #                     page_num += 1
        #                     # header = True
        #                     # sr = 0
        #
        #                 # c = (list_limit * page_num) % (loaded_rows + row_limit)
        #                 new_row_limit = (list_limit * page_num) - loaded_rows if (list_limit * page_num) - loaded_rows < row_limit else row_limit
        #                 # a = (list_limit * page_num) % loaded_rows
        #                 # print(f"{a=}")
        #             else:
        #                 new_row_limit = row_limit
        #
        #             # df = pd.read_sql(f"""SELECT Ключ1_поставщика as "Ключ1 поставщика", Артикул_поставщика as "Артикул поставщика",
        #             # Производитель_поставщика as "Производитель поставщика", Наименование_поставщика as "Наименование поставщика",
        #             # Количество_поставщика as "Количество поставщика", Цена_поставщика as "Цена поставщика", Кратность_поставщика
        #             # as "Кратность поставщика", Примечание_поставщика as "Примечание поставщика", _01Артикул as "01Артикул",
        #             # _03Наименование as "03Наименование", _05Цена as "05Цена", _06Кратность as "06Кратность-", _07Код_поставщика
        #             # as "07Код поставщика", _09Код_Поставщик_Товар as "09Код + Поставщик + Товар", _10Оригинал as "10Оригинал",
        #             # _13Градация as "13Градация", _14Производитель_заполнен as "14Производитель заполнен", _15КодТутОптТорг as
        #             # "15КодТутОптТорг", _17КодУникальности as "17КодУникальности", _18КороткоеНаименование as "18КороткоеНаименование",
        #             # _19МинЦенаПоПрайсу as "19МинЦенаПоПрайсу", _20ИслючитьИзПрайса as "20ИслючитьИзПрайса", Отсрочка as "Отсрочка",
        #             # Продаём_для_ОС as "Продаём для ОС", Наценка_для_ОС as "Наценка для ОС", Наценка_Р as "Наценка Р", Наценка_ПБ
        #             # as "Наценка ПБ", Мин_наценка as "Мин наценка", Шаг_градаци as "Шаг градаци", Шаг_опт as "Шаг опт",
        #             # Разрешения_ПП as "Разрешения ПП", УбратьЗП as "УбратьЗП", Предложений_опт as "Предложений опт",
        #             # ЦенаБ as "ЦенаБ", Кол_во as "Кол-во", Код_ПБ_П as "Код ПБ_П", _06Кратность as "06Кратность",
        #             # Кратность_меньше as "Кратность меньше=", Кратность_меньше_ as "Кратность меньше", _05Цена_плюс as "05Цена+",
        #             # Количество_закупок as "Количество закупок", Процент_Отгрузки as "% Отгрузки"
        #             # from res ORDER BY _17КодУникальности OFFSET {loaded_rows} LIMIT {new_row_limit}""", connection)
        #
        #             df = pd.read_sql(f"""SELECT Ключ1_поставщика, Артикул_поставщика, Производитель_поставщика,
        #             Наименование_поставщика, Количество_поставщика, Цена_поставщика, Кратность_поставщика, Примечание_поставщика,
        #             _01Артикул, _03Наименование, _05Цена, _06Кратность, _07Код_поставщика , _09Код_Поставщик_Товар, _10Оригинал,
        #             _13Градация, _14Производитель_заполнен, _15КодТутОптТорг, _17КодУникальности, _18КороткоеНаименование,
        #             _19МинЦенаПоПрайсу, _20ИслючитьИзПрайса, Отсрочка, Продаём_для_ОС, Наценка_для_ОС, Наценка_Р, Наценка_ПБ,
        #             Мин_наценка, Шаг_градаци, Шаг_опт, Разрешения_ПП, УбратьЗП, Предложений_опт, ЦенаБ, Кол_во, Код_ПБ_П,
        #             _06Кратность, Кратность_меньше, _05Цена_плюс, Количество_закупок, Процент_Отгрузки, ЦенаМин, ЦенаМинПоставщик
        #             from res ORDER BY _17КодУникальности OFFSET {loaded_rows} LIMIT {new_row_limit}""", connection)
        #
        #             df_len = len(df)
        #             if not df_len:
        #                 break
        #
        #             # if sr == row_limit: # Вторая итерация. Чтобы пропустить header и не терялась одна позиция
        #             #     sr += 1
        #             loaded_rows += df_len
        #             # mode='w' if header else 'a'
        #             df.to_csv(file_csv.format(page_num), mode='a', sep=';', decimal=',', encoding="windows-1251",
        #                       index=False, header=False, errors='ignore') #  header=header,
        #         # with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        #         #     df.to_excel(writer, index=False, sheet_name=f"Результат{page_num}", startrow=sr, header=header)
        #         # sr += new_row_limit
        #
        #         # header = False
        #         connection.commit()
        #         connection.close()
        #
        #         for i in range(1, report_parts_count + 1):
        #             shutil.copy(fr"{path_to_res}/Страница {i}.csv", fr"Итог/Страница {i}.csv")
        #
        #         Log.add(f"Итоговый прайса готов! Общее время: {showTime(datetime.datetime.now() - nt)}")
        #
        #         # if email:
        #         send_email_report()
        #         Log.add(f"Письмо отправлено")
        #
        # except Exception as ex:
        #     # logger.error("create report error:", exc_info=ex)
        #     # print('create report error:', ex)
        #     Log.error(ex, "create report ERROR")
        # finally:
        #     try:
        #         if connection:
        #             connection.close()
        #     except:
        #         pass
        #     self.finishSignal.emit(1)

    # def RefreshTable2(self):
    #     try:
    #         connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    #         data = []
    #         with connection.cursor() as cur:
    #             # cur.execute("SELECT * FROM Время_изменений ORDER BY Название_файла ASC")
    #             cur.execute("SELECT Название_файла FROM Время_изменений WHERE Название_файла NOT LIKE '%Условия%' GROUP BY Название_файла ORDER BY Название_файла ASC")
    #             data = cur.fetchall()
    #             # print(data)
    #             prices_dict = dict()
    #             for i in data:
    #                 prices_dict[i[0]] = '-'
    #
    #             cur.execute("SELECT Название_файла, COUNT(*) FROM res GROUP BY Название_файла")
    #             data2 = cur.fetchall()
    #
    #             for i in data2:
    #                 prices_dict[i[0]] = i[1]
    #
    #         connection.close()
    #         headers = ['Файл', 'Кол-во записей']
    #
    #         self.mainApp.tableWidget.setColumnCount(len(headers))
    #         self.mainApp.tableWidget.setHorizontalHeaderLabels(headers)
    #         self.mainApp.tableWidget.setColumnWidth(0, 100)
    #         self.mainApp.tableWidget.setColumnWidth(1, 150)
    #         self.mainApp.tableWidget.setRowCount(len(data))
    #
    #         for id, d in enumerate(prices_dict):
    #             self.mainApp.tableWidget.setItem(id, 0, QTableWidgetItem(str(d)))
    #             self.mainApp.tableWidget.setItem(id, 1, QTableWidgetItem(str(prices_dict[d])))
    #     except Exception as ex:
    #         print('tableWidget error:', ex)
    def Update_csv_catalogs(self):
        self.startSignal.emit(1)
        try:
            Log.add("Формирование Справочник Базовая цена и Справочник Предложений в опте")
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cur:
                cur.execute("delete from base_price")
                cur.execute("delete from mass_offers")
            connection.commit()
            connection.close()

            # path_ = r"D:\other\price_processing\тз"
            path_ = r"\\Fileserver\рабочая папка\Работа с прайсами\4.0\обработка\справочники"
            for i in range(1, 5):
                df = pd.read_csv(
                    fr"{path_}\Справочник Базовая цена\Базовая цена - страница {i}.csv",
                    delimiter=';', encoding='windows-1251', header=0, index_col=False)
                if len(df):
                    df = df.rename(columns={"Мин. Цена": "ЦенаМин", "Мин. Поставщик": "ЦенаМинПоставщик"})
                    df.to_sql(name='base_price', con=engine, if_exists='append', index=False, index_label=False,
                              chunksize=10000)

                df = pd.read_csv(
                    fr"{path_}\Справочник Предложений в опте\Предложений в опте - страница {i}.csv",
                    delimiter=';', encoding='windows-1251', header=0, index_col=False)
                if len(df):
                    df = df.rename(columns={"Предложений в опте": "Предложений_в_опте"})
                    df.to_sql(name='mass_offers', con=engine, if_exists='append', index=False, index_label=False,
                              chunksize=10000)

            Log.add("Справочник Базовая цена и Справочник Предложений в опте сформированы!")
        except Exception as ex:
            # logger.error("create report error:", exc_info=ex)
            # print('Update_csv_catalogs error:', ex)
            Log.error(ex, "create report ERROR")
        finally:
            self.finishSignal.emit(1)


class DBAction():
    loadStep = 0

    def __init__(self, mainApp):
        self.mainApp = mainApp

    def force_global_update(self, not_all=False):
        # time_cond_edit = str(datetime.datetime.fromtimestamp(os.path.getmtime(path_to_conditions)))
        time_cond_edit = datetime.datetime.fromtimestamp(os.path.getmtime(path_to_conditions)).strftime(
            "%Y-%m-%d %H:%M:%S")
        conditions_file_name = path_to_conditions.split('\\')[-1]

        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            cur.execute("DELETE FROM Закупки_для_ОС")
            cur.execute("DELETE FROM data07")
            cur.execute("DELETE FROM data15")
            cur.execute("DELETE FROM data07_14")
            cur.execute("DELETE FROM data09")
            cur.execute("DELETE FROM Резерв_да")
            # cur.execute("DELETE FROM res")
            if not_all:
                cur.execute(f"DELETE FROM Время_изменений where Название_файла = '{conditions_file_name}'")
            else:
                cur.execute(f"DELETE FROM Время_изменений")
            cur.execute("UPDATE tmp SET val = '0' WHERE setting = 'SilentUpdateConditions'")
            cur.execute(f"INSERT INTO Время_изменений VALUES('{conditions_file_name}', '{time_cond_edit}')")

            cur.execute(f"select distinct(Название_файла) from res")
            files_in_db = cur.fetchall()
            if files_in_db:
                files_in_db = [i[0] for i in files_in_db]
                files_in_path = [f.split('.xlsx')[0] for f in os.listdir(path_to_files)]
                for f in files_in_db:
                    if f not in files_in_path:
                        cur.execute(f"DELETE FROM res where Название_файла = '{f}'")
        connection.commit()
        connection.close()

        Log.add('Обновление условий ...')

        nt = datetime.datetime.now()
        LoadToDBPandas(path_to_conditions, 'data07_14', sh='07&14Данные',
                       request="INSERT INTO {table} (Работаем, Период_обновления_не_более,"
                               " Настройка, Макс_снижение_от_базовой_цены, Правильное, Наценка_ПБ, Код_ПБ_П) "
                               "VALUES({row})",
                       cols=['Работаем?', 'Период обновления не более', 'Настройка', 'Макс снижение от базовой цены',
                             'Правильное', 'Наценка ПБ', 'Код ПБ_П'])
        LoadToDBPandas(path_to_conditions, 'data15', sh='15Данные',
                       request="INSERT INTO {table} (_15, Предложений_опт, ЦенаБ) VALUES({row})",
                       cols=['15', 'Предложений опт', 'ЦенаБ'])
        LoadToDBPandas(path_to_conditions, 'Резерв_да', sh='Резерв_да',
                       request="INSERT INTO {table} (_09Код, ШтР, _07Код) VALUES({row})",
                       cols=['09Код', 'ШтР', '07Код'])
        LoadToDBPandas(path_to_conditions, 'data09', sh='09Данные',
                       request="INSERT INTO {table} (УбратьЗП, ШтР, _09) VALUES({row})", cols=['УбратьЗП', 'ШтР', '09'])
        LoadToDBPandas(path_to_conditions, 'Закупки_для_ОС', sh='Закупки для ОС',
                       request="INSERT INTO {table} (Количество_закупок, АртикулПроизводитель) VALUES({row})",
                       cols=['Количество закупок', 'АртикулПроизводитель'])
        LoadToDBPandas(path_to_conditions, 'data07', sh='07Данные',
                       request="INSERT INTO {table} (Работаем, Период_обновления_не_более, Настройка, Отсрочка, Продаём_для_ОС, "
                               "Наценка_для_ОС, Макс_снижение_от_базовой_цены, Наценка_на_праздники_1_02, Наценка_Р, Мин_наценка, "
                               "Наценка_на_оптовые_товары, Шаг_градаци, Шаг_опт, Разрешения_ПП, Процент_Отгрузки) VALUES({row})",
                       cols=['Работаем?', 'Период обновления не более', 'Настройка', 'Отсрочка', 'Продаём для ОС',
                             'Наценка для ОС', 'Макс снижение от базовой цены', 'Наценка на праздники (1,02)',
                             'Наценка Р',
                             'Мин наценка', 'Наценка на оптовые товары', 'Шаг градаци', 'Шаг опт', 'Разрешения ПП',
                             '% Отгрузки'])

        Log.add(f"Загрузка условий {showTime(datetime.datetime.now() - nt)}")
        Log.add('Конец обновления')

        Log.add("Поиск новых данных ...")

        files = []  # { имя файла: время изменения }
        if not_all:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cur:
                cur.execute(f"select Название_файла from Время_изменений where Время_изменения < "
                            f"(select Время_изменения from Время_изменений where Название_файла = '{conditions_file_name}')")
                price_codes = cur.fetchall()
                for p in price_codes:
                    files.append(p[0])
            connection.commit()
            connection.close()

        else:
            tables = []
            for f in os.listdir(path_to_files):
                if '.xlsx' in f and f[0] != "~":
                    tables.append(path_to_files + f)

            for f in tables:
                files.append(f.split('.xlsx')[0].split('\\')[-1])
            # = datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M:%S")

            # print(files)
            new_files = set()
            # connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            # with connection.cursor() as cur:

            # s = ''
            for f in files:
                new_files.add(f)
                # s += f"'{f}', "
            # s = s.rstrip(', ')

            # cur.execute("SELECT * FROM Время_изменений")
            # edit_times_table = cur.fetchall()
            # edit_files = set()
            # files_in_db = set()
            # deleted_files = set()
            # for i in edit_times_table:
            #     code, edit_time = i
            #     # files_in_db.add(code)
            #     t = files.get(code, None)
            # if t == None:
            #     deleted_files.add(code)
            # elif edit_time != t:
            #     edit_files.add(code)

            # new_files = new_files - files_in_db

            # if path_to_conditions.split('\\')[-1] in deleted_files:
            #     deleted_files.remove(path_to_conditions.split('\\')[-1])

            # for i in deleted_files:
            #     cur.execute(f"DELETE FROM Время_изменений WHERE Название_файла = '{i}'")
            #     cur.execute(f"DELETE FROM res WHERE Название_файла = '{i}'")
            # for i in edit_files:
            #     cur.execute(f"UPDATE Время_изменений SET Время_изменения = '{files[i]}' WHERE Название_файла = '{i}'")
            # cur.execute(f"DELETE FROM res WHERE Название_файла = '{i}'")

            # for i in new_files:
            #     cur.execute(f"INSERT INTO Время_изменений VALUES('{i}', '{files[i]}')")
            # connection.commit()

            # new_files = new_files.union(edit_files)

        connection.close()

        threads = self.mainApp.spinBox.value()
        if files:
            Log.add(f'Загрузка новых данных... (используется потоков: {threads})')

        mng = mp.Manager()
        total = len(files)
        count = mng.Value('count', 0)
        fls = []
        for i in files:
            fls.append(
                [f"{path_to_files}{i}.xlsx", 'res', "INSERT INTO {table} (Ключ1_поставщика, Артикул_поставщика,"
                                                    "Производитель_поставщика, Наименование_поставщика, Количество_поставщика,"
                                                    "Цена_поставщика, Кратность_поставщика, Примечание_поставщика, _01Артикул, _02Производитель,"
                                                    "_03Наименование, _04Количество, _05Цена, _06Кратность_, _07Код_поставщика,"
                                                    "_09Код_Поставщик_Товар, _10Оригинал, _13Градация, _14Производитель_заполнен,"
                                                    "_15КодТутОптТорг, _17КодУникальности, _18КороткоеНаименование, _19МинЦенаПоПрайсу, _20ИслючитьИзПрайса,"
                                                    "Название_файла) VALUES({row})",
                 unnecessary_fields_for_form, count, total, password])

        pool_time = datetime.datetime.now()
        with (mp.Pool(processes=threads)) as p:
            p.map(LoadMulti, fls)
        if files:
            Log.add(f"Конец обновления. Общее время: {showTime(datetime.datetime.now() - pool_time)}")

        Log.add("Поиск новых данных закончен")

        A = Action()
        A.Create_price_list(email=False)

    # Проверяет записи на актуальность (добавление / изменение / удаление файлов)
    def Check_files(self):
        Log.add("Поиск новых данных ...")

        tables = []
        for f in os.listdir(path_to_files):
            if '.xlsx' in f and f[0] != "~":
                tables.append(path_to_files + f)

        files = dict()  # { имя файла: время изменения }
        for f in tables:
            files[f.split('.xlsx')[0].split('\\')[-1]] = datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime(
                "%Y-%m-%d %H:%M:%S")

        # print(files)
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            new_files = set()
            # s = ''
            for f in files:
                new_files.add(f)
                # s += f"'{f}', "
            # s = s.rstrip(', ')

            cur.execute("SELECT * FROM Время_изменений")
            edit_times_table = cur.fetchall()
            edit_files = set()
            files_in_db = set()
            deleted_files = set()
            for i in edit_times_table:
                code, edit_time = i
                files_in_db.add(code)
                t = files.get(code, None)
                if t == None:
                    deleted_files.add(code)
                elif edit_time != t:
                    edit_files.add(code)

            new_files = new_files - files_in_db

            if path_to_conditions.split('\\')[-1] in deleted_files:
                deleted_files.remove(path_to_conditions.split('\\')[-1])

            for i in deleted_files:
                cur.execute(f"DELETE FROM Время_изменений WHERE Название_файла = '{i}'")
                cur.execute(f"DELETE FROM res WHERE Название_файла = '{i}'")
            # for i in edit_files:
            #     cur.execute(f"UPDATE Время_изменений SET Время_изменения = '{files[i]}' WHERE Название_файла = '{i}'")
            # cur.execute(f"DELETE FROM res WHERE Название_файла = '{i}'")
            # for i in new_files:
            #     cur.execute(f"INSERT INTO Время_изменений VALUES('{i}', '{files[i]}')")
            connection.commit()

            new_files = new_files.union(edit_files)
            # print('расчёт', new_files)

            threads = self.mainApp.spinBox.value()
            if new_files:
                Log.add(f'Загрузка новых данных... (используется потоков: {threads})')

            mng = mp.Manager()
            total = len(new_files)
            count = mng.Value('count', 0)
            fls = []
            for i in new_files:
                fls.append(
                    [f"{path_to_files}{i}.xlsx", 'res', "INSERT INTO {table} (Ключ1_поставщика, Артикул_поставщика,"
                                                        "Производитель_поставщика, Наименование_поставщика, Количество_поставщика,"
                                                        "Цена_поставщика, Кратность_поставщика, Примечание_поставщика, _01Артикул, _02Производитель,"
                                                        "_03Наименование, _04Количество, _05Цена, _06Кратность_, _07Код_поставщика,"
                                                        "_09Код_Поставщик_Товар, _10Оригинал, _13Градация, _14Производитель_заполнен,"
                                                        "_15КодТутОптТорг, _17КодУникальности, _18КороткоеНаименование, _19МинЦенаПоПрайсу, _20ИслючитьИзПрайса,"
                                                        "Название_файла) VALUES({row})",
                     unnecessary_fields_for_form, count, total, password])

            pool_time = datetime.datetime.now()
            with (mp.Pool(processes=threads)) as p:
                p.map(LoadMulti, fls)
            if new_files:
                Log.add(f"Конец обновления. Общее время: {showTime(datetime.datetime.now() - pool_time)}")

        connection.close()
        Log.add("Поиск новых данных закончен")

    def update_conditions(self):
        # time_cond_edit = str(datetime.datetime.fromtimestamp(os.path.getmtime(path_to_conditions)))
        time_cond_edit = datetime.datetime.fromtimestamp(os.path.getmtime(path_to_conditions)).strftime(
            "%Y-%m-%d %H:%M:%S")
        conditions_file_name = path_to_conditions.split('\\')[-1]
        Log.add(f"Проверка '{conditions_file_name}'")

        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            cur.execute(f"SELECT Время_изменения FROM Время_изменений WHERE Название_файла = '{conditions_file_name}'")
            res = cur.fetchone()
            t = str(*res) if res else None
            connection.commit()
            connection.close()

            if t == None or time_cond_edit != t:
                return True
        return False

    def SilentUpdateConditions(self):
        # time_cond_edit = str(datetime.datetime.fromtimestamp(os.path.getmtime(path_to_conditions))) 2025-06-17 16:26:13
        time_cond_edit1 = datetime.datetime.fromtimestamp(os.path.getmtime(path_to_conditions)).strftime(
            "%Y-%m-%d %H:%M:%S")
        conditions_file_name = path_to_conditions.split('\\')[-1]
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            Log.add(f"Обновление '{conditions_file_name}' ... (без полного обновления прайсов)")
            nt = datetime.datetime.now()
            cur.execute("UPDATE tmp SET val = '1' WHERE setting = 'SilentUpdateConditions'")
            cur.execute(f"DELETE FROM Время_изменений WHERE Название_файла = '{conditions_file_name}'")

            cur.execute("DELETE FROM Закупки_для_ОС")
            cur.execute("DELETE FROM data07")
            cur.execute("DELETE FROM data15")
            cur.execute("DELETE FROM data07_14")
            cur.execute("DELETE FROM data09")
            cur.execute("DELETE FROM Резерв_да")
            cur.execute(f"INSERT INTO Время_изменений VALUES('{conditions_file_name}', '{time_cond_edit1}')")
        connection.commit()
        # with connection.cursor() as cur:
        LoadToDBPandasSilent(path_to_conditions, 'data07_14', connection, sh='07&14Данные',
                             request="INSERT INTO {table} (Работаем, Период_обновления_не_более,"
                                     " Настройка, Макс_снижение_от_базовой_цены, Правильное, Наценка_ПБ, Код_ПБ_П) "
                                     "VALUES({row})",
                             cols=['Работаем?', 'Период обновления не более', 'Настройка',
                                   'Макс снижение от базовой цены',
                                   'Правильное', 'Наценка ПБ', 'Код ПБ_П'])
        LoadToDBPandasSilent(path_to_conditions, 'data15', connection, sh='15Данные',
                             request="INSERT INTO {table} (_15, Предложений_опт, ЦенаБ) VALUES({row})",
                             cols=['15', 'Предложений опт', 'ЦенаБ'])
        LoadToDBPandasSilent(path_to_conditions, 'Резерв_да', connection, sh='Резерв_да',
                             request="INSERT INTO {table} (_09Код, ШтР, _07Код) VALUES({row})",
                             cols=['09Код', 'ШтР', '07Код'])
        LoadToDBPandasSilent(path_to_conditions, 'data09', connection, sh='09Данные',
                             request="INSERT INTO {table} (УбратьЗП, ШтР, _09) VALUES({row})",
                             cols=['УбратьЗП', 'ШтР', '09'])
        LoadToDBPandasSilent(path_to_conditions, 'Закупки_для_ОС', connection, sh='Закупки для ОС',
                             request="INSERT INTO {table} (Количество_закупок, АртикулПроизводитель) VALUES({row})",
                             cols=['Количество закупок', 'АртикулПроизводитель'])
        LoadToDBPandasSilent(path_to_conditions, 'data07', connection, sh='07Данные',
                             request="INSERT INTO {table} (Работаем, Период_обновления_не_более, Настройка, Отсрочка, Продаём_для_ОС, "
                                     "Наценка_для_ОС, Макс_снижение_от_базовой_цены, Наценка_на_праздники_1_02, Наценка_Р, Мин_наценка, "
                                     "Наценка_на_оптовые_товары, Шаг_градаци, Шаг_опт, Разрешения_ПП, Процент_Отгрузки) VALUES({row})",
                             cols=['Работаем?', 'Период обновления не более', 'Настройка', 'Отсрочка', 'Продаём для ОС',
                                   'Наценка для ОС', 'Макс снижение от базовой цены', 'Наценка на праздники (1,02)',
                                   'Наценка Р',
                                   'Мин наценка', 'Наценка на оптовые товары', 'Шаг градаци', 'Шаг опт',
                                   'Разрешения ПП',
                                   '% Отгрузки'])

        # LoadToDBPandasSilent(path_to_conditions, 'data07_14', connection, sh='07&14Данные',
        #                      request="INSERT INTO {table} (Работаем, Период_обновления_не_более,"
        #                              " Настройка, Макс_снижение_от_базовой_цены, Правильное, Наценка_ПБ, Код_ПБ_П) "
        #                              "VALUES({row})",
        #                      cols=['Работаем?', 'Период обновления не более', 'Настройка',
        #                            'Макс снижение от базовой цены',
        #                            'Правильное', 'Наценка ПБ', 'Код ПБ_П'])
        # LoadToDBPandasSilent(path_to_conditions, 'data15', connection, sh='15Данные',
        #                      request="INSERT INTO {table} (_15, Предложений_опт, ЦенаБ) VALUES({row})",
        #                      cols=[])
        # LoadToDBPandasSilent(path_to_conditions, 'Резерв_да', sh='Резерв_да',
        #                request="INSERT INTO {table} (_09Код, ШтР, _07Код) VALUES({row})", cols=[])
        # LoadToDBPandasSilent(path_to_conditions, 'data09', connection, sh='09Данные',
        #                      request="INSERT INTO {table} (УбратьЗП, ШтР, _09) VALUES({row})", cols=[])
        # LoadToDBPandasSilent(path_to_conditions, 'Закупки_для_ОС', connection, sh='Закупки для ОС',
        #                      request="INSERT INTO {table} (Количество_закупок, АртикулПроизводитель) VALUES({row})",
        #                      cols=[])
        # LoadToDBPandasSilent(path_to_conditions, 'data07', connection, sh='07Данные', cols=[])
        Log.add(f"Загрузка условий {showTime(datetime.datetime.now() - nt)}")
        Log.add('Конец обновления')

    def CheckSilentUpdateConditions(self):
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        res = False
        with connection.cursor() as cur:
            cur.execute("SELECT val FROM tmp WHERE setting = 'SilentUpdateConditions'")
            res = int(*cur.fetchone())
            cur.execute("UPDATE tmp SET val = '0' WHERE setting = 'SilentUpdateConditions'")
        connection.commit()
        connection.close()
        return res

    def CreateTotal(self):
        Log.add("Формирование итогового прайса ...")
        report_parts_count = 4
        nt = datetime.datetime.now()
        connection = None
        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cur:
                cur.execute(
                    f"UPDATE res SET ШтР = Резерв_да.ШтР FROM Резерв_да WHERE res._09Код_Поставщик_Товар = Резерв_да._09Код")

                cur.execute(f"UPDATE res SET Кол_во = Кол_во - ШтР where ШтР > 0")
                cur.execute(f"delete from res where Кол_во <= 0")

                cur.execute(f"update res set _06Кратность = 1 where _06Кратность is null")

                cur.execute(f"update res set Кратность_меньше = '-' where Кол_во < _06Кратность")

                cur.execute(f"update res set Разрешения_ПП = null where Разрешения_ПП = 'nan'")

                path_to_res = r'pre Итог'
                for file in os.listdir(path_to_res):
                    if file.startswith('Страница'):
                        os.remove(fr"{path_to_res}/{file}")
                file_csv = path_to_res + "/Страница {}.csv"

                df = pd.DataFrame(columns=["Ключ1 поставщика", "Артикул поставщика", "Производитель поставщика",
                                           "Наименование поставщика",
                                           "Количество поставщика", "Цена поставщика", "Кратность поставщика",
                                           "Примечание поставщика", "01Артикул", "02Производитель",
                                           "03Наименование", "05Цена", "06Кратность-", "07Код поставщика",
                                           "09Код + Поставщик + Товар", "10Оригинал",
                                           "13Градация", "14Производитель заполнен", "15КодТутОптТорг",
                                           "17КодУникальности", "18КороткоеНаименование",
                                           "19МинЦенаПоПрайсу", "20ИслючитьИзПрайса", "Отсрочка", "Продаём для ОС",
                                           "Наценка для ОС", "Наценка Р",
                                           "Наценка ПБ", "Мин наценка", "Наценка на оптовые товары", "Шаг градаци",
                                           "Шаг опт", "Разрешения ПП", "УбратьЗП", "Предложений опт",
                                           "ЦенаБ", "Кол-во", "Код ПБ_П", "06Кратность", "Кратность меньше", "05Цена+",
                                           "Количество закупок", "% Отгрузки",
                                           "Мин. Цена", "Мин. Поставщик"])

                for i in range(1, report_parts_count + 1):
                    df.to_csv(file_csv.format(i), sep=';', decimal=',', encoding="windows-1251", index=False,
                              errors='ignore')

                row_limit = report_row_limit
                list_limit = 1_048_500
                loaded_rows = 0
                page_num = 1
                # header = True
                # sr = 0

                # connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

                while True:
                    if loaded_rows > 0:
                        if int(loaded_rows / list_limit) >= page_num:
                            page_num += 1
                            # header = True
                            # sr = 0

                        # c = (list_limit * page_num) % (loaded_rows + row_limit)
                        new_row_limit = (list_limit * page_num) - loaded_rows if (list_limit * page_num) - loaded_rows < row_limit else row_limit
                        # a = (list_limit * page_num) % loaded_rows
                        # print(f"{a=}")
                    else:
                        new_row_limit = row_limit
                    df = pd.read_sql(f"""SELECT Ключ1_поставщика, Артикул_поставщика, Производитель_поставщика, 
                            Наименование_поставщика, Количество_поставщика, Цена_поставщика, Кратность_поставщика, Примечание_поставщика, 
                            _01Артикул, _02Производитель, _03Наименование, _05Цена, _06Кратность, _07Код_поставщика , _09Код_Поставщик_Товар, _10Оригинал, 
                            _13Градация, _14Производитель_заполнен, _15КодТутОптТорг, _17КодУникальности, _18КороткоеНаименование, 
                            _19МинЦенаПоПрайсу, _20ИслючитьИзПрайса, Отсрочка, Продаём_для_ОС, Наценка_для_ОС, Наценка_Р, Наценка_ПБ, 
                            Мин_наценка, Наценка_на_оптовые_товары, Шаг_градаци, Шаг_опт, Разрешения_ПП, УбратьЗП, Предложений_опт, ЦенаБ, Кол_во, Код_ПБ_П, 
                            _06Кратность, Кратность_меньше, _05Цена_плюс, Количество_закупок, Процент_Отгрузки, ЦенаМин, ЦенаМинПоставщик 
                            from res ORDER BY _17КодУникальности OFFSET {loaded_rows} LIMIT {new_row_limit}""",
                                     connection)

                    df_len = len(df)
                    if not df_len:
                        break

                    # if sr == row_limit: # Вторая итерация. Чтобы пропустить header и не терялась одна позиция
                    #     sr += 1
                    loaded_rows += df_len
                    # mode='w' if header else 'a'
                    df.to_csv(file_csv.format(page_num), mode='a', sep=';', decimal=',', encoding="windows-1251",
                              index=False, header=False, errors='ignore')  # header=header,
                # with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                #     df.to_excel(writer, index=False, sheet_name=f"Результат{page_num}", startrow=sr, header=header)
                # sr += new_row_limit

                # header = False
                connection.commit()
                connection.close()

                for i in range(1, report_parts_count + 1):
                    shutil.copy(fr"{path_to_res}/Страница {i}.csv", fr"Итог/Страница {i}.csv")

                Log.add(f"Итоговый прайса готов! Общее время: {showTime(datetime.datetime.now() - nt)}")

                # if email:
                send_email_report()
                Log.add(f"Письмо отправлено")

        except Exception as ex:
            Log.error(ex, "create report ERROR")
        finally:
            try:
                if connection:
                    connection.close()
            except:
                pass

def showTime(dt):
    h = int((dt.total_seconds() / 3600) % 60)
    m = int((dt.total_seconds() / 60) % 60)
    s = int(dt.total_seconds() % 60)
    if h < 10: h = f"0{h}"
    if m < 10: m = f"0{m}"
    if s < 10: s = f"0{s}"
    return f"[{h}:{m}:{s}]"


def LoadToDBPandas(path, table, cols, sh='', request="INSERT INTO {table} VALUES({row})", days=None):
    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    with connection.cursor() as cur:

        file_name = ''
        del_name = ''
        upd = 0
        if table == 'res':
            file_name = path.split('\\')[-1].split('/')[-1].split('.')[0]
            del_name = file_name
            cur.execute(f"SELECT Период_обновления_не_более FROM data07 WHERE Настройка = '{file_name}'")
            upd = cur.fetchone()
            if upd != None:
                upd = round(float(*upd), 2)
            file_name = ", '" + file_name + "'"

            if upd == None:
                Log.add(f"Нет в условиях {file_name}")
                connection.commit()
                connection.close()
                return
            if days - upd >= 30:
                Log.add(f"Не подходит по периоду обновления {file_name}")
                connection.commit()
                connection.close()
                return

        try:
            header = pd.read_excel(path, sheet_name=sh if sh else 0, header=0, nrows=1)
            cols_num = {}
            for i, c in enumerate(header.columns):
                if c in cols:
                    cols_num[i] = c

            sr = 1
            limit = 50000
            while True:
                excl = pd.read_excel(path, header=None, nrows=limit, skiprows=sr, usecols=cols_num.keys(),
                                     sheet_name=sh if sh else 0)
                # excl = excl.fillna('')
                if not len(excl):
                    break
                # print(len(excl), file_name, r)
                sr += len(excl)
                excl = excl.rename(columns=cols_num)
                excl = excl.reindex(columns=cols)
                # print(excl)
                # excl = pd.read_excel(path, sheet_name=sh if sh else 0)
                # excl = excl.fillna('')

                for row in excl.values:
                    s = ''
                    for i, content in enumerate(row):
                        # if i in unnecessary_fields:
                        #     continue
                        if isinstance(content, str):
                            content = content.replace('\'', '\'\'').replace(";", " ")
                        if content == '':
                            s += f"NULL, "
                        else:
                            s += f"'{content}', "

                    s = s.rstrip(', ') + file_name
                    try:
                        cur.execute(request.format(table=table, row=s))
                    except Exception as ex1:
                        # logger.error("load to db error 1:", exc_info=ex1)
                        # print('load to db error 1 [Ошибка]:', ex1)
                        Log.error(ex1, "load to db ERROR:1")
                        connection.rollback()
                        # print(request.format(table=table, row=s))
                        # print('---')
                        # print(ex1.args)
                        # print(ex1.__dict__)
                        # x = input()

        except Exception as ex:
            # logger.error("table error:", exc_info=ex)
            # print('[Ошибка в таблице с данными]:', ex)
            Log.error(ex, "table ERROR")
            if table == 'res':
                try:
                    cur.execute(f"DELETE FROM Время_изменений WHERE Название_файла = '{del_name}'")
                except Exception as ex2:
                    # logger.error("t2 error:", exc_info=ex2)
                    # print(ex2)
                    Log.error(ex2, "t2 ERROR")

    connection.commit()
    connection.close()


def LoadMulti(args):
    path, table, request, unnecessary_fields, count, total, password = args

    file_name = ''
    nt = datetime.datetime.now()
    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    with connection.cursor() as cur:
        # del_name = ''
        upd = 0
        if table == 'res':
            file_name = path.split('\\')[-1].split('/')[-1].split('.')[0]
            Log.add(f"{file_name} ...")
            time_edit = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            now = datetime.datetime.today()
            days = (now - time_edit).days

            cur.execute(f"DELETE FROM res WHERE Название_файла = '{file_name}'")

            # del_name = file_name
            cur.execute(f"SELECT Период_обновления_не_более FROM data07 WHERE Настройка = '{file_name}'")
            upd = cur.fetchone()
            if upd != None:
                upd = round(float(*upd), 2)
            file_name2 = ", '" + file_name + "'"

            if upd == None:
                Log.add(f"Нет в условиях {file_name}")
                cur.execute(f"delete from info_tab where Название_файла = '{file_name}'")
                cur.execute(f"insert into info_tab values('{file_name}', 'Нет в условиях', "
                            f"'{datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d-%m-%Y %H:%M:%S')}')")
                cur.execute(f"DELETE FROM Время_изменений WHERE Название_файла = '{file_name}'")
                cur.execute(
                    f"INSERT INTO Время_изменений VALUES('{file_name}', "
                    f"'{datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')}')")
                connection.commit()
                connection.close()
                count.value += 1
                Log.add(f'Обработка {file_name} закончена. Всего файлов загружено: {count.value}/{total}')
                return
            if days - upd >= 30:
                Log.add(f"Не подходит по периоду обновления {file_name}")
                cur.execute(f"delete from info_tab where Название_файла = '{file_name}'")
                cur.execute(f"insert into info_tab values('{file_name}', 'Не подходит по периоду обновления', "
                            f"'{datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d-%m-%Y %H:%M:%S')}')")
                cur.execute(f"DELETE FROM Время_изменений WHERE Название_файла = '{file_name}'")
                cur.execute(
                    f"INSERT INTO Время_изменений VALUES('{file_name}', "
                    f"'{datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')}')")
                connection.commit()
                connection.close()
                count.value += 1
                Log.add(f'Обработка {file_name} закончена. Всего файлов загружено: {count.value}/{total}')
                return

        try:
            r = 1
            limit = 50000
            while True:
                excl = pd.read_excel(path, header=None, nrows=limit, skiprows=r)
                excl = excl.fillna('')
                if not len(excl):
                    break
                # print(len(excl), file_name, r)
                r += len(excl)

                for row in excl.values:
                    s = ''
                    for i, content in enumerate(row):
                        if i in unnecessary_fields:
                            continue
                        if isinstance(content, str):
                            content = content.replace('\'', '\'\'').replace(";", " ")
                        if content == '':
                            s += f"NULL, "
                        else:
                            s += f"'{content}', "

                    s = s.rstrip(', ') + file_name2
                    try:
                        cur.execute(request.format(table=table, row=s))
                    except Exception as ex1:
                        # logger.error("load to db error 2:", exc_info=ex1)
                        # print('load to db error 2 [Ошибка]:', ex1)
                        Log.error(ex1, "load to db ERROR:2")
                        connection.rollback()
                        # print(request.format(table=table, row=s))
                        # print('---')
                        # print(ex1.args)
                        # print(ex1.__dict__)
                        # x = input()

        except Exception as ex:
            # logger.error("table2 error:", exc_info=ex)
            # print('[Ошибка в таблице с данными]:', ex)
            Log.error(ex, "table2 ERROR")
            # if table == 'res':
            #     try:
            #         cur.execute(f"DELETE FROM Время_изменений WHERE Название_файла = '{del_name}'")
            #     except Exception as ex2:
            #         print(ex2)
        Log.add(f"Загрузка сырых данных {file_name} {showTime(datetime.datetime.now() - nt)}")

        cur.execute(
            f"WITH deleted AS (DELETE FROM res WHERE Название_файла = '{file_name}' AND (_04Количество < 1 OR _05Цена <= 0 "
            f"OR _05Цена IS NULL OR _19МинЦенаПоПрайсу = 'DEL' OR _20ИслючитьИзПрайса IS NOT NULL OR _01Артикул IS NULL) returning *) "
            f"SELECT count(*) FROM deleted;")
        cnt = int(*cur.fetchone())
        if cnt != 0:
            Log.add(f"Удалено по первому условию: {cnt} {file_name}")

        cur.execute(
            f"update res set _01Артикул = regexp_replace(regexp_replace(_01Артикул, '^ | $', '', 'g'), ' +', ' ', 'g') "
            f"where Название_файла = '{file_name}'")
        cur.execute(f"update res set Кол_во = _04Количество where Название_файла = '{file_name}'")

        nt = datetime.datetime.now()
        cur.execute(f"select _14Производитель_заполнен from res where Название_файла = '{file_name}' "
                    f"group by _01Артикул, _07Код_поставщика, _14Производитель_заполнен having count(*) > 1")
        rep_brands = cur.fetchall()
        total_reps = 0
        if rep_brands:
            # cur.execute(f"select distinct(_14Производитель_заполнен) from res where Название_файла = '{file_name}'")
            cur.execute(f"select _01Артикул, _14Производитель_заполнен from res where Название_файла= '{file_name}' "
                        f"group by _01Артикул, _14Производитель_заполнен having count(*) > 1")
            # print(rep_brands)
            reps = cur.fetchall()
            reps = [i for i in reps]
            # print(reps)
            # return
            for art, brand in reps:
                art = art.replace('\'', '\'\'')
                brand = brand.replace('\'', '\'\'')

                # DEL для всех повторений
                cur.execute(f"""update res set _20ИслючитьИзПрайса = 'DEL' where Название_файла = '{file_name}' 
                            and _01Артикул = '{art}' and _14Производитель_заполнен = '{brand}'""")
                # Устанавливается 'not DEL' в каждой группе повторения, если цена в группе минимальная
                cur.execute(f"""update res set _20ИслючитьИзПрайса = 'not DEL' where Название_файла = '{file_name}' and 
                            _20ИслючитьИзПрайса = 'DEL' and _01Артикул = '{art}' and _14Производитель_заполнен = '{brand}' 
                            and _05Цена = (select min(_05Цена) from res where Название_файла = '{file_name}' and 
                            _20ИслючитьИзПрайса = 'DEL' and _01Артикул = '{art}' and _14Производитель_заполнен = '{brand}')""")
                # Среди записей с 'not DEL' ищутся записи не с максимальным кол-вом и на них устанавливается DEL
                cur.execute(f"""update res set _20ИслючитьИзПрайса = 'DEL' where Название_файла = '{file_name}' and 
                            _20ИслючитьИзПрайса = 'not DEL' and _01Артикул = '{art}' and _14Производитель_заполнен = '{brand}' 
                            and _04Количество != (select max(_04Количество) from res where Название_файла = '{file_name}' 
                            and _20ИслючитьИзПрайса = 'not DEL' and _01Артикул = '{art}' and _14Производитель_заполнен = '{brand}')""")
                # В оставшихся группах, где совпадает мин. цена и макс. кол-вл, остаются лишь записи с максимальным id
                cur.execute(
                    f"update res set _20ИслючитьИзПрайса = gen_random_uuid() where Название_файла = '{file_name}' and "
                    f"_01Артикул = '{art}' and _14Производитель_заполнен = '{brand}' and _20ИслючитьИзПрайса = 'not DEL'")
                cur.execute(f"""update res set _20ИслючитьИзПрайса = 'DEL' where Название_файла = '{file_name}' and _20ИслючитьИзПрайса != 'DEL' 
                            and _01Артикул = '{art}' and _14Производитель_заполнен = '{brand}' and _20ИслючитьИзПрайса != (select max(_20ИслючитьИзПрайса) 
                            from res where Название_файла = '{file_name}' and _20ИслючитьИзПрайса != 'DEL' and _01Артикул = '{art}' 
                            and _14Производитель_заполнен = '{brand}')""")
                cur.execute(
                    f"WITH deleted AS (DELETE FROM res WHERE Название_файла = '{file_name}' and _01Артикул = '{art}' "
                    f"and _14Производитель_заполнен = '{brand}' AND _20ИслючитьИзПрайса = 'DEL' returning *) SELECT count(*) FROM deleted")
                cnt = int(*cur.fetchone())
                total_reps += cnt
                cur.execute(
                    f"update res set _20ИслючитьИзПрайса = null where Название_файла = '{file_name}' and _01Артикул = '{art}' "
                    f"and _14Производитель_заполнен = '{brand}' AND _20ИслючитьИзПрайса != 'DEL'")
                # print(f"Удаление дублей {brand} {f"({cnt})" if cnt else '-'} {file_name}")

            Log.add(
                f"Удаление дублей завершено {f'({total_reps})' if total_reps else '-'} {file_name} {showTime(datetime.datetime.now() - nt)}")
            # total count reps

        #     # DEL(gen_random_uuid) для всех повторений
        #     cur.execute(f"""update res set _20ИслючитьИзПрайса = 'DEL' where Название_файла = '{file_name}' and
        #         (_01Артикул, _07Код_поставщика, _14Производитель_заполнен) in (select _01Артикул, _07Код_поставщика,
        #         _14Производитель_заполнен from res where Название_файла = '{file_name}' group by _01Артикул, _07Код_поставщика,
        #         _14Производитель_заполнен having count(*) > 1)""")
        #     # Устанавливается 'not DEL' в каждой группе повторения, если цена в группе минимальная
        #     cur.execute(f"""update res set _20ИслючитьИзПрайса = 'not DEL' from (
        #         select _01Артикул, _07Код_поставщика, _14Производитель_заполнен, count(*), min(_05Цена) as min_price
        #         from res where Название_файла = '{file_name}' and _20ИслючитьИзПрайса is not null
        #         group by _01Артикул, _07Код_поставщика, _14Производитель_заполнен HAVING COUNT(*) > 1) as T
        #         where res.Название_файла = '{file_name}' and res._01Артикул = T._01Артикул and
        #         res._07Код_поставщика = T._07Код_поставщика and res._14Производитель_заполнен = T._14Производитель_заполнен
        #         and res._05Цена = T.min_price""")
        #     # Среди записей с 'not DEL' ищутся записи не с максимальным кол-вом и на них устанавливается DEL
        #     cur.execute(f"""update res set _20ИслючитьИзПрайса ='DEL' from (select max(_04Количество) as max_count,
        #         _01Артикул, _07Код_поставщика, _14Производитель_заполнен from res where Название_файла = '{file_name}' and
        #         _20ИслючитьИзПрайса = 'not DEL' group by _01Артикул, _07Код_поставщика, _14Производитель_заполнен) as T
        #         where res.Название_файла = '{file_name}' and res._04Количество != T.max_count and res._01Артикул = T._01Артикул
        #         and res._07Код_поставщика = T._07Код_поставщика and res._14Производитель_заполнен = T._14Производитель_заполнен""")
        #     # В оставшихся группах, где совпадает мин. цена и макс. кол-вл, остаются лишь записи с максимальным id
        #     cur.execute(f"update res set _20ИслючитьИзПрайса = gen_random_uuid() where Название_файла = '{file_name}' and _20ИслючитьИзПрайса = 'not DEL'")
        #     cur.execute(f"""update res set _20ИслючитьИзПрайса ='DEL' from (select max(_20ИслючитьИзПрайса) as max_id,
        #         _01Артикул, _07Код_поставщика, _14Производитель_заполнен, count(*) from res where Название_файла = '{file_name}' and
        #         _20ИслючитьИзПрайса != 'DEL' and _20ИслючитьИзПрайса is not NULL group by _01Артикул, _07Код_поставщика,
        #         _14Производитель_заполнен) as T where res.Название_файла = '{file_name}' and res._20ИслючитьИзПрайса != T.max_id
        #         and res._01Артикул = T._01Артикул and res._07Код_поставщика = T._07Код_поставщика""")
        #     cur.execute(f"WITH deleted AS (DELETE FROM res WHERE Название_файла = '{file_name}' AND _20ИслючитьИзПрайса = 'DEL' returning *) SELECT count(*) FROM deleted")
        #     cnt = int(*cur.fetchone())
        #     cur.execute(f"update res set _20ИслючитьИзПрайса = null where Название_файла = '{file_name}' AND _20ИслючитьИзПрайса is not null")
        #     print(f"Удаление дублей {f"({cnt})" if cnt else ''} {file_name} {showTime(datetime.datetime.now() - nt)}")

        nt = datetime.datetime.now()
        cur.execute(f"""UPDATE res SET Отсрочка = data07.Отсрочка, Продаём_для_ОС = data07.Продаём_для_ОС, Наценка_для_ОС = data07.Наценка_для_ОС,
                                             Макс_снижение_от_базовой_цены = data07.Макс_снижение_от_базовой_цены, 
                                             Наценка_на_праздники_1_02 = data07.Наценка_на_праздники_1_02,
                                             Наценка_Р = data07.Наценка_Р, Мин_наценка = data07.Мин_наценка, 
                                             Наценка_на_оптовые_товары = data07.Наценка_на_оптовые_товары, Шаг_градаци = data07.Шаг_градаци, 
                                             Шаг_опт = data07.Шаг_опт, Разрешения_ПП = data07.Разрешения_ПП, 
                                             Процент_Отгрузки = data07.Процент_Отгрузки FROM data07 WHERE Название_файла = '{file_name}' AND
                                             res._07Код_поставщика = data07.Настройка;""")
        Log.add(f"Расчёт data07 {file_name} {showTime(datetime.datetime.now() - nt)}")

        nt = datetime.datetime.now()
        # cur.execute(f"""UPDATE res SET УбратьЗП = data09.УбратьЗП, ШтР = data09.ШтР FROM data09 WHERE res.Название_файла = '{file_name}' AND res._09Код_Поставщик_Товар = data09._09;""")
        cur.execute(
            f"""UPDATE res SET УбратьЗП = data09.УбратьЗП FROM data09 WHERE res.Название_файла = '{file_name}' AND res._09Код_Поставщик_Товар = data09._09;""")
        Log.add(f"Расчёт data09 {file_name} {showTime(datetime.datetime.now() - nt)}")

        nt = datetime.datetime.now()
        # cur.execute(
        #     f"""UPDATE res SET Предложений_опт = data15.Предложений_опт, ЦенаБ = data15.ЦенаБ FROM data15 WHERE Название_файла = '{file_name}' AND res._15КодТутОптТорг = data15._15;""")
        cur.execute(f"""UPDATE res SET ЦенаБ = base_price.ЦенаБ, ЦенаМин = base_price.ЦенаМин, ЦенаМинПоставщик = base_price.ЦенаМинПоставщик 
                        FROM base_price WHERE Название_файла = '{file_name}' AND res._01Артикул = base_price.Артикул 
                        AND res._14Производитель_заполнен = base_price.Бренд""")
        cur.execute(f"""UPDATE res SET Предложений_опт = mass_offers.Предложений_в_опте FROM mass_offers WHERE Название_файла = '{file_name}' 
                        AND res._01Артикул = mass_offers.Артикул AND res._14Производитель_заполнен = mass_offers.Бренд""")
        Log.add(f"Расчёт ЦенаБ, Предложений в опте {file_name} {showTime(datetime.datetime.now() - nt)}")

        nt = datetime.datetime.now()
        cur.execute(f"UPDATE res SET Низкая_цена = _05Цена / ЦенаБ WHERE Название_файла = '{file_name}';")

        # cur.execute(f"UPDATE res SET ШтР = NULL WHERE Название_файла = '{file_name}' AND ШтР = 0;")
        # cur.execute(f"UPDATE res SET Кол_во = _04Количество WHERE Название_файла = '{file_name}' AND Низкая_цена IS NULL AND ШтР IS NULL;")  # ШтР = ''
        # cur.execute(f"UPDATE res SET Кол_во = _04Количество - ШтР WHERE Название_файла = '{file_name}' AND Низкая_цена IS NULL AND ШтР IS NOT NULL AND Кол_во IS NULL;")  # ШтР != '' AND Низкая_цена IS NULL
        # cur.execute(f"UPDATE res SET Кол_во = 0 WHERE Название_файла = '{file_name}' AND Низкая_цена IS NOT NULL AND Низкая_цена < Макс_снижение_от_базовой_цены AND Кол_во IS NULL;")
        # cur.execute(f"UPDATE res SET Кол_во = _04Количество WHERE Название_файла = '{file_name}' AND Низкая_цена IS NOT NULL AND ШтР IS NULL AND Кол_во IS NULL;")
        # cur.execute(f"UPDATE res SET Кол_во = _04Количество - ШтР WHERE Название_файла = '{file_name}' AND Низкая_цена IS NOT NULL AND ШтР IS NOT NULL AND Кол_во IS NULL;")

        # cur.execute(f"DELETE FROM res WHERE Название_файла = '{file_name}' AND Кол_во < 1;")
        # cur.execute(f"DELETE FROM res WHERE Название_файла = '{file_name}' AND Кол_во IS NULL;")
        cur.execute(
            f"WITH deleted AS (DELETE FROM res WHERE Название_файла = '{file_name}' AND (_04Количество < 1 OR _04Количество IS NULL) returning *) SELECT count(*) FROM deleted;")
        cnt = int(*cur.fetchone())
        if cnt != 0:
            Log.add(f"Удалено по первому условию: {cnt} {file_name}")
        Log.add(f"Расчёт Низкая_цена, удаление по второму условию {file_name} {showTime(datetime.datetime.now() - nt)}")

        nt = datetime.datetime.now()
        cur.execute(f"""UPDATE res SET Наценка_ПБ = data07_14.Наценка_ПБ, Код_ПБ_П = data07_14.Код_ПБ_П FROM data07_14 
                WHERE Название_файла = '{file_name}' AND res._07Код_поставщика = data07_14.Настройка AND res._14Производитель_заполнен 
                ILIKE data07_14.Правильное;""")
        Log.add(f"Расчёт data07_14 {file_name} {showTime(datetime.datetime.now() - nt)}")

        nt = datetime.datetime.now()
        cur.execute(
            f"UPDATE res SET _06Кратность = _06Кратность_ WHERE Название_файла = '{file_name}' AND Наценка_на_праздники_1_02 = 0;")
        cur.execute(
            f"UPDATE res SET _06Кратность = _04Количество WHERE Название_файла = '{file_name}' AND Наценка_на_праздники_1_02 > _05Цена * _04Количество")
        cur.execute(f"""UPDATE res SET _06Кратность = CEILING(GREATEST(_06Кратность_, Наценка_на_праздники_1_02 / _05Цена) / _06Кратность_) * _06Кратность_ 
                WHERE Название_файла = '{file_name}' AND Наценка_на_праздники_1_02 < _05Цена * _04Количество AND 
                Наценка_на_праздники_1_02 != 0 AND _06Кратность IS NULL;""")
        # cur.execute(f"""UPDATE res SET Кратность_меньше = '-' WHERE Название_файла = '{file_name}' AND Кол_во < GREATEST(_06Кратность_, _06Кратность);""")
        cur.execute(f"UPDATE res SET _05Цена_плюс = _05Цена WHERE Название_файла = '{file_name}';")
        cur.execute(
            f"UPDATE res SET _05Цена_плюс = Наценка_на_праздники_1_02 / _04Количество WHERE Название_файла = '{file_name}' "
            f"AND _05Цена * _04Количество < Наценка_на_праздники_1_02")
        cur.execute(f"""UPDATE res SET Количество_закупок = Закупки_для_ОС.Количество_закупок 
                FROM Закупки_для_ОС WHERE Название_файла = '{file_name}' AND res._15КодТутОптТорг = Закупки_для_ОС.АртикулПроизводитель ;""")
        Log.add(
            f"Расчёт 06Кратность, 05Цена_плюс, Количество_закупок {file_name} {showTime(datetime.datetime.now() - nt)}")

        cur.execute(f"DELETE FROM Время_изменений WHERE Название_файла = '{file_name}'")
        cur.execute(f"INSERT INTO Время_изменений VALUES('{file_name}', "
                    f"'{datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')}')")

        cur.execute(f"select count(*) from res where Название_файла = '{file_name}'")
        cnt = cur.fetchone()[0]
        cur.execute(f"delete from info_tab where Название_файла = '{file_name}'")
        cur.execute(f"insert into info_tab values('{file_name}', '{cnt}', "
                    f"'{datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d-%m-%Y %H:%M:%S')}')")

        count.value += 1
        Log.add(f"Обработка {file_name} ({cnt}) закончена. Всего файлов загружено: {count.value}/{total}")
    connection.commit()
    connection.close()


def LoadToDBPandasSilent(path, table, connection, cols, sh='', request="INSERT INTO {table} VALUES({row})", days=None):
    with connection.cursor() as cur:
        file_name = ''
        del_name = ''
        upd = 0
        if table == 'res':
            file_name = path.split('\\')[-1].split('/')[-1].split('.')[0]
            del_name = file_name
            cur.execute(f"SELECT Период_обновления_не_более FROM data07 WHERE Настройка = '{file_name}'")
            upd = cur.fetchone()
            if upd != None:
                upd = round(float(*upd), 2)
            file_name = ", '" + file_name + "'"

            if upd == None:
                Log.add(f"Нет в условиях {file_name}")
                return
            if days - upd >= 30:
                Log.add(f"Не подходит по периоду обновления {file_name}")
                return

        try:
            header = pd.read_excel(path, sheet_name=sh if sh else 0, header=0, nrows=1)
            cols_num = {}
            for i, c in enumerate(header.columns):
                if c in cols:
                    cols_num[i] = c

            sr = 1
            limit = 50000
            while True:
                excl = pd.read_excel(path, header=None, nrows=limit, skiprows=sr, usecols=cols_num.keys(),
                                     sheet_name=sh if sh else 0)
                # excl = excl.fillna('')
                if not len(excl):
                    break
                excl = excl.rename(columns=cols_num)
                excl = excl.reindex(columns=cols)
                # print(len(excl), file_name, r)
                sr += len(excl)

                # excl = pd.read_excel(path, sheet_name=sh if sh else 0)
                # excl = excl.fillna('')

                for row in excl.values:
                    s = ''
                    for i, content in enumerate(row):
                        # if i in unnecessary_fields:
                        #     continue
                        if isinstance(content, str):
                            content = content.replace('\'', '\'\'').replace(";", " ")
                        if content == '':
                            s += f"NULL, "
                        else:
                            s += f"'{content}', "

                    s = s.rstrip(', ') + file_name
                    # print(s)
                    try:
                        cur.execute(request.format(table=table, row=s))
                    except Exception as ex1:
                        # logger.error("load to db error 3:", exc_info=ex1)
                        # print('load to db error 3 [Ошибка]:', ex1)
                        Log.error(ex1, "load to db ERROR:3")
                        connection.rollback()
                        # print('[Ошибка]:', ex1)
                        # print(request.format(table=table, row=s))
                        # print('---')
                        # print(ex1.args)
                        # print(ex1.__dict__)
                        # x = input()

        except Exception as ex:
            # logger.error("table3 error:", exc_info=ex)
            # print('[Ошибка в таблице с данными]:', ex)
            Log.error(ex, "table3 ERROR")
            if table == 'res':
                try:
                    cur.execute(f"DELETE FROM Время_изменений WHERE Название_файла = '{del_name}'")
                except Exception as ex2:
                    # logger.error("t3 error:", exc_info=ex2)
                    # print(ex2)
                    Log.error(ex2, "t3 ERROR")
    connection.commit()


def send_email_report():
    '''Отправка письма с вложенным прайсом'''
    msg = MIMEText("", "plain", "utf-8")
    send_to = "" 

    msg["Subject"] = Header("Обновились данные для прайсов")
    msg["From"] = mail_login
    msg["To"] = send_to

    s = smtplib.SMTP("smtp.yandex.ru", 587, timeout=100)
    try:
        s.starttls()
        s.login(mail_login, mail_password)
        s.sendmail(msg["From"], send_to, msg.as_string())
    except Exception as ex:
        Log.error(ex, "send mail ERROR")
    finally:
        s.quit()


    # send_to = "1@gmail.com" 
    # msg = MIMEMultipart()
    # msg["Subject"] = Header(f"{code}")
    # msg["From"] = mail_login
    # msg["To"] = send_to
    # # msg.attach(MIMEText("price PL3", 'plain'))
    #
    # s = smtplib.SMTP("smtp.yandex.ru", 587, timeout=100)
    #
    # try:
    #     s.starttls()
    #     s.login(mail_login, mail_password)
    #
    #     file_path = rf"{path_to_final}\{name}.csv"
    #
    #     with open(file_path, 'rb') as f:
    #         file = MIMEApplication(f.read())
    #
    #     file.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
    #     msg.attach(file)
    #
    #     s.sendmail(msg["From"], send_to, msg.as_string()) # tmptr101@gmail.com
    #
    #     shutil.copy(file_path, fr"{path_to_sended}/{name}.csv")
    # except Exception as ex:
    #     logger.error("send_email error:", exc_info=ex)
    #     InfoModule.increase_error_count()
    # finally:
    #     s.quit()


if __name__ == '__main__':
    mp.freeze_support()
    try:
        if len(sys.argv) >= 2:
            autostart = sys.argv[1]

        text = ["Путь до условий:\n", "Путь до папки с прайсами:\n", "Пароль для БД:\n", "Chunk"]
        if not 'Settings.txt' in os.listdir():
            with open('Settings.txt', 'w', encoding='utf-8') as settings:
                settings.writelines(text)

        dirs = [r'Итог', r'pre Итог']
        for d in dirs:
            if not os.path.exists(d):
                os.mkdir(d)

        with open('Settings.txt', 'r', encoding='utf-8') as settings:
            path_to_conditions = settings.readline().strip('Путь до условий:').strip()
            path_to_files = settings.readline().strip('Путь до папки с прайсами:').strip()
            password = settings.readline().strip('Пароль для БД:').strip()
            report_row_limit = settings.readline().strip('Chunk:').strip()
            report_row_limit = int(report_row_limit)
            if report_row_limit > 1_048_500:
                report_row_limit = 1_048_500

        if path_to_conditions == '' and path_to_files == '' and password =='':
            Log.add("Заполните Settings.txt")
            time.sleep(5)
            exit(0)

        db_url = f"postgresql+psycopg2://postgres:{password}@localhost:5432/prices"
        engine = create_engine(url=db_url, echo=False)

        if path_to_files[-1] != '\\':
            path_to_files += '\\'

        now = datetime.datetime.now()
        # logger.info("Start")
        Log.add("Start")

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())

    except Exception as ex:
        # logger.error("main error:", exc_info=ex)
        # print(ex)
        Log.error(ex, "main ERROR")
        ex = input('Error')
