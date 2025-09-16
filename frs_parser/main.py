from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from main_ui import Ui_MainWindow
import multiprocessing as mp
import re
import time
import sys

options = Options()
options.add_argument('--headless')

url = r"https://egrul.nalog.ru/index.html"
rows_count = 10

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['ОГРН', 'Название'])
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setModel(self.model)
        self.tableView.verticalHeader().hide()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.textBrowser.document().setMaximumBlockCount(200)

        for i in range(rows_count):
            self.model.appendRow([QStandardItem(""), QStandardItem("")])

        self.StartButton.clicked.connect(self.StartChecking)

        self.ResetButtonText.clicked.connect(lambda _: self.textEdit.clear())
        self.ResetButton.clicked.connect(self.TableClear)
        self.ClearLogButton.clicked.connect(self.textBrowser.clear)

    def TableClear(self):
        self.model.removeRows(0, rows_count)
        for i in range(rows_count):
            self.model.appendRow([QStandardItem(""), QStandardItem("")])

    def StartChecking(self):
        args = list()
        for i in range(rows_count):
            ogrn = self.model.item(i, 0).text()
            name = self.model.item(i, 1).text()
            if ogrn and name:
                # print(i, ogrn, name)
                args.append([i, ogrn, name])

        # print(args)

        if args:
            self.get_info_from_frs(args)


    def get_info_from_frs(self, args):
        # id, ogrn, name_in_doc = args
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(url=url)
            driver.maximize_window()
            # time.sleep(1)
            query_input = driver.find_element(By.ID, 'query')
            for arg in args:
                id, ogrn, name_in_doc = arg
                id += 1
                query_input.clear()
                query_input.send_keys(ogrn)
                # driver.implicitly_wait(1)
                # search_button = driver.find_element(By.ID, 'query')
                # time.sleep(1)
                query_input.send_keys(Keys.ENTER)
                time.sleep(1)
                # with open('egrul_nalog.html', encoding='utf-8') as file:
                # file.write(driver.page_source)
                # page = file.read()
                soup = BeautifulSoup(driver.page_source, "lxml")
                row = soup.find("div", class_="res-row")
                name = str(row.find("div", class_="res-caption").a.text).lower()
                info = row.find("div", class_="res-text").text


                color = "#3bc718"
                if re.findall('прекращения', info):
                    color = "#e54919"
                self.textBrowser.append(f"({id}) <span style='color:{color};'>{info}</span>")

                name_in_doc = re.sub(r'\W', '', name_in_doc).lower()
                name_to_compare = re.sub(r'\W', '', name).lower()
                # print(f"{name_in_doc=}")
                # print(f"{name_to_compare=}")

                color = "#3bc718"
                if name_in_doc != name_to_compare:
                    color = "#e54919"
                self.textBrowser.append(f"({id}) <span style='color:{color};'>{name}</span>")
                self.textBrowser.append('-' * 30)
                print(name)
                print(info)
                print()

            time.sleep(5)
        except Exception as ex:
            self.textBrowser.append(f"({id}) <span style='color:#e54919;'>НЕ НАЙДЕНО ({ogrn}) {name_in_doc}</span>")
            print(ex)
        finally:
            driver.close()
            driver.quit()

# def main():
#     driver = webdriver.Chrome()
#     ogrn = 261301394234
#
#     try:
#         driver.get(url=url)
#         # time.sleep(2)
#         query_input = driver.find_element(By.ID, 'query')
#         query_input.clear()
#         query_input.send_keys(ogrn)
#         # time.sleep(1)
#         search_button = driver.find_element(By.ID, 'query')
#         # time.sleep(1)
#         search_button.send_keys(Keys.ENTER)
#         # time.sleep(2)
#         driver.maximize_window()
#         # with open('egrul_nalog.html', encoding='utf-8') as file:
#             # file.write(driver.page_source)
#             # page = file.read()
#         soup = BeautifulSoup(driver.page_source, "lxml")
#         row = soup.find("div", class_="res-row")
#         name = str(row.find("div", class_="res-caption").a.text).lower()
#         info = row.find("div", class_="res-text").text
#         print(name)
#         print(info)
#
#         time.sleep(5)
#     except Exception as ex:
#         print(ex)
#     finally:
#         driver.close()
#         driver.quit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

    # x = 'asd ysy asd12'
    # print('+' if re.findall('1ysy', x) else '-')