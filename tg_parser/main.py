import time
import datetime
from pyrogram import Client, filters, idle
from dadata import Dadata
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from ui_form import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QThread
import re
import logging
from logging.handlers import RotatingFileHandler
import sys
import os
# pip install openpyxl

logger = logging.getLogger('logs.log')
logger.setLevel(21)
formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

f_handler = RotatingFileHandler('logs.log', maxBytes=5 * 1024 * 1024, backupCount=2, errors='ignore',)
f_handler.setFormatter(formater)
# s_handler = logging.StreamHandler()
# s_handler.setFormatter(formater)
logger.addHandler(f_handler)
# logger.addHandler(s_handler)


if not os.path.exists(fr"{os.getcwd()}/reports"):
    os.mkdir(fr"{os.getcwd()}/reports")


# path_to_excel_file = input("Укажите путь для excel таблицы:")
# req_limit = int(input("Укажите лимит запросов:"))

options = Options()
options.add_argument('--headless')

# client = Client(name='my_session', api_id=data['api_id_tg'], api_hash=data['api_hash_tg'])
# bot_id = data['bot_id']



class PhoneSearchProcess(QThread):
    def __init__(self, file_path, log_browse, req_limit, data, parent=None):
        self.file_path = file_path
        self.log_browse = log_browse
        self.req_limit = req_limit
        self.data = data
        QThread.__init__(self, parent)

        try:
            self.client = Client(name='my_session', api_id=self.data['api_id_tg'], api_hash=self.data['api_hash_tg'])
            self.bot_id = self.data['bot_id']
            self.driver = webdriver.Chrome(options=options)
        except Exception as init_ex:
            self.add_log(f"init ERROR", f"<span style='color:#f25633;font-weight:bold;'>init ERROR</span>  ")
            logger.error('init ERROR:', exc_info=init_ex)


    def run(self):
        self.start_searching()


    def add_log(self, t, custom_t=None):
        logger.log(21, f"{t}")
        self.log_browse.append(f"{custom_t or t}")

    def start_searching(self):
        try:
            self.add_log('start')
            self.client.start()
            last_msg_id = next(self.client.get_chat_history(self.bot_id, limit=1, offset_id=-1)).id
            # last_msg_id = None

            df = pd.read_excel(self.file_path, header=0, dtype=object, na_filter=False)  # usecols=[0,1]
            company_info = dict()
            for id in df[df['Название компании (полное)'].str.contains('\"')].index:
                if df.loc[id]['ФИО руководителя'] != '':
                    company_info[df.loc[id]['Название компании (полное)']] = {"director": df.loc[id]['ФИО руководителя'],
                                                                              "company_inn": None}
            # print(name_list)

            self.add_log("Поиск ИНН для компаний...", f"<span style='font-weight:bold;'>Поиск ИНН для компаний...</span>  ")

            with Dadata(self.data['api_key_dd'], self.data['api_secret_key_dd']) as dadata:
                for id, company_name in enumerate(company_info):
                    if id % 5 == 1:
                        time.sleep(1)
                    try:
                        clear_name = company_name[company_name.find('"') + 1:-1]
                        company_inn = None
                        for d in dadata.suggest(name="party",
                                                query=f"{clear_name} {company_info[company_name]['director']}"):
                            if d['data']['management']['name'] == company_info[company_name]['director']:
                                company_inn = d['data']['inn']
                                company_info[company_name]['company_inn'] = company_inn
                                # self.add_log(f"{company_name}, ИНН: {company_inn} ({id + 1}/{self.req_limit})")
                                self.add_log(f"{company_name}, ИНН: {company_inn} ({id + 1}/{self.req_limit})",
                                             f"{company_name}, ИНН: <span style='color:green;font-weight:bold;'>"
                                             f"{company_inn}</span> ({id + 1}/{self.req_limit})")
                                break
                        if company_inn == None:
                            # self.add_log(f"- {company_name}, ИНН: НЕ НАЙДЕН ({id + 1}/{self.req_limit})")
                            self.add_log(f"- {company_name}, ИНН: НЕ НАЙДЕН ({id + 1}/{self.req_limit})",
                                         f"{company_name}, ИНН: <span style='color:#f25633;font-weight:bold;'>"
                                         f"НЕ НАЙДЕН</span> ({id + 1}/{self.req_limit})")
                    except Exception as comp_inn_ex:
                        self.add_log(f"Get Company INN ERROR",f"<span style='color:#f25633;font-weight:bold;'>Get Company INN ERROR</span>  ")
                        logger.error('Get Company INN ERROR:', exc_info=comp_inn_ex)

                    if id + 1 == self.req_limit:
                        break

            # print(company_info)

            self.add_log("Поиск ИНН для руководителей...", f"<span style='font-weight:bold;'>Поиск ИНН для руководителей...</span>  ")

            for id, company_name in enumerate(company_info):
                try:
                    self.client.send_message(self.bot_id, fr"/inn {company_info[company_name]['company_inn']}")
                    while True:
                        time.sleep(2)
                        msg = next(self.client.get_chat_history(self.bot_id, limit=1, offset_id=-1))
                        if not msg.outgoing and msg.id != last_msg_id:
                            last_msg_id = msg.id
                            # print(msg.text)
                            inn_search = re.search(fr"{company_info[company_name]['director']} \(ИНН \d+\)", msg.text)
                            if inn_search:
                                inn = re.search(r"\d+", inn_search.group()).group()
                                df.loc[df['Название компании (полное)'] == company_name, 'Инн'] = inn
                                # self.add_log(f"{company_info[company_name]['director']}, ИНН: {inn} ({id + 1}/{self.req_limit})")
                                self.add_log(f"{company_info[company_name]['director']}, ИНН: {inn} ({id + 1}/{self.req_limit})",
                                             f"{company_info[company_name]['director']}, ИНН: <span style='color:green;font-weight:bold;'>"
                                             f"{inn}</span> ({id + 1}/{self.req_limit})")
                            else:
                                # self.add_log(f"- {company_info[company_name]['director']}, ИНН: НЕ НАЙДЕН ({id + 1}/{self.req_limit})")
                                self.add_log(f"- {company_info[company_name]['director']}, ИНН: НЕ НАЙДЕН ({id + 1}/{self.req_limit})",
                                             f"{company_info[company_name]['director']}, ИНН: <span style='color:#f25633;font-weight:bold;'>"
                                             f"НЕ НАЙДЕН</span> ({id + 1}/{self.req_limit})")
                            break

                        self.add_log('waiting...')

                except Exception as get_director_ex:
                    # print(get_director_ex)
                    self.add_log(f"Get Director INN ERROR",
                                 f"<span style='color:#f25633;font-weight:bold;'>Get Director INN ERROR</span>  ")
                    logger.error('Get Director INN ERROR:', exc_info=get_director_ex)
                if id + 1 == self.req_limit:
                    break

            self.add_log("Поиск Телефонных номеров...", f"<span style='font-weight:bold;'>Поиск Телефонных номеров...</span>  ")

            inn_list = []
            for id, i in enumerate(df[df['Инн'] != '']['Инн']):
                inn_list.append(i)
                if id >= self.req_limit - 1:
                    break
            # print(inn_list)

            total_count = len(inn_list)
            for cur_id, inn in enumerate(inn_list):
                try:
                    skip = False
                    self.client.send_message(self.bot_id, inn)
                    while True:
                        time.sleep(2)
                        msg = next(self.client.get_chat_history(self.bot_id, limit=1, offset_id=-1))
                        if not msg.outgoing and msg.id != last_msg_id:
                            last_msg_id = msg.id
                            # print('MSG:')
                            # print(msg.text)
                            if 'Обнаружен идентификатор' in msg.text:
                                # print('OK')
                                try:
                                    msg.click('ИНН (физ. лицо)')
                                except TimeoutError:
                                    pass
                                except Exception as ph_ex:
                                    self.add_log(f"ph_ex ERROR", f"<span style='color:#f25633;font-weight:bold;'>ph_ex ERROR</span>  ")
                                    logger.error('ph_ex ERROR:', exc_info=ph_ex)
                                    skip = True
                            else:
                                skip = True
                                # self.add_log(f"{inn} skip")
                                self.add_log(f"{inn} skip",
                                             f"<span style='color:#f25633;font-weight:bold;'>{inn} skip</span>  ")
                            break
                        self.add_log('waiting...')
                    if skip:
                        continue

                    while True:
                        time.sleep(2)
                        msg = next(self.client.get_chat_history(self.bot_id, limit=1, offset_id=-1))
                        if not msg.outgoing and msg.id != last_msg_id:
                            last_msg_id = msg.id
                            # print('MSG 2:')
                            # print(msg.text)
                            url = msg.reply_markup.inline_keyboard[0][0].url
                            self.driver.get(url=url)
                            time.sleep(1)
                            soup = BeautifulSoup(self.driver.page_source, "lxml")
                            phone_div = soup.find("div", class_="report-card__label", string="Телефон")

                            phones_list = ''
                            if phone_div:
                                phones = phone_div.find_previous().find_all("span")
                                for phone in phones:
                                    phone = phone.text.strip()
                                    if phone[0] == '+':
                                        phone = phone[1:]
                                    phone = phone[:11]
                                    phones_list += f"{phone}, "
                                    # print(phone)

                                phones_list = phones_list[:-2]
                                df.loc[df['Инн'] == inn, 'Телефоны'] = phones_list
                            else:
                                reports_div = soup.find("h2", class_="report-card__title",
                                                        string="Отчёты по найденным лицам").parent
                                if not reports_div:
                                    break

                                person = reports_div.find("div", class_="requests-tags")
                                if not person:
                                    break

                                url_path = person.a.get('data-modal-settings')
                                url_path = re.search(r'"src": .+', url_path).group()[8:-2]

                                url = rf"https://dc6.sherlock-report.at{url_path}"
                                self.driver.get(url=url)
                                time.sleep(1)
                                soup = BeautifulSoup(self.driver.page_source, "lxml")
                                new_phone_div = soup.find("div", class_="report-card__label", string="Телефон")

                                if new_phone_div:
                                    phones = new_phone_div.find_previous().find_all("span")
                                    for phone in phones:
                                        phone = phone.text.strip()
                                        if phone[0] == '+':
                                            phone = phone[1:]
                                        phone = phone[:11]
                                        phones_list += f"{phone}, "

                                    phones_list = phones_list[:-2]
                                    df.loc[df['Инн'] == inn, 'Телефоны'] = phones_list

                            # self.add_log(f"ИНН: {inn}, url: {url}\n"
                            #         f"Телефоны: {phones_list} \n({cur_id + 1}/{total_count})")
                            self.add_log(
                                f"ИНН: {inn}, url: {url}\n"
                                    f"Телефоны: {phones_list} \n({cur_id + 1}/{total_count})",
                                f"ИНН: {inn}, url: <a href='{url}' style='color:#3d85f2;'>{url}</a><br>"
                                f"Телефоны: <span style='color:green;'>{phones_list}</span><br>({cur_id + 1}/{total_count})")

                            break
                        self.add_log('waiting...')
                except Exception as phone_get_er:
                    self.add_log(f"Get Phone ERROR", f"<span style='color:#f25633;font-weight:bold;'>Get Phone ERROR</span>  ")
                    logger.error('Get Phone ERROR:', exc_info=phone_get_er)

            df.to_excel(fr"{os.getcwd()}/reports/result {datetime.datetime.now().strftime(('%Y_%m_%d %H-%M-%S'))}.xlsx", index=False)

        except Exception as main_ex:
            self.add_log(f"ERROR", f"<span style='color:#f25633;font-weight:bold;'>ERROR</span>  ")
            logger.error('ERROR:', exc_info=main_ex)
        finally:
            try:
                self.client.stop()
            except:
                self.add_log("error client.stop")
            try:
                self.driver.quit()
            except:
                self.add_log("error driver.quit")
            self.add_log('finish')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.Logs_textBrowser.document().setMaximumBlockCount(200)
        self.Logs_textBrowser.setOpenExternalLinks(True)

        self.Start_Button.clicked.connect(self.StartSearching)
        # self.Start_Button.clicked.connect(self.StartSearching)
        self.ToDir_Button.clicked.connect(lambda: os.startfile(fr"{os.getcwd()}/reports"))
        self.FileBrowse_Button.clicked.connect(self.FileSelect)
        self.SaveButton.clicked.connect(self.SaveSettings)

    def StartSearching(self):
        if not os.path.exists(fr"{os.getcwd()}/Settings.txt"):
            self.Logs_textBrowser.append(f"<span style='color:#ed6226;font-weight:bold;'>Заполните настройки!</span>  ")
            return
        if not self.Path_lineEdit.text():
            self.Logs_textBrowser.append(f"<span style='color:#ed6226;font-weight:bold;'>Необходимо указать путь к excel файлу!</span>  ")
            return
        if not os.path.exists(self.Path_lineEdit.text()):
            return

        properties = ["api_id_tg:", "api_hash_tg:", "bot_id:", "api_key_dd:", "api_secret_key_dd:"]
        self.data = dict()

        with open('Settings.txt', 'r', encoding='utf-8') as settings:
            for i in range(len(properties)):
                line = settings.readline()
                self.data[line.strip().split(':')[0]] = line.lstrip(properties[i]).strip() or None

        self.PSP = PhoneSearchProcess(file_path=self.Path_lineEdit.text(), log_browse=self.Logs_textBrowser,
                                      req_limit=self.Limit_spinBox.value(), data=self.data)
        if not self.PSP.isRunning():
            self.PSP.start()


    def FileSelect(self):
        file_name = QFileDialog.getOpenFileName(filter='Excel File (*.xlsx *.xls)')[0]
        if file_name:
            self.Path_lineEdit.setText(file_name)

    def SaveSettings(self):
        try:
            with open('Settings.txt', 'w', encoding='utf-8') as settings:
                settings.write(f"api_id_tg:{self.api_id_tg_lineEdit.text()}\n")
                settings.write(f"api_hash_tg:{self.api_hash_tg_lineEdit.text()}\n")
                bot_id = f"{self.bot_id_lineEdit.text()}"
                if len(bot_id) >= 1 and bot_id[0] == '@':
                    bot_id = bot_id[1:]
                settings.write(f"bot_id:{bot_id}\n")
                settings.write(f"api_key_dd:{self.api_key_dd_lineEdit.text()}\n")
                settings.write(f"api_secret_key_dd:{self.api_secret_key_dd_lineEdit.text()}\n")

            self.Logs_textBrowser.append(f"<span style='color:green;'>Настройки сохранены</span>  ")
        except Exception as save_ex:
            self.Logs_textBrowser.append(f"<span style='color:#ed6226;font-weight:bold;'>SaveSettings ERROR</span>  ")
            logger.error('SaveSettings ERROR:', exc_info=save_ex)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

    # try:
    #     main()
    # except Exception as ex:
    #     logger.error('ERROR:', exc_info=ex)
    # input()