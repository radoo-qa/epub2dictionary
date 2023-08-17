from random import randint

import requests
from bs4 import BeautifulSoup
import webbrowser
import re
from lxml import etree
from pprint import pprint
import pandas as pd
from requests.exceptions import ConnectTimeout
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_soup(word):
    global response

    try:
        response = requests.get(f'https://dictionary.cambridge.org/dictionary/english-polish/{word}', headers=HEADERS,
                                timeout=3)
        if len(response.url) > 59:
            soup = BeautifulSoup(response.content, "lxml")
            for i in soup.find_all(class_=["pr entry-body__el", "pr entry-body"]):
                i.find(class_="pos dpos").string
            return soup
        return False

    except AttributeError:
        print(f'{word} - AttributeError!')
        return False


def scrap_word(chapter, word, soup):
    new_row = {'chapter': chapter, 'word': word}

    if soup.find_all(class_="pr entry-body__el"):
        entry_body = soup.find_all(class_="pr entry-body__el")
    else:
        entry_body = soup.find_all(class_="pr entry-body")

    for i in entry_body:
        if soup.find(class_="ipa dipa"):
            new_row['pronunciation'] = soup.find(class_="ipa dipa").text
        else:
            new_row['pronunciation'] = "NaN"

        for i in entry_body:
            part_of_speech = i.find(class_="pos dpos").string
            translated_words = [td.text.strip() for td in i.find_all(class_="trans dtrans dtrans-se", limit=2)]
            translated_words = sum([i.split(',  ') for i in translated_words], [])
            translated_words = set(translated_words)
            new_row[i.find(class_="pos dpos").string] = [i for i in translated_words]

    return pd.Series(new_row)


def translate_words(word_dict):
    df = pd.DataFrame(columns=['chapter',
                               'word',
                               'pronunciation',
                               'verb',
                               'noun',
                               'adjective'])

    for chapter, words in word_dict.items():
        print(f"{len(words)} to check")
        for word in words:
            soup = get_soup(word)
            if not soup:
                print(f"{word} not found")
                time.sleep(randint(1, 3))
                continue
            else:
                next_row = scrap_word(chapter, word, soup)
                df = pd.concat([df, next_row.to_frame().T], ignore_index=True)
                print(f"{word} added")
                time.sleep(randint(1, 3))
    return df
