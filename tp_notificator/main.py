from flask import Flask, request, abort, make_response
import logging
from logging.handlers import RotatingFileHandler
import hashlib
import hmac
import telebot
import datetime
from config import TG_TOKEN, TP_SECRET_KEY

logger = logging.getLogger('logs.log')
logger.setLevel(21)
formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

f_handler = RotatingFileHandler('logs.log', maxBytes=5 * 1024 * 1024, backupCount=2, errors='ignore',)
f_handler.setFormatter(formater)
# s_handler = logging.StreamHandler()
# s_handler.setFormatter(formater)
logger.addHandler(f_handler)
# logger.addHandler(s_handler)

last_req_id = None

bot = telebot.TeleBot(TG_TOKEN)

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        print(f"[{datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}] new webhook")
        global last_req_id
        if request.method == 'POST' and request.headers.get('X-Hub-Signature', None):
            body_hash = hmac.new(TP_SECRET_KEY, request.data, hashlib.sha1).hexdigest()
            post_hash = f"{request.headers.get('X-Hub-Signature', None)}".split('=')[-1]
            data = request.json
            # data = json.dumps()

            # logger.log(21, f"bh: {body_hash}, ph: {post_hash}")

            if last_req_id == data['id']:
                return 'OK', 200  # дубликат
            last_req_id = data['id']

            logger.log(21, '------')
            if body_hash != post_hash:
                logger.log(21, 'НЕОПОЗНАННЫЙ WEBHOOK')
                logger.log(21, data)
                return

            # print(data)
            # headers = dict(request.headers)
            logger.log(21, data)

            with open('users.txt', 'r') as f:
                users = f.read().split()
                users = [int(u) for u in users]

            event_name = data['event']['name']
            created_at = data['created_at'][:19].replace('T', ' ')

            for ticket in data['tickets']:
                msg = ''
                msg += f"Событие: {event_name}\n"
                msg += f"Тип билета: {ticket['ticket_type']['name']}\n"
                for i in ticket['answers']:
                    if isinstance(ticket['answers'][i], str):
                        val = ticket['answers'][i].replace('&quot;', '"')
                        if i == 'phone':
                            val = val.replace(" ", "")
                    elif isinstance(ticket['answers'][i], list):
                        val = ", ".join(ticket['answers'][i])
                    else:
                        val = ticket['answers'][i]

                    msg += f"{'Q' if i.startswith('question') else i}: {val}\n"

                msg += f"Время регистрации {created_at}\n"

                # print(msg)
                for u in users:
                    bot.send_message(chat_id=u, text=msg)



            # logger.log(21, headers)
            # logger.log(21, '------')
            # logger.log(21, f"x: {headers.get('X-Hub-Signature', None)}, sh: {headers.get('sha1', None)}")
            # logger.log(21, '---d---')
            # logger.log(21, request.data)
            # logger.log(21, '------')

            # logger.log(21, '------')
            # print(headers)

            print(f"msg id: {last_req_id}")

            return 'OK', 200
        else:
            abort(400)
    except Exception as ex:
        logger.error('ERROR:', exc_info=ex)

if __name__ == '__main__':
    app.run(host='123.456.789.01', port=8000)

