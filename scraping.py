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
    except ConnectTimeout:
        print('Request has timed out')

    if len(response.url) > 59:
        return BeautifulSoup(response.content, "lxml")
    return False


def scrap_word(chapter, word, soup):
    new_row = {'chapter': chapter, 'word': word}

    for i in soup.find_all(class_="pr entry-body__el"):
        new_row['pronunciation'] = soup.find(class_="ipa dipa").string

        part_of_speech = i.find(class_="pos dpos").string

        translated_words = []

        for td in i.find_all(class_="trans dtrans dtrans-se", limit=2):
            translated_words.append(td.text.strip())

            if len(translated_words) > 1:
                new_row[part_of_speech] = translated_words[0]
                new_row[f"{part_of_speech}2"] = translated_words[1]
            else:
                new_row[part_of_speech] = translated_words[0]

    return pd.Series(new_row)


def translate_words(word_dict):
    df = pd.DataFrame(columns=['chapter',
                               'word',
                               'pronunciation',
                               'verb',
                               'verb2',
                               'noun',
                               'noun2',
                               'adjective',
                               'adjective2'])

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
