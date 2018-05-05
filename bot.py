import sys
import json

import telebot

import config
import urban


def run_bot(debug=True):

    bot = telebot.TeleBot(
        config.URBAN_BOT_TOKEN if len(sys.argv) == 1 else sys.argv[-1]
    )

    urban_scrapper = urban.UrbanDictionaryScrapper()

    with open('botCommands.json') as bot_activity_file:
        bot_activity = json.loads(bot_activity_file.read())

    @bot.message_handler(commands=['start', 'help'])
    def handle_start_help(message):
        bot.send_message(message.chat.id, bot_activity['commands'][message.text])

    @bot.message_handler(content_types=['text'])
    def get_explanation(message):

        if len(message.text.split()) > 1:
            explanation = urban_scrapper.search("+".join(message.text.split()), debug=debug)
        else:
            explanation = urban_scrapper.search(message.text, debug=debug)

        if debug and explanation is not None:
            print("[{0}, {1}]:\n{2}\n".format(message.chat.id, message.text, explanation.strip()))

        if explanation is None:
            explanation = "There is no word's '{}' explanation on Urban Dictionary."

        bot.send_message(message.chat.id, explanation.strip().format(message.text))

    bot.polling(none_stop=True)


if __name__ == '__main__':
    run_bot()
