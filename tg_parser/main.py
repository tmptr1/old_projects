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
import re
import logging
from logging.handlers import RotatingFileHandler
# pip install openpyxl

logger = logging.getLogger('logs.log')
logger.setLevel(21)
formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

f_handler = RotatingFileHandler('logs.log', maxBytes=5 * 1024 * 1024, backupCount=2, errors='ignore',)
f_handler.setFormatter(formater)
s_handler = logging.StreamHandler()
s_handler.setFormatter(formater)
logger.addHandler(f_handler)
logger.addHandler(s_handler)

properties = ["api_id_tg:", "api_hash_tg:", "bot_id:", "api_key_dd:", "api_secrey_key_dd:"]
data = dict()

with open('Settings.txt', 'r', encoding='utf-8') as settings:
    for i in range(len(properties)):
        line = settings.readline()
        data[line.strip().split(':')[0]] = line.lstrip(properties[i]).strip() or None

path_to_excel_file = input("Укажите путь для excel таблицы:")
req_limit = int(input("Укажите лимит запросов:"))

options = Options()
options.add_argument('--headless')

client = Client(name='my_session', api_id=data['api_id_tg'], api_hash=data['api_hash_tg'])
bot_id = data['bot_id']


def add_log(t):
    logger.log(21, f"{t}")

def main():
    add_log('start')
    client.start()
    last_msg_id = next(client.get_chat_history(bot_id, limit=1, offset_id=-1)).id
    # last_msg_id = None
    driver = webdriver.Chrome(options=options)


    df = pd.read_excel(path_to_excel_file, header=0, dtype=object, na_filter=False) # usecols=[0,1]
    company_info = dict()
    for id in df[df['Название компании (полное)'].str.contains('\"')].index:
        if df.loc[id]['ФИО руководителя'] != '':
            company_info[df.loc[id]['Название компании (полное)']] = {"director": df.loc[id]['ФИО руководителя'], "company_inn": None}
    # print(name_list)


    add_log("Поиск ИНН для компаний...")

    with Dadata(data['api_key_dd'], data['api_secrey_key_dd']) as dadata:
        for id, company_name in enumerate(company_info):
            if id % 5 == 1:
                time.sleep(1)
            try:
                clear_name = company_name[company_name.find('"')+1:-1]
                for d in dadata.suggest(name="party", query=f"{clear_name} {company_info[company_name]['director']}"):
                    if d:
                        company_inn = d['data']['inn']
                        company_info[company_name]['company_inn'] = company_inn
                        add_log(f"{company_name}, ИНН: {company_inn} ({id+1}/{req_limit})")
                        break
                else:
                    add_log(f"- {company_name}, ИНН: НЕ НАЙДЕН ({id + 1}/{req_limit})")
            except Exception as comp_inn_ex:
                logger.error('Get Company INN ERROR:', exc_info=comp_inn_ex)

            if id+1 == req_limit:
                break

    # print(company_info)

    add_log("Поиск ИНН для руководителей...")

    for id, company_name in enumerate(company_info):
        try:
            client.send_message(bot_id, fr"/inn {company_info[company_name]['company_inn']}")
            while True:
                time.sleep(2)
                msg = next(client.get_chat_history(bot_id, limit=1, offset_id=-1))
                if not msg.outgoing and msg.id != last_msg_id:
                    last_msg_id = msg.id
                    # print(msg.text)
                    inn_search = re.search(fr"{company_info[company_name]['director']} \(ИНН \d+\)", msg.text)
                    if inn_search:
                        inn = re.search(r"\d+", inn_search.group()).group()
                        df.loc[df['Название компании (полное)'] == company_name, 'Инн'] = inn
                        add_log(f"{company_info[company_name]['director']}, ИНН: {inn} ({id+1}/{req_limit})")
                    else:
                        add_log(f"- {company_info[company_name]['director']}, ИНН: НЕ НАЙДЕН ({id+1}/{req_limit})")
                    break

                add_log('waiting...')

        except Exception as get_director_ex:
            logger.error('Get Director INN ERROR:', exc_info=get_director_ex)
        if id + 1 == req_limit:
            break

    add_log("Поиск Телефонных номеров...")

    inn_list = []
    for id, i in enumerate(df[df['Инн'] != '']['Инн']):
        inn_list.append(i)
        if id >= req_limit-1:
            break
    # print(inn_list)

    total_count = len(inn_list)
    for cur_id, inn in enumerate(inn_list):
        try:
            skip = False
            client.send_message(bot_id, inn)
            while True:
                time.sleep(2)
                msg = next(client.get_chat_history(bot_id, limit=1, offset_id=-1))
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
                        except Exception as ex:
                            print(ex)
                            skip = True
                    else:
                        skip = True
                        add_log(f"{inn} skip")
                    break
                add_log('waiting...')
            if skip:
                continue

            while True:
                time.sleep(2)
                msg = next(client.get_chat_history(bot_id, limit=1, offset_id=-1))
                if not msg.outgoing and msg.id != last_msg_id:
                    last_msg_id = msg.id
                    # print('MSG 2:')
                    # print(msg.text)
                    url = msg.reply_markup.inline_keyboard[0][0].url
                    driver.get(url=url)
                    time.sleep(1)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    phone_div = soup.find("div", class_="report-card__label", string="Телефон")
                    if phone_div:
                        phones_list = ''
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
                    add_log(f"ИНН: {inn}, url: {url}\n"
                            f"Телефоны: {phones_list} \n({cur_id+1}/{total_count})")

                    break
                add_log('waiting...')
        except Exception as inn_get_er:
            logger.error('INN ERROR:', exc_info=inn_get_er)

    df.to_excel(f"result {datetime.datetime.now().strftime(('%Y_%m_%d %H-%M-%S'))}.xlsx", index=False)

    client.stop()
    driver.quit()
    add_log('finish')



if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        logger.error('ERROR:', exc_info=ex)
    input()

