import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import logging
from logging.handlers import RotatingFileHandler
from config import TG_TOKEN, TP_API
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger('tg.log')
logger.setLevel(21)
formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

f_handler = RotatingFileHandler('tg.log', maxBytes=5 * 1024 * 1024, backupCount=2, errors='ignore',)
f_handler.setFormatter(formater)
logger.addHandler(f_handler)


bot = telebot.TeleBot(TG_TOKEN)
headers = {'Authorization': f'Bearer {TP_API}'}
def check_user_id(id):
    with open('users.txt', 'r') as f:
        users = f.read().split()
        users = [int(u) for u in users]
    if id not in users:
        bot.send_message(id, text=f'Для взаимодействия с ботом отправь свой ID администратору.', parse_mode='HTML')
        return False
    return True

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, f'Привет, твой ID: {message.chat.id}.\nДля получения рассылки отправь ID администратору.\n\n'
                                      f'Команды бота:\n/list - Получить список всех актуальных событий\n/info - Получить csv таблицу с заказами по событию')

@bot.message_handler(commands=['help'])
def help_command(message):
    if not check_user_id(message.chat.id):
        return
    bot.send_message(message.chat.id, text=f'Команды бота:\n/list - Получить список всех актуальных событий\n/info - '
                                      f'Получить csv таблицу с заказами по событию', parse_mode='HTML')

def show_list(chat_id, page_num):
    skip = (page_num - 1) * 10
    url = fr"https://api.timepad.ru/v1/events?limit=10&skip={skip}&sort=-starts_at&organization_ids=11111&access_statuses=private,draft,link_only,public&starts_at_min=2024-01-01"
    r = requests.get(url=url, headers=headers).json()
    total_pages = int(r['total'] / 10)
    if not len(r['values']):
        bot.send_message(chat_id, text='Событий нет', parse_mode='HTML')
        return

    keyboard = types.InlineKeyboardMarkup()
    for i in r['values']:
        # print('id:', i['id'], i['name'])
        event_name = i['name'].replace('&quot;', '"')
        keyboard.row(
            types.InlineKeyboardButton(text=f"{event_name}", callback_data=f"/info {i['id']}"))  # id: {i['id']} |

    if page_num == 1:
        left = '❌'
        prev = 1
    else:
        left = '◀️'
        prev = page_num - 1

    if page_num == total_pages:
        right = '❌'
        next = page_num
    else:
        right = '▶️'
        next = page_num + 1

    prev_btn = types.InlineKeyboardButton(text=f"{left}", callback_data=f"/list {int(prev)}")
    next_btn = types.InlineKeyboardButton(text=f"{right}", callback_data=f"/list {int(next)}")
    keyboard.row(prev_btn, next_btn)

    bot.send_message(chat_id, text=f'События (страница {page_num}/{total_pages}):', parse_mode='HTML',
                     reply_markup=keyboard)

@bot.message_handler(commands=['list'])
def orders_list(message):
    if not check_user_id(message.chat.id):
        return
    try:
        page_num = re.search(r'/list \d+', message.text)
        if not page_num:
            page_num = 1
        else:
            page_num = int(message.text[6:])
        show_list(message.chat.id, page_num)
    except Exception as ex:
        bot.send_message(message.chat.id, text='Ошибка! Возможно, некорректный номер страницы', parse_mode='HTML')

@bot.message_handler(commands=['info'])
def info_command(message):
    if not check_user_id(message.chat.id):
        return
    msg_text = message.text
    if msg_text == '/info':
        bot.send_message(message.chat.id, text='Укажите <b>id</b> события (/info <b>id</b>)', parse_mode='HTML')
        return
    event_id = re.search(r'/info \d+', msg_text)
    if not event_id:
        bot.send_message(message.chat.id, text='Некорректный <b>id</b> события', parse_mode='HTML')
        return
    event_id = msg_text[6:]
    # print(event_id)
    get_csv(event_id, message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def but_pressed(call):
    if not check_user_id(call.message.chat.id):
        return
    if call.data[:5] == '/info':
        event_id = call.data[6:]
        # print(f"{event_id=}")
        logger.log(21, f"{event_id}")
        get_csv(event_id, call.message.chat.id)
    if call.data[:5] == '/list':
        try:
            page_num = int(call.data[6:])
            show_list(call.message.chat.id, page_num)
        except Exception as ex:
            bot.send_message(call.message.chat.id, text='Ошибка! Возможно, некорректный номер страницы', parse_mode='HTML')


def get_csv(event_id, chat_id):
    try:
        csv_path = get_csv_path(event_id)
        if csv_path == None:
            bot.send_message(chat_id, text='У события нет заказов', parse_mode='HTML')
            return
        bot.send_document(chat_id, document=open(fr'{csv_path}', 'rb'))
    except Exception as ex:
        logger.error(f'get_csv {event_id} ERROR:', exc_info=ex)
        bot.send_message(chat_id, text='Ошибка! Возможно, некорректный <b>id</b> события', parse_mode='HTML')


# def get_question_list(id):
#     url = fr"https://afisha.timepad.ru/event/{id}"
#     try:
#         r = requests.get(url=url)
#         title = BeautifulSoup(r.text, "lxml").find('div', class_='t-subheader t-subheader--no-padding').text.strip()
#         title = re.sub(r'[^\w ]', '', title)
#         # print(title)
#
#         r.encoding = 'unicode_escape'
#
#         soup = BeautifulSoup(r.content.decode('unicode_escape'), "lxml")
#         q = soup.find('script', id="evModel")
#         questions_start = q.text.find('"questions":')
#         questions_end = q.text.find('"questions_count":')
#         questions = q.text[questions_start:questions_end]
#         questions = questions.split('"name":')[1:]
#         question_list = [q[1:q.find(',"description":')-1].replace('\\', "") for q in questions]
#         # print(question_list)
#         return question_list
#     except Exception as ex:
#         return []

def get_csv_path(event_id):
    # question_list = get_question_list(event_id)
    url = fr"https://api.timepad.ru/v1/events/{event_id}"
    r = requests.get(url=url, headers=headers).json()
    title = r['name'].replace('&quot;', '"')
    title = re.sub(r'[^\w ]', '', title)

    question_dict = {}
    for i in r['questions']:
        if i['field_id'] != 'subscribe_digest':
            question_dict[i['field_id']] = i['name']

    question_dict['ticket_type'] = 'Тип билета'

    df = pd.DataFrame(columns=question_dict.keys())
    empty_row = {k: '-' for k in question_dict}

    limit = 250
    indx = 0
    while True:
        url = fr"https://api.timepad.ru/v1/events/{event_id}/orders.json?limit={limit}&skip={len(df)}"
        r = requests.get(url=url, headers=headers).json()
        if r['total'] == 0:
            return None

        step = len(r['values'])
        for i in r['values']:
            for t in i['tickets']:
                new_row = empty_row.copy()
                for a in t['answers']:
                    # new_row.append(str(t['answers'][a]).replace('&quot;', '"'))
                    new_row[a] = str(t['answers'][a]).replace('&quot;', '"')
                new_row['ticket_type'] = t['ticket_type']['name']
                # print(new_row)
                # if not question_list:
                #     question_list = ['' for _ in new_row]
                #     df = pd.DataFrame(columns=question_list)
                # df.loc[indx] = new_row
                df = df._append(new_row, ignore_index=True)
                indx += 1

        if step != limit:
            break

    df = df.rename(columns={k: question_dict[k] for k in question_dict})
    df.to_csv(f"csv/{title}.csv", sep=';', index=False, encoding='windows-1251', errors='ignore')
    return f"csv/{title}.csv"



if __name__ == '__main__':
    bot.infinity_polling()

