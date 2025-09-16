'''
Отправляет прайсы покупателей на указанные адреса
'''
import time
import multiprocessing as mp
import os
import shutil
import datetime
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header
from info_module import info_module
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

import psycopg2
from PyQt5 import QtCore
import logging
from logger import configure_logging

login = 'login@yandex.ru'
password_m = 'passIMAP'

logger = logging.getLogger(__name__)
configure_logging(logger, 'logs/mail_sender.log')

MODULE_NUM = 4
InfoModule = None

host = ''
user = ''
password = ''
db_name = ''
path_to_final = ''
path_to_sended = ''
mail_login = ''
mail_password = ''


class mail_sender():
    def __init__(self, cls):
        self.main_ui = cls
        global host, user, password, db_name, path_to_final, path_to_sended, InfoModule, mail_login, mail_password
        InfoModule = info_module(cls, module_num=MODULE_NUM)
        host = self.main_ui.host
        user = self.main_ui.user
        password = self.main_ui.password
        db_name = self.main_ui.db_name
        path_to_final = self.main_ui.path_to_final
        path_to_sended = self.main_ui.path_to_sended
        mail_login = self.main_ui.mail_login
        mail_password = self.main_ui.mail_password

        mp.freeze_support()

    def UpdateTable(self):
        '''Обновление таблицы с прайсами покупателей для последующей возможности выбрать и отпрвить необходимые'''
        headers = ['Имя прайса', 'Код', 'Обновить']
        self.main_ui.PricesTable_7.setColumnCount(len(headers))
        self.main_ui.PricesTable_7.setHorizontalHeaderLabels(headers)

        try:
            files = os.listdir(path_to_final)
            # print(files[0].rsplit('.csv')[0])
            # return
            if not files:
                return
            files = str(''.join([f"'{file.rsplit('.csv')[0]}', " for file in files])[:-2])
            # print(files)
            # return
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cur:
                cur.execute(f"select Имя_прайса, Код_прайса_покупателя from Настройки_прайса_покупателя where Имя_прайса in ({files})")
                data = cur.fetchall()
            connection.close()

            self.main_ui.PricesTable_7.setRowCount(len(data))
            for id, d in enumerate(data):
                self.main_ui.PricesTable_7.setItem(id, 0, QTableWidgetItem(str(d[0]))) # name
                self.main_ui.PricesTable_7.setItem(id, 1, QTableWidgetItem(str(d[1]))) # code
                sb = QtWidgets.QCheckBox()
                sb.setStyleSheet("QCheckBox::indicator { width: 70px; height: 70px;}")
                self.main_ui.PricesTable_7.setCellWidget(id, 2, sb)

        except Exception as ex:
            logger.error("[UpdateTable error]:", exc_info=ex)
            InfoModule.increase_error_count()

    def StartProcess(self):
        self.act = Action(self)
        self.t = QtCore.QThread()
        self.act.moveToThread(self.t)
        self.main_ui.StartButton_7.setEnabled(False)
        self.main_ui.SendButton_all.setEnabled(False)
        self.main_ui.SendButton_selected.setEnabled(False)
        self.t.started.connect(self.act.mainCircle)
        self.act.finishSignal.connect(self.setOnStartButton)
        self.act.finishSignal.connect(self.setModuleStatusPause)

        self.main_ui.Module_status_5.setText("Работает")
        self.main_ui.Module_status_5.setStyleSheet(f"color: green;")
        self.t.start()
        self.t.quit()

    def SendSelected(self):
        '''Отправка выбранных в таблице прайсов'''
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle('Отправка прайсов')
        msg.setText('Вы действительно хотите отправить выбранные прайсы?')

        buttonAceptar  = msg.addButton("Да", QMessageBox.YesRole)
        buttonCancelar = msg.addButton("Отменить", QMessageBox.RejectRole)
        msg.setDefaultButton(buttonAceptar)
        msg.exec_()

        if not msg.clickedButton() == buttonAceptar:
            return

        self.act2 = Action(self)
        self.t2 = QtCore.QThread()
        self.act2.moveToThread(self.t2)
        self.main_ui.StartButton_7.setEnabled(False)
        self.main_ui.SendButton_all.setEnabled(False)
        self.main_ui.SendButton_selected.setEnabled(False)
        self.t2.started.connect(self.act2.SendSelected)
        self.act2.finishSignal.connect(self.setOnStartButton)
        self.act2.finishSignal.connect(self.setModuleStatusPause)

        self.main_ui.Module_status_5.setText("Работает")
        self.main_ui.Module_status_5.setStyleSheet(f"color: green;")
        self.t2.start()
        self.t2.quit()

    def SendAll(self):
        '''Отправка всех прайсов'''
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle('Отправка прайсов')
        msg.setText('Вы действительно хотите отправить ВСЕ прайсы?')

        buttonAceptar  = msg.addButton("Да", QMessageBox.YesRole)
        buttonCancelar = msg.addButton("Отменить", QMessageBox.RejectRole)
        msg.setDefaultButton(buttonAceptar)
        msg.exec_()

        if not msg.clickedButton() == buttonAceptar:
            return

        self.act3 = Action(self)
        self.t3 = QtCore.QThread()
        self.act3.moveToThread(self.t3)
        self.main_ui.StartButton_7.setEnabled(False)
        self.main_ui.SendButton_all.setEnabled(False)
        self.main_ui.SendButton_selected.setEnabled(False)
        self.t3.started.connect(self.act3.SendAll)
        self.act3.finishSignal.connect(self.setOnStartButton)
        self.act3.finishSignal.connect(self.setModuleStatusPause)

        self.main_ui.Module_status_5.setText("Работает")
        self.main_ui.Module_status_5.setStyleSheet(f"color: green;")
        self.t3.start()
        self.t3.quit()
        
    def setModuleStatusPause(self):
        self.main_ui.Module_status_5.setText("Пауза")
        self.main_ui.Module_status_5.setStyleSheet(f"color: red;")

    def setOnStartButton(self):
        self.main_ui.StartButton_7.setEnabled(True)
        self.main_ui.SendButton_all.setEnabled(True)
        self.main_ui.SendButton_selected.setEnabled(True)



class Action(QtCore.QThread):
    '''Класс для многопоточной работы в PyQt'''
    finishSignal = QtCore.pyqtSignal(int)
    def __init__(self, mainApp=None):
        super(Action, self).__init__()
        self.mainApp = mainApp
        mp.freeze_support()

    def mainCircle(self):
        '''Основной цикл, отправляет прайсы покупателей на соответствующую почту, отправка происходит не позже указанного
        времени отправки + added_min минут'''
        wait_sec = 10

        while True:
            now1 = datetime.datetime.now()
            try:
                if self.mainApp.main_ui.Pause_7.isChecked():
                    self.mainApp.main_ui.Pause_7.setChecked(False)
                    self.finishSignal.emit(1)
                    return
                InfoModule.set_update_time(MODULE_NUM, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                with connection.cursor() as cur:
                    cur.execute(f"select Имя_прайса, Адрес_для_прайсов, Время_рассылки_прайса, "
                                f"Настройки_прайса_покупателя.Код_прайса_покупателя from Настройки_прайса_покупателя "
                                f"join (select Код_прайса_покупателя from Время_отправки_прайсов) as T on "
                                f"Настройки_прайса_покупателя.Код_прайса_покупателя = T.Код_прайса_покупателя")
                    price_list = cur.fetchall()

                    for name, address, time_list, code in price_list:
                        to_send = False
                        for t in time_list.split():
                            added_min = 10
                            try:
                                dt = datetime.datetime.strptime(t, '%H-%M')
                                if datetime.datetime.now().time() > dt.time() and (
                                        dt + datetime.timedelta(minutes=added_min)).time() > datetime.datetime.now().time():
                                    to_send = True
                                    break
                            except Exception as timeEx:
                                logger.error('time read error', exc_info=timeEx)
                                InfoModule.increase_error_count()

                        if to_send:
                            cur.execute(
                                f"select last_send_time from Время_отправки_прайсов where Код_прайса_покупателя = '{code}'")
                            last_send_time = cur.fetchone()
                            if not last_send_time:  # если прайс ещё не сформирован
                                continue
                            last_send_time = last_send_time[0]

                            if not last_send_time:  # если прайс отправляется первый раз
                                logger.info(f"Отправка {name} [{code}] ...")
                                send_email(path_to_final, name, code)
                                logger.info(f"Отправка {code} завершена")

                                cur.execute(
                                    f"update Время_отправки_прайсов set last_send_time = '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}' where Код_прайса_покупателя = '{code}'")
                                continue
                            last_send_time = datetime.datetime.strptime(f"{str(last_send_time)}", '%Y-%m-%d %H:%M:%S')
                            dt = datetime.datetime.strptime(f"{datetime.datetime.now().date()} {dt.time()}",
                                                            '%Y-%m-%d %H:%M:%S')

                            if last_send_time >= dt and last_send_time <= dt + datetime.timedelta(minutes=added_min):
                                continue
                            else:
                                logger.info(f"Отправка {name} [{code}] ...")
                                send_email(path_to_final, name, code)
                                logger.info(f"Отправка {code} завершена")
                                cur.execute(f"update Время_отправки_прайсов set last_send_time = '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}' "
                                            f"where Код_прайса_покупателя = '{code}'")
                            continue

                connection.commit()
                connection.close()

                # проверка на паузу
                now2 = datetime.datetime.now()
                if wait_sec > (now2 - now1).seconds:
                    for _ in range(wait_sec - (now2 - now1).seconds):
                        if self.mainApp.main_ui.Pause_7.isChecked():
                            self.mainApp.main_ui.Pause_7.setChecked(False)
                            self.finishSignal.emit(1)
                            return
                        time.sleep(1)

            except Exception as ex:
                logger.error("mainCycle error:", exc_info=ex)
                InfoModule.increase_error_count()
                time.sleep(5)

    def SendSelected(self):
        try:
            price_list = list()
            for i in range(self.mainApp.main_ui.PricesTable_7.rowCount()):
                if self.mainApp.main_ui.PricesTable_7.cellWidget(i, 2).checkState():
                    price_list.append(self.mainApp.main_ui.PricesTable_7.item(i, 1).text())
            # print(price_list)
            SendFromPriceList(price_list)

        except Exception as ex:
            logger.error("[SendSelected error]:", exc_info=ex)
            InfoModule.increase_error_count()
        finally:
            self.finishSignal.emit(1)

    def SendAll(self):
        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cur:
                cur.execute(f"select Настройки_прайса_покупателя.Код_прайса_покупателя from Настройки_прайса_покупателя "
                            f"join (select Код_прайса_покупателя from Время_отправки_прайсов) as T on "
                            f"Настройки_прайса_покупателя.Код_прайса_покупателя = T.Код_прайса_покупателя")
                price_list = cur.fetchall()

            connection.close()
            if not price_list:
                return
            price_list = [p[0] for p in price_list]

            SendFromPriceList(price_list)

        except Exception as ex:
            logger.error("[SendSelected error]:", exc_info=ex)
            InfoModule.increase_error_count()
        finally:
            self.finishSignal.emit(1)



def SendFromPriceList(price_list):
    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    with connection.cursor() as cur:
        for code in price_list:
            cur.execute(
                f"select Имя_прайса, Адрес_для_прайсов from Настройки_прайса_покупателя where Код_прайса_покупателя = '{code}'")
            res = cur.fetchone()
            if not res:
                continue
            name, address = res
            logger.info(f"Отправка {name} [{code}] ...")
            send_email(path_to_final, name, code)
            logger.info(f"Отправка {code} завершена")
            cur.execute(
                f"update Время_отправки_прайсов set last_send_time = '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}' "
                f"where Код_прайса_покупателя = '{code}'")
    connection.commit()
    connection.close()


def send_email(path_to_final, name, code):
    '''Отправка письма с вложенным прайсом'''
    send_to = "login@mail.ru"
    msg = MIMEMultipart()
    msg["Subject"] = Header(f"{code}")
    msg["From"] = mail_login
    msg["To"] = send_to
    # msg.attach(MIMEText("price PL3", 'plain'))

    s = smtplib.SMTP("smtp.yandex.ru", 587, timeout=100)

    try:
        s.starttls()
        s.login(mail_login, mail_password)

        file_path = rf"{path_to_final}\{name}.csv"

        with open(file_path, 'rb') as f:
            file = MIMEApplication(f.read())

        file.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        msg.attach(file)

        s.sendmail(msg["From"], send_to, msg.as_string())

        shutil.copy(file_path, fr"{path_to_sended}/{name}.csv")
    except Exception as ex:
        logger.error("send_email error:", exc_info=ex)
        InfoModule.increase_error_count()
    finally:
        s.quit()

