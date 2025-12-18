from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QThread
from main_ui import Ui_MainWindow
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from pyrogram import Client
import pyperclip
import pandas as pd
import time
import datetime
import re
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

useragrnt = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
option = webdriver.ChromeOptions()
option.add_argument(f'user-agent={useragrnt}')
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument('--allow-profiles-outside-user-dir')
option.add_argument('--enable-profile-shortcut-manager')
option.add_argument('--enable-aggressive-domstorage-flushing')

browser_profile_dir = fr"{os.getcwd()}/profile"
option.add_argument(fr"user-data-dir={browser_profile_dir}")
option.add_argument('--profile-directory=profile')

app_path = fr"{os.getcwd()}\chromedriver\chromedriver.exe"
service = Service(executable_path=app_path)


logger = logging.getLogger('logs.log')
logger.setLevel(21)
formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

f_handler = RotatingFileHandler('logs.log', maxBytes=5 * 1024 * 1024, backupCount=2, errors='ignore',)
f_handler.setFormatter(formater)
s_handler = logging.StreamHandler()
s_handler.setFormatter(formater)
logger.addHandler(f_handler)
logger.addHandler(s_handler)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # self.textBrowser.document().setMaximumBlockCount(200)
        properties = ["api_id_tg:", "api_hash_tg:", "bot_id:"]
        self.data = dict()
        with open('Settings.txt', 'r', encoding='utf-8') as settings:
            for i in range(len(properties)):
                line = settings.readline()
                self.data[line.strip().split(':')[0]] = line.lstrip(properties[i]).strip() or None

        try:
            self.driver = webdriver.Chrome(service=service, options=option)
            self.client = Client(name='my_session', api_id=self.data['api_id_tg'], api_hash=self.data['api_hash_tg'])
        except Exception as ex:
            logger.error('driver/client create ERROR: ', exc_info=ex)

        self.WorgingThread = WorkingQthread()
        self.AuthTgButton.clicked.connect(self.tg_auth)
        self.SelectFileButton.clicked.connect(self.select_file)
        self.StartButton.clicked.connect(self.start_sending)

    def __del__(self):
        try:
            self.driver.close()
            self.driver.quit()
        except Exception as ex:
            logger.error('__del__ ERROR: ', exc_info=ex)

    def tg_auth(self):
        try:
            logger.log(21, 'Авторизуйтесь в Telegram')
            self.driver.get(url=r'https://web.telegram.org/')
        except Exception as ex:
            logger.error('tg_auth ERROR: ', exc_info=ex)
    def select_file(self):
        file_path = QFileDialog.getOpenFileName(filter='Excel File (*.xlsx *.xls)')[0]
        if file_path and not self.WorgingThread.isRunning():
            try:
                self.lineEdit.setText(file_path)
                table = pd.read_excel(file_path, header=None, nrows=1, sheet_name=0)
                header = table.values
                header = list(header[0])
                self.Name_comboBox.addItems(header)
                self.Phone_comboBox.addItems(header)
                header_ = ['Status']
                header_ += header
                self.Status_comboBox.addItems(header_)
            except Exception as ex:
                logger.error('WorkingQthread ERROR: ', exc_info=ex)

    def start_sending(self):
        file_path = self.lineEdit.text()
        if not self.WorgingThread.isRunning() and file_path:

            self.WorgingThread.bot_id = self.data['bot_id']
            self.WorgingThread.client = self.client
            self.WorgingThread.driver = self.driver
            self.WorgingThread.file_path = file_path
            self.WorgingThread.phone_col = self.Phone_comboBox.currentText()
            self.WorgingThread.name_col = self.Name_comboBox.currentText()
            self.WorgingThread.status_col = self.Status_comboBox.currentText()
            self.WorgingThread.start_row = self.StartRow_spinBox.value()
            self.WorgingThread.get_rows = self.GetRow_spinBox.value()
            self.WorgingThread.delay = self.Delay_spinBox.value()

            self.WorgingThread.start()

    # def add_log(self, text):
    #     logger.log(21, f"{text}")
    #     self.textBrowser.append(f"{text}")

class WorkingQthread(QThread):
    # textSignal = Signal(str)
    bot_id = None
    client = None
    driver = None
    file_path = None
    name_col = None
    phone_col = None
    status_col = None
    start_row = None
    get_rows = None
    delay = None

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        try:
            self.client.start()
            last_msg_id = next(self.client.get_chat_history(self.bot_id, limit=1, offset_id=-1)).id

            with open('send.txt', 'r', encoding='utf-8') as f:  # windows-1251
                send_msg = f.read()

            # print(self.phone_col, self.name_col)
            table = pd.read_excel(self.file_path, header=0, nrows=self.get_rows, skiprows=range(1, self.start_row),
                                  usecols=[self.phone_col, self.name_col], sheet_name=0)
            total_table = pd.read_excel(self.file_path, header=0, sheet_name=0)

            table = table[[self.phone_col, self.name_col]]
            row = self.start_row
            id = 1
            for phone_number, name in table.values:
                try:
                    if not phone_number:
                        continue
                    if len(phone_number) < 11:
                        continue

                    name = name.split(' ')[0].title()
                    phone_number = re.sub(r'\D', '', phone_number)
                    if phone_number[0] == '8':
                        phone_number = f"7{phone_number[1:]}"

                    logger.log(21, f"[{row}] {phone_number} ...")
                    self.driver.get(fr"https://t.me/+{phone_number}")

                    while self.driver.page_source.find('tgme_page_action tgme_page_web_action') == -1:
                        time.sleep(3)

                    soup = BeautifulSoup(self.driver.page_source, "lxml")
                    div_with_href = soup.find("a", class_="tgme_action_button_new tgme_action_web_button")
                    self.driver.get(div_with_href.get('href'))
                    # ref_btn = self.driver.find_element(By.CLASS_NAME, "tgme_page_web_action")

                    # api_send = False

                    timeout = 2
                    t = 0
                    cont = True
                    while self.driver.page_source.find("editable-message-text") == -1:
                        if t > timeout:
                            cont = False
                            break
                        time.sleep(2)
                        t += 1

                    msg_txt = ''
                    if not cont:
                        self.client.send_message(self.bot_id, f"+{phone_number}")
                        # self.client.send_message(471126141, f"+{phone_number}")
                        while True:
                            time.sleep(2)
                            msg = next(self.client.get_chat_history(self.bot_id, limit=1, offset_id=-1))
                            if not msg.outgoing and msg.id != last_msg_id:
                                last_msg_id = msg.id
                                msg_txt = msg.text
                                break

                        match = re.search(r'Telegram: @\w+', msg_txt)
                        if match:
                            # tg = re.search(r'Telegram: @\w+', msg.text).group()
                            tg = match.group()
                            tg = tg[11:]
                            tg_ref = fr"https://t.me/{tg}"
                            logger.log(21, tg_ref)
                            self.driver.get(tg_ref)


                            while self.driver.page_source.find('tgme_page_action tgme_page_web_action') == -1:
                                time.sleep(2)

                            soup = BeautifulSoup(self.driver.page_source, "lxml")
                            div_with_href = soup.find("a", class_="tgme_action_button_new tgme_action_web_button")

                            self.driver.get(div_with_href.get('href'))

                            t = 0
                            while self.driver.page_source.find("editable-message-text") == -1:
                                if t > timeout:
                                    cont = False
                                    break
                                time.sleep(2)
                                t += 1
                            else:
                                cont = True
                        # elif re.search(r'Telegram: \d+', msg_txt):
                        #     tg_id = re.search(r'Telegram: \d+', msg_txt).group()
                        #     tg_id = int(tg_id[10:])
                        #     self.client.send_message(tg_id, f"{send_msg.format(name=name)}")
                        #     logger.log(21, f"Отправлено по api - id: {tg_id}")
                        #     total_table.loc[row - 1, self.status_col] = f"направлено по api {datetime.datetime.now().date().strftime('%d.%m')}"
                        #     api_send = True
                        else:
                            cont = False

                    if not cont:
                        logger.log(21, f"-- {phone_number} НЕ ОТПРАВЛЕНО! ({id}/{self.get_rows})")
                        total_table.loc[row-1, self.status_col] = f"НЕ направлено {datetime.datetime.now().date().strftime('%d.%m')}"
                        continue

                    # if not api_send:
                    msg_input = self.driver.find_element(By.ID, 'editable-message-text')
                    msg_input.clear()

                    pyperclip.copy(f"{send_msg.format(name=name)}")
                    act = ActionChains(self.driver)
                    act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
                    time.sleep(1)
                    msg_input.send_keys(Keys.ENTER)
                    logger.log(21, f"{phone_number} Отправлено ({id}/{self.get_rows})")
                    total_table.loc[row-1, self.status_col] = f"направлено {datetime.datetime.now().date().strftime('%d.%m')}"

                except Exception as ex_iter:
                    logger.error('iter ERROR: ', exc_info=ex_iter)
                finally:
                    row += 1
                    id += 1

                time.sleep(self.delay)

            # total_table.to_csv(fr"{os.path.basename(self.file_path)} {datetime.datetime.now().strftime('%Y-%m-%d (%H-%M-%S)')}.csv",
            #                    sep=';', index=False, encoding="windows-1251", errors='ignore')
            total_table.to_excel(fr"{os.path.basename(self.file_path)} {datetime.datetime.now().strftime('%Y-%m-%d (%H-%M-%S)')}.xlsx",
                               index=False)

            logger.log(21, f"================")
            logger.log(21, f"Готово!")
            logger.log(21, f"================")

        except Exception as ex:
            logger.error('WorkingQthread ERROR: ', exc_info=ex)
        finally:
            self.client.stop()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
   main()