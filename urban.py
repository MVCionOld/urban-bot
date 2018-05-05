import bs4
import requests

import config

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

    def search(self, word, debug=config.DEBUG):

        r = requests.get(URL % word)

        if r.status_code != requests.codes.ok:
            if debug:
                print('Wrong url or unknown word!\nError: [%s]\n' % r.status_code)
            return None

        parser = bs4.BeautifulSoup(r.content, 'html.parser')
        explanation = parser.find('div', {'class': 'meaning'}).get_text()

        return self.filter(explanation)

    def filter(self, explanation):
        for k, v in HTML_CODE_TABLE:
            explanation = explanation.replace(k, v)
        return explanation
