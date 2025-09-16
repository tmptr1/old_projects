import time
import re
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from bs4 import BeautifulSoup
import sqlite3 as sq
import pandas as pd
import numpy as np
import os
import logging
from logging.handlers import RotatingFileHandler
# import openpyxl
# from python_calamine.pandas import pandas_monkeypatch
# from python_calamine.pandas import pandas_monkeypatch

logger = logging.getLogger(__name__)
log_format = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s",
                               datefmt="%Y-%m-%d %H:%M:%S")

handler = RotatingFileHandler('Информация.log', maxBytes=20 * 1024 * 1024, backupCount=2, errors='ignore')
handler.setFormatter(log_format)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

class Ui_MainWindow(object):
    name_char_limit = 500
    article_char_limit = 256

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(509, 540)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(30, 10, 451, 261))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(5, 1, item)
        self.LoadAll = QtWidgets.QPushButton(self.centralwidget)
        self.LoadAll.setGeometry(QtCore.QRect(210, 290, 101, 23))
        self.LoadAll.setObjectName("LoadAll")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 340, 491, 151))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 300, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 509, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.TA = ThreadAction(self)
        self.TA.printSignal.connect(self.print_log)
        self.TA.start()

        list_of_func = [self.load_alt, self.load_dm, self.load_kv, self.load_ser, self.load_eli, self.load_adi]

        for r, f in enumerate(list_of_func):
            btn = QtWidgets.QPushButton(self.tableWidget)
            btn.setText('Загрузить')
            btn.clicked.connect(f)
            self.tableWidget.setCellWidget(r, 2, btn)

        self.LoadAll.clicked.connect(self.create_ex)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "5"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "6"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Прайс"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Курс валюты"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "-"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "Альтернатива"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("MainWindow", "usd: 100"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("MainWindow", "Думанян"))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("MainWindow", "usd: 100"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("MainWindow", "Коврежкина"))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("MainWindow", "usd: 100"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("MainWindow", "Сердюченко"))
        item = self.tableWidget.item(3, 1)
        item.setText(_translate("MainWindow", "usd: 100"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("MainWindow", "Элион"))
        item = self.tableWidget.item(4, 1)
        item.setText(_translate("MainWindow", "usd: 100"))
        item = self.tableWidget.item(5, 0)
        item.setText(_translate("MainWindow", "ADILET"))
        item = self.tableWidget.item(5, 1)
        item.setText(_translate("MainWindow", "cny: 12.42, usd: 100"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.LoadAll.setText(_translate("MainWindow", "Объединить"))
        self.label.setText(_translate("MainWindow", "Информация:"))


    def print_log(self, text):
        self.textBrowser.setPlainText(text)
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)

    def get_val(self, row_id, pattern):
        dgt = ""
        dgt += pattern
        dgt += "\d{1,10}.\d{1,2}"
        try:
            val = float(re.sub(pattern, "", re.findall(dgt, self.tableWidget.item(row_id, 1).text().replace(",","."))[0]))
            if val <= 0:
                raise Exception
        except Exception as ex:
            logger.info("Некорректное значение курса доллара")
            return False
        return val

    def load_kv(self):
        # p = "usd: "
        # x = ''
        # x += p
        # x += "\d{1,10}.\d{1,2}"
        # print(re.findall(x, "usd: 222.45"))
        # return
        usd = self.get_val(2, "usd: ")
        if not usd:
            return
        # print(usd)
        # return
        try:
            with open("Прайсы/index.html") as file:
                page = file.read()

            soap = BeautifulSoup(page, "html.parser")
            tables = soap.find_all(class_="MsoNormalTable")
            # print(len(tables))
            logger.info("Загрузка прайса 'Коврежкина' ...")
            with sq.connect('price.db') as con:
                cur = con.cursor()
                cur.execute(f"delete from price_list where price_code = 'Коврежкина'")

                for t in tables:
                    # cnt = 0
                    for tr in t.find_all("tr"):
                        # cnt += 1
                        td = tr.find_all("td")
                        try:
                            # print(td[1].text.strip(), td[2].text.strip(), td[7].text.strip())
                            name, article, price = text_fix(td[1].text)[:self.name_char_limit], text_fix(td[2].text)[:self.article_char_limit], float(
                                td[7].text.replace(',', '.'))
                            # print(name, article, price)
                            # cur.execute(f"insert into price_list values('{name}', '{article}', {price}, 'Коврежкина')")
                        except Exception as e_:
                            # print(ex)
                            # logger.error("Ошибка:", exc_info=e_)
                            continue
                        cur.execute(f"insert into price_list(name, article, price, price_usd, price_code) "
                                    f"values('{name}', '{article}', {int(price * usd)}, {round(price, 2)}, 'Коврежкина')")
                    # print(cnt)

                cur.execute("delete from price_list where price_code = 'Коврежкина' "
                            "AND (price <= 0 OR name is NULL)")
                cur.execute("select count(*) from price_list where price_code = 'Коврежкина'")
                cnt = cur.fetchone()[0]
            # print(res[0])
            logger.info(f"Прайс 'Коврежкина' обработан. Записей загружено: {cnt}")
        except Exception as ex:
            # print(ex)
            logger.error("Ошибка при обработке прайса 'Коврежкина':", exc_info=ex)


    def load_dm(self):
        usd = self.get_val(1, "usd: ")
        if not usd:
            return

        try:
            df = pd.read_excel("Прайсы\Думанян.xlsx", header=None, usecols=[1,2,3,4])
            # print(len(df))
            df = df[df[2].apply(lambda x: x != 'компл')]
            df = df[df[4].apply(lambda x: x is np.nan)]
            df = df[df[3].apply(price_check)]
            # print(len(df))
            logger.info("Загрузка прайса 'Думанян' ...")

            with sq.connect('price.db') as con:
                cur = con.cursor()
                cur.execute(f"delete from price_list where price_code = 'Думанян'")

                for i in df.values:
                    try:
                        article = re.sub(r"толщ \d{1,3}.\d{1,3}", '', i[0])
                        words = re.findall(r"[а-яА-Я]{3,30}", article)
                        name = ''
                        for w in words:
                            name += f"{w} "
                            article = article.replace(w, '')
                        name = re.sub(r"Пленка|ПВХ|колле[ц]{1,2}ия Керамик|[Мм]атовая", '', name).strip()[:self.name_char_limit]
                        name = re.sub(r"[ ]{2,5}", " ", name)
                        article = article.replace('(', '').replace(')', '').strip()[:self.article_char_limit]

                    except Exception as e_:
                        # print(ex)
                        continue
                    # print(name, '||', article, i[2])
                    # cur.execute(f"insert into price_list values('{name}', '{article}', {i[2]}, 'Думанян')")
                    cur.execute(f"insert into price_list(name, article, price, price_usd, price_code) "
                                f"values('{text_fix(name)}', '{text_fix(article)}', {int(i[2])}, {round(i[2]/usd, 2)}, 'Думанян')")

                cur.execute("delete from price_list where price_code = 'Думанян' "
                            "AND (price <= 0 OR name is NULL)")
                cur.execute("select count(*) from price_list where price_code = 'Думанян'")
                cnt = cur.fetchone()[0]

            logger.info(f"Прайс 'Думанян' обработан. Записей загружено: {cnt}")

        except Exception as ex:
            logger.error("Ошибка при обработке прайса 'Думанян':", exc_info=ex)


    def load_alt(self):
        usd = self.get_val(0, "usd: ")
        if not usd:
            return
        try:
            # pandas_monkeypatch()
            df = pd.read_excel("Прайсы\Альтернатива.xlsx", header=None, usecols=[0, 1, 4])
            # print(len(df))
            # print(df[:11])
            df = df[df[4].apply(price_check)]
            # print(len(df))
            # print(df[df[2]])
            logger.info("Загрузка прайса 'Альтернатива' ...")

            with sq.connect('price.db') as con:
                cur = con.cursor()
                cur.execute(f"delete from price_list where price_code = 'Альтернатива'")

                for i in df.values:
                    try:
                        cur.execute(f"insert into price_list(name, article, price, price_usd, price_code) "
                                    f"values('{text_fix(i[0])[:self.name_char_limit]}', '{text_fix(i[1])[:self.article_char_limit]}', "
                                    f"{int(i[2])}, {round(i[2] / usd, 2)}, 'Альтернатива')")
                    except Exception as e_:
                        continue

                cur.execute("delete from price_list where price_code = 'Альтернатива' "
                            "AND (price <= 0 OR name is NULL)")
                cur.execute("select count(*) from price_list where price_code = 'Альтернатива'")
                cnt = cur.fetchone()[0]

            logger.info(f"Прайс 'Альтернатива' обработан. Записей загружено: {cnt}")

        except Exception as ex:
            logger.error("Ошибка при обработке прайса 'Альтернатива':", exc_info=ex)


    def load_ser(self):
        usd = self.get_val(3, "usd: ")
        if not usd:
            return

        try:
            df = pd.read_excel("Прайсы\Сердюченко.xlsx", header=None, usecols=[1, 2, 4])
            # print(len(df))
            df = df[df[4].apply(price_check)]

            logger.info("Загрузка прайса 'Сердюченко' ...")

            with sq.connect('price.db') as con:
                cur = con.cursor()
                cur.execute(f"delete from price_list where price_code = 'Сердюченко'")

                for i in df.values:
                    try:
                        name = i[0].replace("НОВИНКА!!!", "").replace("НОВИНКА !!!", "")
                        # print(name, i[1], int(i[2]))
                        cur.execute(f"insert into price_list(name, article, price, price_usd, price_code) "
                                    f"values('{text_fix(name)[:self.name_char_limit]}', '{text_fix(i[1])[:self.article_char_limit]}', "
                                    f"{int(i[2])}, {round(i[2] / usd, 2)}, 'Сердюченко')")
                    except Exception as e_:
                        continue

                cur.execute("delete from price_list where price_code = 'Сердюченко' "
                            "AND (price <= 0 OR name is NULL)")
                cur.execute("delete from price_list where price_code = 'Сердюченко' and name = 'Каталог'")
                cur.execute("select count(*) from price_list where price_code = 'Сердюченко'")
                cnt = cur.fetchone()[0]

            logger.info(f"Прайс 'Сердюченко' обработан. Записей загружено: {cnt}")

        except Exception as ex:
            logger.error("Ошибка при обработке прайса 'Сердюченко':", exc_info=ex)


    def load_eli(self):
        usd = self.get_val(4, "usd: ")
        if not usd:
            return

        try:
            df = pd.read_excel("Прайсы\Элион.xlsx", header=None, usecols=[0, 1, 2])
            # print(len(df))
            df = df[df[2].apply(price_check)]
            # print(len(df))

            logger.info("Загрузка прайса 'Элион' ...")

            with sq.connect('price.db') as con:
                cur = con.cursor()
                cur.execute(f"delete from price_list where price_code = 'Элион'")

                for i in df.values:
                    try:
                        # print(i)
                        # name = i[0].replace("НОВИНКА!!!", "").replace("НОВИНКА !!!", "")
                        # print(name, i[1], int(i[2]))
                        cur.execute(f"insert into price_list(name, article, price, price_usd, price_code) "
                                    f"values('{text_fix(i[1])[:self.name_char_limit]}', '{text_fix(i[0])[:self.article_char_limit]}', "
                                    f"{int(i[2])}, {round(int(i[2]) / usd, 2)}, 'Элион')")
                    except Exception as e_:
                        print(e_)
                        continue

                cur.execute("delete from price_list where price_code = 'Элион' "
                            "AND (price <= 0 OR name is NULL)")
                cur.execute("select count(*) from price_list where price_code = 'Элион'")
                cnt = cur.fetchone()[0]

            logger.info(f"Прайс 'Элион' обработан. Записей загружено: {cnt}")

        except Exception as ex:
            logger.error("Ошибка при обработке прайса 'Элион':", exc_info=ex)

    def load_adi(self):
        usd = self.get_val(5, "usd: ")
        if not usd:
            return
        cny = self.get_val(5, "cny: ")
        if not cny:
            return
        # print(usd)
        # print(cny)

        try:
            df = pd.read_excel("Прайсы\ПРАЙС ADILET  - КРАСНОДАР - ЮАНЬ -07.10.xlsx", header=None, usecols=[0,2])
            # print(len(df))
            # return
            # df = df[df[2].apply(lambda x: x != 'компл')]
            # df = df[df[4].apply(lambda x: x is np.nan)]
            df = df[df[2].apply(price_check)]
            # print(len(df))
            logger.info("Загрузка прайса 'Adilet' ...")

            with sq.connect('price.db') as con:
                cur = con.cursor()
                cur.execute(f"delete from price_list where price_code = 'Adilet'")

                for i in df.values:
                    try:
                        # article = re.sub(r"толщ \d{1,3}.\d{1,3}", '', i[0])
                        article = i[0]
                        article = re.sub(r"Пленка мат|Плёнка мат|мет|Пленка глянц", '', article)
                        words = re.findall(r"[а-яА-Яёa-zA-Z]{3,30}|\d{1,3},\d{1,2}мм", article)
                        name = ''
                        for w in words:
                            name += f"{w} "
                            article = article.replace(w, '')
                        name = name.replace('.', '')
                        name = name.strip()[:self.name_char_limit]
                        # name = re.sub(r"[ ]{2,5}", " ", name)
                        article = article.replace('(', '').replace(')', '').replace('.', '').strip()[:self.article_char_limit]
                        rub = i[1] * cny * 1.4
                        # print(name, '||', article, '||', int(rub), round(rub/usd, 2))
                    except Exception as e_:
                        # print(ex)
                        continue
                    # print(name, '||', article, i[2])
                    cur.execute(f"insert into price_list(name, article, price, price_usd, price_code) "
                                f"values('{text_fix(name)}', '{text_fix(article)}', {int(rub)}, {round(rub/usd, 2)}, 'Adilet')")

                cur.execute("delete from price_list where price_code = 'Adilet' "
                            "AND (price <= 0 OR name is NULL)")
                cur.execute("select count(*) from price_list where price_code = 'Adilet'")
                cnt = cur.fetchone()[0]

            logger.info(f"Прайс 'Adilet' обработан. Записей загружено: {cnt}")

        except Exception as ex:
            logger.error("Ошибка при обработке прайса 'Adilet':", exc_info=ex)

    def create_ex(self):
        with sq.connect('price.db') as con:
            df = pd.read_sql("select * from price_list", con)
            writer = pd.ExcelWriter("Итоговый прайс.xlsx")
            df.to_excel(writer, index=False)
            writer.close()
        logger.info(f"Итоговый прайс сформирован")


def price_check(x):
    if isinstance(x, (int, float)):
        if x > 0:
            return True
    return False



class ThreadAction(QtCore.QThread):
    printSignal = QtCore.pyqtSignal(str)
    def __init__(self, mainApp=None):
        super(ThreadAction, self).__init__()
        self.mainApp = mainApp
        self.log_file = 'Информация.log'

    def run(self):
        while True:
            try:
                if os.path.exists(self.log_file):
                    with open(self.log_file, 'r') as f:
                        lines = f.readlines()[-10:]
                        lines = ''.join(lines)
                        self.printSignal.emit(lines)
            except Exception as ex:
                print(f"LOG ERROR: {ex}")
            time.sleep(2)


def text_fix(t):
    return str(t).replace('\'', '\'\'').strip()



if __name__ == "__main__":
    # df = pd.read_excel("Прайсы\Альтернатива.xlsx")
    # print(len(df))

    # if False:
    with sq.connect('price.db') as con:
        cur = con.cursor()
        cur.execute("CREATE table IF NOT EXISTS price_list( "
                    "name varchar(500), "
                    "article varchar(500), "
                    "price NUMERIC(12,2), "
                    "price_usd NUMERIC(12,2), "
                    "price_code varchar(50))")
    #     res = cur.fetchone()
    #     print(res[0])
    #     for i in res:
    #         print(i)


    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

