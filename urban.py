import bs4
import requests

url = "http://www.urbandictionary.com/define.php?term=%s"


def search(word):
    # get request of searching word
    r = requests.get(url % word)

    # action for invalid url or wrong word
    if r.status_code != requests.codes.ok:
        print('Wrong url or unknown word!')
        print('Error: [%s]' % r.status_code)
        return None

    # get beautiful soup of request content
    bs_obj = bs4.BeautifulSoup(r.content, 'html.parser')

    # get string explanation
    exp = bs_obj.find('div', {'class': 'meaning'}).get_text()

    return exp


if __name__ == '__main__':
    while True:
        pass
