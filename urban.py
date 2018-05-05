import bs4
import requests

import config

url_pattern = "http://www.urbandictionary.com/define.php?term=%s"


class UrbanDictionaryScrapper:

    def __init__(self):
        pass

    def search(self, word, debug=config.DEBUG):

        r = requests.get(url_pattern % word)

        if r.status_code != requests.codes.ok:
            if debug:
                print('Wrong url or unknown word!\nError: [%s]\n' % r.status_code)
            return None

        parser = bs4.BeautifulSoup(r.content, 'html.parser')
        explanation = parser.find('div', {'class': 'meaning'}).get_text()

        return self.fix(explanation)

    def fix(self, explanation):
        return explanation.strip().replace("&apos;", "'").replace('&quot;', '"')
