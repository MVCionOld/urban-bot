import json
import sys
import time

import flask
import telebot

import config
import urban

bot = telebot.TeleBot(
    config.URBAN_BOT_TOKEN if len(sys.argv) == 1 else sys.argv[-1],
    threaded=True
)

urban_scrapper = urban.UrbanDictionaryScrapper()

with open('botCommands.json') as bot_activity_file:
    bot_activity = json.loads(bot_activity_file.read())

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route(config.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, bot_activity['commands'][message.text])


@bot.message_handler(commands=['mem'])
def send_mem(message):
    bot.send_message(message.chat.id, bot_activity['commands'][message.text])


@bot.message_handler(content_types=['text'])
def get_explanation(message):
    if len(message.text.split()) > 1:
        explanation = urban_scrapper.search("+".join(message.text.split()))
    else:
        explanation = urban_scrapper.search(message.text)

    if config.DEBUG and explanation is not None:
        print("[{0}, {1}]:\n{2}\n".format(message.chat.id, message.text, explanation.strip()))

    if explanation is None:
        explanation = "There is no word's '{}' explanation on Urban Dictionary."

    bot.send_message(message.chat.id, explanation.strip().format(message.text))


bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

app.run(host=config.WEBHOOK_LISTEN,
        port=config.WEBHOOK_PORT,
        ssl_context=(config.WEBHOOK_SSL_CERT, config.WEBHOOK_SSL_PRIV),
        debug=config.DEBUG)
