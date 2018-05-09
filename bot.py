import json
import sys
import time

import flask
import telebot

import config
import logger
import urban

app = flask.Flask(__name__)

bot = telebot.TeleBot(
    config.URBAN_BOT_TOKEN if len(sys.argv) == 1 else sys.argv[-1],
    threaded=True
)

scrapper = urban.UrbanDictionaryScrapper()

with open('botCommands.json') as bot_activity_file:
    bot_activity = json.loads(bot_activity_file.read())


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
    bot.send_message(message.chat.id, bot_activity['commands'][message.text])


@bot.message_handler(commands=['statistics'])
def handle_start_help(message):
    logger.bot_logger.info("%s: %s" % (message.chat, message.text))
    bot.send_message(message.chat.id, bot_activity['commands'][message.text])


@bot.message_handler(commands=['lang'])
def handle_start_help(message):
    logger.bot_logger.info("%s: %s" % (message.chat, message.text))
    bot.send_message(message.chat.id, bot_activity['commands'][message.text])


@bot.message_handler(content_types=['text'])
def get_explanation(message):
    logger.bot_logger.info("%s: %s" % (message.chat, message.text))
    if len(message.text.split()) > 1:
        explanation = scrapper.search("+".join(message.text.split()))
    else:
        explanation = scrapper.search(message.text)

    explanation = "" if explanation is None else explanation

    logger.bot_logger.info('Send to %s: %s...'
                           % (message.chat.id, explanation[:min(20, len(explanation))]))

    if not explanation:
        explanation = "There is no explanation for '{}' in Urban Dictionary."

    bot.send_message(message.chat.id, explanation.strip().format(message.text))


bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

app.run(host=config.WEBHOOK_LISTEN,
        port=config.WEBHOOK_PORT,
        ssl_context=(config.WEBHOOK_SSL_CERT, config.WEBHOOK_SSL_PRIV),
        debug=config.DEBUG)
