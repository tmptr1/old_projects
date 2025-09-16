'''
Скачивает поступившые на почту прайсы
'''
import time
import datetime
from PyQt5 import QtCore
import sys
import psycopg2
import openpyxl
from zipfile import ZipFile
import os
import aspose.zip as az
import shutil
import imaplib
import email
from email.header import decode_header
import logging
from logger import configure_logging
from info_module import info_module
import chardet

MODULE_NUM = 0
InfoModule = None

logger = logging.getLogger(__name__)
configure_logging(logger, 'logs/mail_parser.log')


host = ''
user = ''
password = ''
db_name = ''
pause = False
mail_login = ''
mail_password = ''
Dir = ''
letters_b = set()

class mail_parser:
    def __init__(self, cls):
        self.main_ui = cls
        global host, user, password, db_name, mail_login, mail_password, Dir, InfoModule
        InfoModule = info_module(cls, module_num=MODULE_NUM)
        host = self.main_ui.host
        user = self.main_ui.user
        password = self.main_ui.password
        db_name = self.main_ui.db_name
        mail_login = self.main_ui.mail_login
        mail_password = self.main_ui.mail_password
        Dir = self.main_ui.Dir


    def start(self):
        self.act = Action(self)
        self.act.startSignal.connect(self.setOffButtons)
        self.t = QtCore.QThread()
        self.act.moveToThread(self.t)
        self.t.started.connect(self.act.start)
        self.act.finishSignal.connect(self.t.quit)
        self.act.finishSignal.connect(self.setModuleStatusPause)

        self.main_ui.Module_status_1.setText("Работает")
        self.main_ui.Module_status_1.setStyleSheet(f"color: green;")
        self.t.start()

        self.act.finishSignal.connect(self.setOnButtons)
        self.act.finishSignal.connect(self.resetPause)

    def setModuleStatusPause(self):
        self.main_ui.Module_status_1.setText("Пауза")
        self.main_ui.Module_status_1.setStyleSheet(f"color: red;")

    def setOffButtons(self):
        self.main_ui.StartButton_2.setEnabled(False)

    def setOnButtons(self):
        self.main_ui.StartButton_2.setEnabled(True)

    def resetPause(self):
        self.main_ui.Pause_2.setChecked(False)
        global pause
        pause = False

    def stop(self):
        global pause
        pause = not pause


class Action(QtCore.QObject):
    startSignal = QtCore.pyqtSignal(int)
    finishSignal = QtCore.pyqtSignal(int)

    def __init__(self, mainApp=None):
        super(Action, self).__init__()
        self.mainApp = mainApp

    def get_mail(self, id, mail):
        try:
            _, res = mail.uid('fetch', id, "(RFC822)")
            raw_email = res[0][1]
            msg = email.message_from_string(raw_email.decode("utf-8"))
            if msg['X-Envelope-From']:
                sender = msg['X-Envelope-From']
            else:
                sender = msg['Return-path']

            # удаление папки для временных файлов из архивов
            tmp_dir = r"tmp"
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)

            # удаление старых архивов
            tmp_archive_dir = r'Archives'
            for f in os.listdir(tmp_archive_dir):
                os.remove(f"{tmp_archive_dir}/{f}")

            logger.info(f"Sender: {sender}")
            try:
                header = decode_header(msg['Subject'])[0][0].decode()
            except:
                header = decode_header(msg['Subject'])[0][0]
            logger.info(f"Header: {header}")

            rcv = msg.get('Received')
            received_time = rcv.split(',')[-1].strip().replace(':', '-').split()[:-1]
            received_time = ' '.join(received_time)
            logger.info(f"Date: {received_time}")

            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cur:
                sender = sender.replace('\'', '\'\'')
                cur.execute(f"SELECT Имя_файла, Условие_имени_файла, Код_прайса FROM Настройки_прайса_поставщика WHERE LOWER(Почта) = LOWER('{sender}') and Сохраняем = 'ДА'")
                data = cur.fetchall()
            connection.close()
            if not data:
                logger.info('Не подходит')
                logger.info('=' * 20)
                return

            self.load_content(msg, tmp_archive_dir, tmp_dir, data, host, user, password, db_name, sender, received_time)

            logger.info('=' * 20)
        except Exception as ex:
            logger.error("get_mail error:", exc_info=ex)
            InfoModule.increase_error_count()

    def load_content(self, message, tmp_archive_dir, tmp_dir, data, host, user, password, db_name, sender, received_time):
        '''Скачивает необходимые файлы, в случае с архивами, скачивает полный архив в папку Archives, далее распаковывает
        его в папку tmp, нужные файлы переносит в папку для сырых прайсов'''
        for part in message.walk():
            if part.get_content_disposition() == 'attachment':

                if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
                    try:
                        enc = chardet.detect(decode_header(part.get_filename())[0][0])['encoding']
                        # print(enc)
                        name = decode_header(part.get_filename())[0][0].decode(enc)
                        # print(name)
                    except:
                        name = part.get_filename()
                    # print(name)
                    # name = None
                    # try:
                    #     name = decode_header(part.get_filename())[0][0].decode()
                    # except:
                    #     if not name:
                    #         try:
                    #             name = decode_header(part.get_filename())[0][0].decode('windows-1251')
                    #         except:
                    #             name = part.get_filename()

                    logger.info(name)

                    file_format = name.split('.')[-1]

                    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
                    with connection.cursor() as cur:
                        # обработка архивов
                        if file_format in ('zip', 'rar'):
                            path_to_archieve = f'{tmp_archive_dir}/{name}'
                            open(path_to_archieve, 'wb').write(part.get_payload(decode=True))
                            if not os.path.exists(tmp_dir):
                                os.mkdir(tmp_dir)
                            if file_format == 'zip':
                                with ZipFile(path_to_archieve, 'r') as archive:
                                    archive.extractall(path=tmp_dir)
                            elif file_format == 'rar':
                                with az.rar.RarArchive(path_to_archieve) as archive:
                                    archive.extract_to_directory(tmp_dir)
                            os.remove(path_to_archieve)

                            for f in os.listdir(tmp_dir):
                                is_loaded = False
                                for d_name in data:
                                    if self.check_file_name(f, d_name[0], d_name[1]):
                                        price_code = str(d_name[2])
                                        self.del_duplicates(price_code, id)
                                        addition = f"{d_name[0]}.{f.split('.')[-1]}"
                                        if d_name[1] == 'Равно':
                                            addition = ".".join(addition.split('.')[:-1])
                                        shutil.move(f"{tmp_dir}/{f}", f"{Dir}/{price_code} {addition}")
                                        logger.info(f"+ ({price_code}) - {f}")
                                        is_loaded = True
                                        break
                                if not is_loaded:
                                    cur.execute(f"delete from mail_report_tab where sender = '{sender}' and file_name = '{f}'")
                                    cur.execute(f"insert into mail_report_tab values('{sender}', '{f}', '{received_time}')")

                            shutil.rmtree(tmp_dir)
                            continue

                        # обработка других файлов
                        is_loaded = False
                        for d_name in data:
                            if self.check_file_name(name, d_name[0], d_name[1]):
                                price_code = str(d_name[2])
                                self.del_duplicates(price_code, id)
                                addition = f"{d_name[0]}.{name.split('.')[-1]}"
                                if d_name[1] == 'Равно':
                                    addition = ".".join(addition.split('.')[:-1])
                                open(f"{Dir}/{price_code} {addition}", 'wb').write(part.get_payload(decode=True))
                                logger.info(f"+ ({price_code}) - {name}")
                                is_loaded = True
                                break
                        if not is_loaded:
                            cur.execute(f"delete from mail_report_tab where sender = '{sender}' and file_name = '{name}'")
                            cur.execute(f"insert into mail_report_tab values('{sender}', '{name}', '{received_time}')")

                    connection.commit()
                    connection.close()


    def del_duplicates(self, file_code, id):
        '''Удаляет файл при совпадении первых 4 символов (код прайса)'''
        try:
            for i in os.listdir(Dir):
                try:
                    if ".".join(i.split('.')[:-1])[:4] == file_code:
                        os.remove(f"{Dir}/{i}")

                except Exception as e:
                    global letters_b
                    if id in letters_b:
                        letters_b.remove(id)
                    logger.error(f"del error ({file_code}):", exc_info=e)
                    InfoModule.increase_error_count()

        except Exception as ex:
            logger.error("del_duplicates error:", exc_info=ex)
            InfoModule.increase_error_count()


    def check_file_name(self, file_name, file_db_name, type):
        try:
            if not file_db_name:
                return 0

            if type == 'Равно':
                if file_name == file_db_name:
                    return 1
                return 1 if ".".join(file_name.split('.')[:-1]) == file_db_name else 0
            elif type == 'Содержит':
                return 1 if file_db_name in file_name else 0
            elif type == 'Начинается':
                if len(file_name) < len(file_db_name):
                    return 0
                return 1 if file_name[:len(file_db_name)] == file_db_name else 0
            elif type == 'Заканчивается':
                if len(file_name) < len(file_db_name):
                    return 0
                return 1 if file_name[-len(file_db_name):] == file_db_name else 0
            else:
                return 0

        except Exception as ex:
            logger.error("Error:", exc_info=ex)
            InfoModule.increase_error_count()
            return 0


    def start(self):
        '''Проверяет наличие новых писем за текущий день, скачивает необходимые файлы из них'''
        logger.info('start')
        self.startSignal.emit(1)
        wait_sec = 600
        global pause, mail_login, mail_password, letters_b
        t = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d-%b-%Y")
        now_time = datetime.datetime.now().strftime("%d-%b-%Y")
        # print(t)
        # res: [b'79912 79913 79914 79915 79916 79917 79918 79919 79920 79921 79922 79923 79924 79925 79926 79927 79928 79929 79930 79931 79932 79933 79934 79935 79936 79937 79938 79939 79940 79941 79942 79943 79944 79945 79946 79947 79948 79949 79950 79951 79952 79953 79954 79955 79956 79957 79958 79959 79960 79961 79962 79963 79964 79965 79966 79967 79968 79969 79970 79971 79972 79973 79974 79975 79976 79977 79978 79979 79980 79981 79982 79983 79984 79985 79986 79987 79988 79989 79990 79991 79992 79993 79994 79995 79996 79997 79998 79999 80000 80001 80002 80003 80004 80005 80006 80007 80008 80009 80010 80011 80012 80013 80014 80015 80016 80017 80018 80019 80020 80021 80022 80023 80024 80025 80026 80027 80028 80029 80030 80031 80032 80033 80034 80035 80036 80037 80038 80039 80040 80041 80042 80043 80044 80045 80046 80047 80048 80049 80050 80051 80052 80053 80054 80055 80056 80057 80058 80059 80060 80061 80062 80063 80064 80065 80066 80067 80068 80069 80070 80071 80072 80073 80074 80075 80076 80077 80078 80079 80080 80081 80082 80083 80084 80085 80086 80087 80088 80089 80090 80091 80092 80093 80094 80095 80096 80097 80098 80099 80100 80101 80102 80103 80104 80105 80106 80107 80108 80109 80110 80111 80112 80113 80114 80115 80116 80117 80118 80119 80120 80121 80122 80123 80124 80125 80126 80127 80128 80129 80130 80131 80132 80133 80134 80135 80136 80137 80138 80139 80140 80141 80142 80143 80144 80145 80146 80147 80148 80149 80150 80151 80152 80153 80154 80155 80156 80157 80158 80159 80160 80161 80162 80163 80164 80165 80166 80167 80168 80169 80170 80171 80172 80173 80174 80175 80176 80177 80178 80179 80180 80181 80182 80183 80184 80185 80186 80187 80188 80189 80190 80191 80192 80193 80194 80195 80196 80197 80198 80199 80200 80201 80202 80203 80204 80205 80206 80207 80208']
        # res: [b'79912 79913 79914 79915 79916 79917 79918 79919 79920 79921 79922 79923 79924 79925 79926 79927 79928 79929 79930 79931 79932 79933 79934 79935 79936 79937 79938 79939 79940 79941 79942 79943 79944 79945 79946 79947 79948 79949 79950 79951 79952 79953 79954 79955 79956 79957 79958 79959 79960 79961 79962 79963 79964 79965 79966 79967 79968 79969 79970 79971 79972 79973 79974 79975 79976 79977 79978 79979 79980 79981 79982 79983 79984 79985 79986 79987 79988 79989 79990 79991 79992 79993 79994 79995 79996 79997 79998 79999 80000 80001 80002 80003 80004 80005 80006 80007 80008 80009 80010 80011 80012 80013 80014 80015 80016 80017 80018 80019 80020 80021 80022 80023 80024 80025 80026 80027 80028 80029 80030 80031 80032 80033 80034 80035 80036 80037 80038 80039 80040 80041 80042 80043 80044 80045 80046 80047 80048 80049 80050 80051 80052 80053 80054 80055 80056 80057 80058 80059 80060 80061 80062 80063 80064']

        while True:
            if pause:
                logger.info("Пауза")
                self.finishSignal.emit(1)
                return

            # logger.info("")
            InfoModule.set_update_time(MODULE_NUM, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            try:
                mail = imaplib.IMAP4_SSL(host='imap.yandex.ru', port=993)
                mail.login(mail_login, mail_password)
                mail.select("inbox")
                # self.get_mail("80068", mail) # unusual encoding
                # self.get_mail("80204", mail) # average price
                # self.get_mail("80145", mail) # MIK (zip)
                # self.get_mail("83545", mail)
                # return # for test
                _, res = mail.uid('search', '(SINCE "' + t + '")', "ALL")
                letters_id = res[0].split()[:]

                if letters_id:
                    if letters_id[0] == b'[UNAVAILABLE]':
                        logger.info('UNAVAILABLE')
                        time.sleep(wait_sec)
                        continue

                    for i in letters_id:
                        if pause:
                            logger.info("Пауза")
                            self.finishSignal.emit(1)
                            return

                        if i not in letters_b:
                            letters_b.add(i)
                            logger.info(str(i))
                            self.get_mail(i, mail) # получение необходимых файлов из письма

                    if now_time < (datetime.datetime.now()).strftime("%d-%b-%Y"):
                        now_time = (datetime.datetime.now()).strftime("%d-%b-%Y")
                        t = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d-%b-%Y")

                        _, yesterday_id_list = mail.uid('search', '(SINCE "' + (
                                    datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
                            "%d-%b-%Y") + '" BEFORE "' + datetime.datetime.now().strftime(
                            "%d-%b-%Y") + '")', "ALL")
                        letters_b = set(yesterday_id_list[0].split()[:])
                        logger.info('=' * 20)
                        logger.info('Обновление времени') # обновление времени при наутуплении следующего дня
                        logger.info('=' * 20)

                # проверка на паузу
                for i in range(wait_sec):
                    if pause:
                        logger.info("Пауза")
                        self.finishSignal.emit(1)
                        return
                    time.sleep(1)

            except Exception as ex:
                logger.error("ERROR:", exc_info=ex)
                InfoModule.increase_error_count()
                # проверка на паузу
                for i in range(wait_sec):
                    if pause:
                        logger.info("Пауза")
                        self.finishSignal.emit(1)
                        return
                    time.sleep(1)
