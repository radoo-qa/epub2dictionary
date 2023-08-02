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
        translated_words = []
        if soup.find(class_="ipa dipa"):
            new_row['pronunciation'] = soup.find(class_="ipa dipa").text
        else:
            new_row['pronunciation'] = "NULL"

        part_of_speech = i.find(class_="pos dpos").string

        if i.find_all(class_="sense-block pr dsense", limit=2):
            for td in i.find_all(class_="sense-block pr dsense", limit=2):
                translated_words.append(td.find(class_="trans dtrans dtrans-se").text.strip())

                if len(translated_words) > 1:
                    new_row[part_of_speech] = translated_words[0]
                    new_row[f"{part_of_speech}2"] = translated_words[1]
                else:
                    new_row[part_of_speech] = translated_words[0]
        else:
            new_row[soup.find(class_="pos dpos").string] = soup.find(class_="trans dtrans dtrans-se").text.strip()

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
