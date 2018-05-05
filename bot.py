import sys
import json
import config
import telebot
from urban import search


def start():
    debug = True
    bot = telebot.TeleBot(
        config.URBAN_BOT_TOKEN if len(sys.argv) == 1 else sys.argv[-1]
    )
    with open('botData.json') as bot_data:
        bot_data = json.loads(bot_data.read())

    @bot.message_handler(commands=['start', 'help'])
    def handle_start_help(message):
        bot.send_message(message.chat.id, bot_data['commands'][message.text])

    @bot.message_handler(content_types=['text'])
    def get_explanation(message):
        if len(message.text.split()) > 1:
            explanation = search("+".join(message.text.split()))
        else:
            explanation = search(message.text)
        if debug:
            print("[{0}, {1}]:\n{2}\n".format(message.chat.id, message.text, explanation.strip()))
        if explanation is None:
            explanation = "There is no word's '{}' explanation on Urban Dictionary."
        bot.send_message(message.chat.id, explanation.strip().format(message.text))

    bot.polling(none_stop=True)


if __name__ == '__main__':
    start()
