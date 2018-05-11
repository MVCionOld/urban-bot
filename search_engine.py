import json

import config
import scrappers
import translate


class SearchEngine:

    def __init__(self):
        self.translator = translate.Translate(config.YANDEX_TRANSLATE_API)
        self.scrapper = scrappers.UrbanDictionaryScrapper()
        with open('botCommands.json') as bot_activity_file:
            self.bot_activity = json.loads(bot_activity_file.read())

    def get(self, text, lang="en"):
        if lang != "en":
            translated_text = self.translator.translate(text, lang="en")
        else:
            translated_text = text
        if len(translated_text.split()) > 1:
            explanation = self.scrapper.search("+".join(translated_text.split()))
        else:
            explanation = self.scrapper.search(translated_text)
        explanation = "" if explanation is None else explanation

        if not explanation:
            explanation = self.bot_activity["unknown"][lang]
        else:
            explanation = self.translator.translate(text, lang=lang)

        return explanation.strip().format(text)
