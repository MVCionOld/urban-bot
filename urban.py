import bs4
import requests

url_pattern = "http://www.urbandictionary.com/define.php?term=%s"


def search(word, debug=True):
    # get request of searching word
    r = requests.get(url_pattern % word)

    # action for invalid url or wrong word
    if r.status_code != requests.codes.ok:
        if debug:
            print('Wrong url or unknown word!\nError: [%s]\n' % r.status_code)
        return None

    parser = bs4.BeautifulSoup(r.content, 'html.parser')
    explanation = parser.find('div', {'class': 'meaning'}).get_text()

    return explanation


def fix(explanation):
    return explanation.strip().replace("&apos;", "'")


if __name__ == '__main__':
    while True:
        request = input()
        if request == 'exit':
            break
        else:
            print(search(request))
