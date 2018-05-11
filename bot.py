import json
import time

import flask
import telebot

import config
import db_manager
import logger
import search_engine

engine = search_engine.SearchEngine()

bot = telebot.TeleBot(config.URBAN_BOT_TOKEN, threaded=True)

with open('bot_commands.json') as bot_activity_file:
    bot_activity = json.loads(bot_activity_file.read())

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route(config.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        logger.server_logger.info(json_string)
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        logger.server_logger.error(flask.request.headers.values())
        flask.abort(403)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    logger.bot_logger.info("%s: %s" % (message.chat, message.text))
    bot.send_message(message.chat.id,
                     bot_activity['commands'][db_manager.get_lang(message.chat.id)][message.text])


@bot.message_handler(commands=['statistics'])
def handle_statistics(message):
    logger.bot_logger.info("%s: %s" % (message.chat, message.text))
    bot.send_message(message.chat.id,
                     bot_activity['commands'][db_manager.get_lang(message.chat.id)][message.text])


@bot.message_handler(commands=['lang'])
def handle_lang(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="English", callback_data='en'))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Русский", callback_data='ru'))
    logger.bot_logger.info("%s: %s" % (message.chat, message.text))
    bot.send_message(message.chat.id,
                     bot_activity['commands'][db_manager.get_lang(message.chat.id)][message.text],
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    db_manager.set_lang(call.message.chat.id, call.data)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=bot_activity["commands"][call.data]["lang_callback"])


@bot.message_handler(content_types=['text'])
def get_explanation(message):
    logger.bot_logger.info("%s: %s" % (message.chat, message.text))
    explanation = engine.search(message.text, lang=db_manager.get_lang(message.chat.id))
    logger.bot_logger.info('Send to %s: %s...'
                           % (message.chat.id, explanation[:min(140, len(explanation))]))
    bot.send_message(message.chat.id, explanation)
    print(message.chat.id, explanation)


bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

app.run(host=config.WEBHOOK_LISTEN,
        port=config.WEBHOOK_PORT,
        ssl_context=(config.WEBHOOK_SSL_CERT, config.WEBHOOK_SSL_PRIV),
        debug=config.DEBUG)
