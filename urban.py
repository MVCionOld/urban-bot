#!/usr/bin/env python3.5


import bs4
import requests
import sys, os, glob
import re


def searchUrbanDictionary(word):
    
    """
    Function for search explanation of urban terms.
    Example:
        >>> exp = searchUrbanDictionary('asshole')
		>>> exp
		Your current boss.
    """

    url = "http://www.urbandictionary.com/define.php?term=%s"

    # get request of searching word 
    r = requests.get(url % word)
    
    # action for invalid url or wrong word
    if r.status_code != requests.codes.ok:
        print('Wrong url or unknown word!')
        print('Error: [%s]' % r.status_code)
        return None

    # get beautiful soup of request content
    bsObj = bs4.BeautifulSoup(r.content, 'html.parser')

    # get string explanation
    exp = bsObj.find('div', {'class' : 'meaning'}).get_text()

    return exp
	

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Attention: no words for search.')
        sys.exit(1)
    for word in sys.argv[1:]:
        print(('-'*10 + ' %s ' + '-'*10) % word)
        print(searchUrbanDictionary(word).strip(), end = '\n\n')
    sys.exit(0)
