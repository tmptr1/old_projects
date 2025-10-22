import time
# import pickle
# import json
import os
import re
# import pywhatkit
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
driver = webdriver.Chrome(service=service, options=option)
# URL = r'https://web.whatsapp.com/'


with open('config.txt', 'r', encoding='utf-8') as f:  # windows-1251
    delay = f.readline().strip()
    delay = int(delay)
    table_name = f.readline().strip()
    # t2 = int(t2)

logger = logging.getLogger('logs.log')
logger.setLevel(21)
formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

f_handler = RotatingFileHandler('logs.log', maxBytes=5 * 1024 * 1024, backupCount=2, errors='ignore',)
f_handler.setFormatter(formater)
s_handler = logging.StreamHandler()
s_handler.setFormatter(formater)
logger.addHandler(f_handler)
logger.addHandler(s_handler)

# def save_cookies():
#     try:
#         driver.get(url=URL)
#         time.sleep(5)
#         _ = input('Нажмите Enter чтобы продолжить')
#         # with open('my_cookiesb.pkl', 'wb') as cookie_file:
#         #     pickle.dump(driver.get_cookies(), cookie_file)
#         # # with open('my_cookies.json', 'w') as cookie_file:
#         # #     json.dump(driver.get_cookies(), cookie_file)
#         print('cookies данной сессии сохранены')
#     except Exception as ex:
#         logger.error('save_cookies ERROR: ', exc_info=ex)
#     finally:
#         driver.close()
#         driver.quit()
#
# def send_messages():
#     try:
#         driver.get(url=URL)
#         driver.delete_all_cookies()
#         time.sleep(2)
#         for cookie in pickle.load(open('my_cookiesb.pkl', 'rb')):
#             driver.add_cookie(cookie)
#         time.sleep(2)
#         # with open('my_cookies.json', 'r') as cookies_file:
#         #     cookies = json.load(cookies_file)
#         # for cookie in cookies:
#         #     driver.add_cookie(cookie)
#         time.sleep(3)
#         print('add')
#         driver.get(url=URL)
#         print('get')
#         time.sleep(3)
#         driver.refresh()
#         print('ref')
#         _ = input('Нажмите Enter для продолжения')
#         # with open('my_cookies', 'wb') as cookie_file:
#         #     pickle.dump(driver.get_cookies(), cookie_file)
#         # print('cookies данной сессии сохранены')
#     except Exception as ex:
#         logger.error('save_cookies ERROR: ', exc_info=ex)
#     finally:
#         driver.close()
#         driver.quit()
def save_profile():
    try:
        driver.get(url=r'https://web.whatsapp.com/')
        time.sleep(5)
        _ = input('Авторизуйтесь в WhatsApp и нажмите Enter для продождения')
    except Exception as ex:
        logger.error('save_profile ERROR: ', exc_info=ex)
    # finally:
    #     driver.quit()

def send_messages():
    try:
        start = int(input('Начать со строки: '))
        rows_count = int(input('Взять строк: '))
        fail_send = 0
        invalid_phones = 0
        # table_name = 'test.xlsx'
        table = pd.read_excel(table_name, usecols=['Имя', 'Мобильный телефон'],
                              skiprows=range(1, start-1), nrows=rows_count, header=0)
        # table = pd.read_excel('test.xlsx', usecols=['Имя', 'Мобильный телефон'],
        #                       skiprows=range(1, 1), nrows=5, header=0)
        # print(table)

        # driver = webdriver.Chrome(service=service, options=option)

        with open('send.txt', 'r', encoding='utf-8') as f: # windows-1251
            send_msg = f.read()
            send_msg = send_msg.replace('\n', '%0A')

        for name, phone in table.values:
            try:
                name = name.split(' ')[0].title()
                if phone[0] == '8':
                    phone = f"7{phone[1:]}"
                # elif phone[0] == '7':
                #     phone = f"+{phone}"
                phone = re.sub(r'\D', '', phone)
                logger.log(21, f"[{start}] {name}, {phone}")
                # pywhatkit.sendwhatmsg_instantly(phone_no=str(phone), message=send_msg.format(name=name), wait_time=t1, tab_close=True)
                url = fr"https://web.whatsapp.com/send?phone={phone}&text={send_msg.format(name=name)}"
                driver.get(url=url)

                phone_error = False
                while driver.page_source.find('wds-ic-send-filled') == -1:
                    time.sleep(3)
                    if driver.page_source.find('aria-label="Номер телефона, отправленн') != -1:
                        phone_error = True
                        break
                if phone_error:
                    logger.log(21, 'Номер недействительный')
                    invalid_phones += 1
                    continue
                time.sleep(delay)

                text_div_count = len(re.findall('data-pre-plain-text', driver.page_source))
                ActionChains(driver).send_keys(Keys.ENTER).perform()
                time.sleep(delay)

                if text_div_count != len(re.findall('data-pre-plain-text', driver.page_source)):
                    logger.log(21, 'Отправлено')
                else:
                    logger.log(21, 'НЕ ОТПРАВЛЕНО!')
                    fail_send += 1

            except Exception as send_ex:
                logger.error("send msg error: ", exc_info=send_ex)
                fail_send += 1
            finally:
                start += 1

        logger.log(21, '==========')
        logger.log(21, 'Готово!')
        logger.log(21, '==========')
        if fail_send > 0:
            logger.log(21, f'Есть неотправленные сообщения! ({fail_send})')
        if invalid_phones > 0:
            logger.log(21, f'Есть недействительные номера! ({invalid_phones})')

    except Exception as ex:
        logger.error("send msg error: ", exc_info=ex)
    finally:
        driver.quit()


if __name__ == '__main__':
    # pywhatkit.sendwhatmsg_instantly(phone_no=phone, message=send_msg.format(name='Имя'), wait_time=7, tab_close=True)

    while True:
        print('1 - Начать рассылку\n2 - Авторизация')
        action = input('Выберите действие: ')
        if action == '1':
            send_messages()
        elif action == '2':
            save_profile()
    _ = input()