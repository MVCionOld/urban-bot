import bs4
import requests

import logger

URL = "http://www.urbandictionary.com/define.php?term=%s"

HTML_CODE_TABLE = {
    "&apos;": "'",
    '&quot;': '"',
    '&amp;': '&',
    '&laquo;': '<<',
    '&raquo;': '>>',
    '&copy;': '(c)',
    '&reg;': '(r)'
}


class UrbanDictionaryScrapper:

    def __init__(self):
        pass

    def search(self, word):

        r = requests.get(URL % word)

        if r.status_code != requests.codes.ok:
            logger.scrapper_logger.error('Wrong url or unknown word!')
            logger.scrapper_logger.error(r)
            return None

        parser = bs4.BeautifulSoup(r.content, 'html.parser')
        explanation = parser.find('div', {'class': 'meaning'}).get_text()
        explanation = self.filter(explanation)
        logger.scrapper_logger.info('%s:\n\t%s' % (word, explanation))
        return explanation

    def filter(self, explanation):
        for code, character in HTML_CODE_TABLE.items():
            explanation = explanation.replace(code, character)
        return explanation.strip()
