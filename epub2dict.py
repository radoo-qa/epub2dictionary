# Step 1. Take epub file and parse to txt

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


epub_file_path = 'book.epub'

def parse_epub2str(epub_file):
    book = epub.read_epub(epub_file)
    text_content = []

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content = item.get_content()
        text_content.append(content.decode('utf-8'))

    parsed_text = '\n'.join(text_content)

    return parsed_text

def clean_str(book):
    output = ''
    soup = BeautifulSoup(book, 'html.parser')
    text = soup.find_all(string=True)
    blacklist = [line.strip() for line in open("blacklist.txt", 'r')]
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def book2dict(book, chapter_identifier='Chapter'):
    current_idx: int = 0
    chapters_idx: list[int] = []
    chapters_dict: dict[int, str] = {}

    content = book

    count_chapters = content.count(chapter_identifier)

    for i in range(count_chapters):
        current_idx = content.find('Chapter', current_idx+1)
        chapters_idx.append(current_idx)

    for idx in range(len(chapters_idx)):
        if idx != len(chapters_idx) - 1:
            chapters_dict[idx+1] = content[chapters_idx[idx]:chapters_idx[idx+1]]
        else:
            chapters_dict[idx+1] = content[chapters_idx[idx]:]

    return chapters_dict


# task: get contents of a book, and then parse into a txt file by linking to chapters

book = epub.read_epub(epub_file_path)
output = []
for item in book.get_items_of_type(ebooklib.ITEM_NAVIGATION):
    output.append(item.get_content().decode('utf-8'))

parsed_text = '\n'.join(output)




"""
def extract_navpoints(xml_string):
    ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
    root = ET.fromstring(xml_string)

    navpoints = root.findall('.//ncx:navPoint', ns)
    contents = {}

    for navpoint in navpoints:
        text = navpoint.find('ncx:navLabel/ncx:text', ns).text
        content = navpoint.find('ncx:content', ns).attrib['src']
        contents[text] = content

    return contents

"""


root = ET.fromstring(parsed_text)

for point in root.findall('navMap'):
    print(point.text)