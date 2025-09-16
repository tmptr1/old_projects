'''
Вывод информации о модулях (статус, время последней активности, счётчик ошибок)
'''
import multiprocessing as mp
import os
import datetime
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
import psycopg2
import time
import re
import logging
from logger import configure_logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import timedelta

logger = logging.getLogger(__name__)
configure_logging(logger, 'logs/info_module.log')

host = ''
user = ''
password = ''
db_name = ''
path_to_catalogs = ''
mail_login = ''
mail_password = ''

class info_module():
    def __init__(self, cls, module_num=None):
        self.main_ui = cls
        self.module_num = module_num

        global host, user, password, db_name, path_to_catalogs, mail_login, mail_password
        host = self.main_ui.host
        user = self.main_ui.user
        password = self.main_ui.password
        db_name = self.main_ui.db_name
        path_to_catalogs = self.main_ui.path_to_catalogs
        mail_login = self.main_ui.mail_login
        mail_password = self.main_ui.mail_password

        self.items = [[self.main_ui.UpdateTime_item_1, "logs/mail_parser.log", self.main_ui.textBrowser_1],
                      [self.main_ui.UpdateTime_item_2, "logs/price_reader.log", self.main_ui.textBrowser_2],
                      [self.main_ui.UpdateTime_item_3, "logs/price_proc.log", self.main_ui.textBrowser_3],
                      [self.main_ui.UpdateTime_item_4, "logs/personalization.log", self.main_ui.textBrowser_4],
                      [self.main_ui.UpdateTime_item_5, "logs/mail_sender.log", self.main_ui.textBrowser_5],
                      [self.main_ui.UpdateTime_item_6, "logs/catalog_update.log", self.main_ui.textBrowser_6]]
        self.error_counters = [self.main_ui.Errors_1, self.main_ui.Errors_2, self.main_ui.Errors_3, self.main_ui.Errors_4,
                               self.main_ui.Errors_5, self.main_ui.Errors_6]
        mp.freeze_support()

    def Start(self):
        self.act = Action(self)
        self.t = QtCore.QThread()
        self.act.moveToThread(self.t)
        self.t.started.connect(self.act.Start)

        self.t.start()

    def Create_report(self):
        self.act2 = Action(self)
        self.main_ui.create_report_button.setEnabled(False)
        self.t2 = QtCore.QThread()
        self.act2.moveToThread(self.t2)
        self.t2.started.connect(self.act2.Create_Report)

        self.t2.start()
        self.t2.quit()
    def Create_mail_report(self):
        self.act3 = Action(self)
        self.main_ui.create_mail_report_button.setEnabled(False)
        self.t3 = QtCore.QThread()
        self.act3.moveToThread(self.t3)
        self.t3.started.connect(self.act3.Create_mail_report)

        self.t3.start()
        self.t3.quit()
        # self.act2.end_signal.connect(self.setOnMailReportButton)


    def setOnMailReportButton(self):
        self.main_ui.create_mail_report_button.setEnabled(True)

    def Restart(self):
        '''Обновление счётчика ошибок'''
        for e in self.error_counters:
            e.setText('0')

    def increase_error_count(self, count=1):
        '''Увеличение счётчика ошибок'''
        self.error_counters[self.module_num].setText(str(int(self.error_counters[self.module_num].text()) + count))

    def set_update_time(self, module_id, text):
        self.items[module_id][0].setText(text)



    def reset_report(self, sql):
        '''Обнуление csv файла с отчётами о прайсах'''
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle('Обнуление отчёта')
        msg.setText('Вы действительно хотите обнулить отчёт?')

        buttonAceptar  = msg.addButton("Да", QMessageBox.YesRole)
        buttonCancelar = msg.addButton("Отменить", QMessageBox.RejectRole)
        msg.setDefaultButton(buttonAceptar)
        msg.exec_()

        if not msg.clickedButton() == buttonAceptar:
            return

        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        with connection.cursor() as cur:
            # cur.execute(f"delete from price_report")
            cur.execute(sql)
        connection.commit()
        connection.close()


class Action(QtCore.QThread):
    '''Класс для многопоточной работы'''
    finishSignal = QtCore.pyqtSignal(int)
    rowSignal = QtCore.pyqtSignal(int, str, str, int, int, int)
    end_signal = QtCore.pyqtSignal()
    def __init__(self, mainApp=None):
        super(Action, self).__init__()
        self.mainApp = mainApp

    def Start(self):
        # обновление информации по времени последней активности в модуле (по последним записям в логах)
        last_day = 0
        while True:
            try:
                now = datetime.datetime.now()

                if now.hour == 22 and now.minute == 30 and now.day != last_day:
                    er_sum = 0
                    for ec in self.mainApp.error_counters:
                        # print(ec.text())
                        er_sum += int(ec.text())
                    status = 'OK'
                    if er_sum > 50:
                        status = 'ОШИБКА'

                    check_last_day = [False, False, False, True]
                    module_names = ["Почта", "Обработка 1", "Обработка 2", "Обновление справочников"]
                    info_text = f"Ошибок: {er_sum}\nВремя последней активноси:\n"
                    items = list()
                    for i in self.mainApp.items:
                        if i[1] not in ('logs/mail_sender.log', 'logs/personalization.log'):
                            items.append(i)
                    for id, i in enumerate(items):
                        info_text += f"{module_names[id]}: "
                        try:
                            t = datetime.datetime.strptime(i[0].text(), "%Y-%m-%d %H:%M:%S")
                            # print(t, check_last_day[id])
                            info_text += f"{t.strftime("%Y-%m-%d %H:%M:%S")}"
                            if check_last_day[id]:
                                if now - timedelta(days=1) > t:
                                    status = 'ОШИБКА'
                            else:
                                if now - timedelta(hours=1) > t:
                                    status = 'ОШИБКА'
                        except:
                            status = 'ОШИБКА'

                        info_text += f"\n"

                    # print(info_text)
                    # print(status)
                    self.send_info_mail(status, info_text)
                    # print('sended')

                    last_day = now.day
                # for item, log, textB in self.mainApp.items:
                #     # item.setText(str(datetime.datetime.fromtimestamp(os.path.getctime(log)).strftime("%H:%M  %d-%m-%Y")))
                #     dtime = textB.toPlainText().split('\n')
                #     if len(dtime) >= 2:
                #         dtime = dtime[-2]
                #         dtime = re.match(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}", dtime)
                #         if dtime:
                #             item.setText(str(dtime[0][1:]))
            except Exception as ex:
                # print(ex)
                logger.error("[Error]:", exc_info=ex)
            time.sleep(10)

    def Create_Report(self):
        '''Формирование csv файла с отчётом о прайсах'''
        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            df = pd.read_sql(
                """SELECT code as "Прайс", exit1 as "Первый этап обработки", exit2 as "Второй этап обработки", 
                loaded_rows as "Загружено", unloaded_rows as "Не загружено", 
                round(loaded_rows/round(loaded_rows+unloaded_rows, 2)*100, 2) as "Процент пройденных позиций", 
                update_time as "Время последнего изменения" FROM price_report""", connection)
            df.to_csv(f"{path_to_catalogs}/Отчёт.csv", sep=';', encoding='windows-1251', index=False, errors='ignore')
            connection.close()
        except Exception as ex:
            logger.error("[Error]:", exc_info=ex)
        self.mainApp.main_ui.create_report_button.setEnabled(True)

    def Create_mail_report(self):
        '''Формирование csv файла с отчётом о письмах'''
        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            df = pd.read_sql("""select sender as "Отправитель", file_name as "Файл", date as "Время" from mail_report_tab order by sender""", connection)
            df.to_csv(f"{path_to_catalogs}/Отчёт_почта.csv", sep=';', encoding='windows-1251', index=False, errors='ignore')
            connection.close()
        except Exception as ex:
            logger.error("[Error]:", exc_info=ex)
        # self.end_signal.emit(1)
        self.mainApp.main_ui.create_mail_report_button.setEnabled(True)

    def send_info_mail(self, status, text):
        msg = MIMEText(text, "plain", "utf-8")

        msg["Subject"] = Header(f"Статус работы программы: {status}")
        msg["From"] = mail_login
        msg["To"] = "login@mail.ru"

        s = smtplib.SMTP("smtp.yandex.ru", 587, timeout=100)
        try:
            s.starttls()
            s.login(mail_login, mail_password)
            s.sendmail(msg["From"], "login@mail.ru", msg.as_string())
        except Exception as ex:
            # print(ex)
            logger.error("[Error]:", exc_info=ex)
        finally:
            s.quit()