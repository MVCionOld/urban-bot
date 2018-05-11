import bs4
import requests

import logger


class UrbanDictionaryScrapper:
    """
    Scrapper for Urban Dictionary
    """

    HTML_CODE_TABLE = {
        "&apos;": "'",
        '&quot;': '"',
        '&amp;': '&',
        '&laquo;': '<<',
        '&raquo;': '>>',
        '&copy;': '(c)',
        '&reg;': '(r)'
    }

    def __init__(self):
        self.url = "http://www.urbandictionary.com/define.php?term=%s"

    def search(self, word):

        request = requests.get(self.url % word)

        if request.status_code != requests.codes.ok:
            logger.scrapper_logger.error('Wrong url or unknown word!')
            logger.scrapper_logger.error(request)
            return None

        parser = bs4.BeautifulSoup(request.content, 'html.parser')
        explanation = parser.find('div', {'class': 'meaning'}).get_text()
        explanation = self.filter(explanation)
        logger.scrapper_logger.info('%s:\n\t%s' % (word, explanation))
        return explanation

    def filter(self, explanation):
        for code, character in self.HTML_CODE_TABLE.items():
            explanation = explanation.replace(code, character)
        return explanation.strip()
