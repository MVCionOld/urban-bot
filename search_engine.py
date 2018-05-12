import json

import config
import db_manager
import scrappers
import translate


class SearchEngine:

    def __init__(self):
        self.translator = translate.Translate(config.YANDEX_TRANSLATE_API)
        self.scrapper = scrappers.UrbanDictionaryScrapper()
        with open('bot_commands.json') as bot_activity_file:
            self.bot_activity = json.loads(bot_activity_file.read())

    def search(self, text, lang="en"):

        if self.translator.detect(text) != "en":
            translated_text = self.translator.translate(text, lang="en")['text'][0]
        else:
            translated_text = text

        db_response = db_manager.get_description(translated_text)

        if db_response is None:
            if len(translated_text.split()) > 1:
                explanation = self.scrapper.search("+".join(translated_text.split()))
            else:
                explanation = self.scrapper.search(translated_text)
            explanation = "" if explanation is None else explanation
            db_manager.add_description(translated_text, explanation)
        else:
            explanation = db_response

        if not explanation:
            explanation = self.bot_activity["unknown"][lang]
        elif lang != "en":
            explanation = self.translator.translate(explanation, lang=lang)['text'][0]

        return explanation.strip().format(text)

    def get_top(self, limit, lang="en"):
        for position, explanation in db_manager.get_top(limit):
            yield "{0}.\n{1}".format(position, self.translator.translate(explanation, lang)['text'][0])
