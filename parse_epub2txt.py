from typing import TextIO

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

epub_path = 'book.epub'


# Convert book.epub file to XML file and save as book.xml
def epub2xml(epub_path):
    xml_path: str = 'book.xml'
    with open(f'{xml_path}', 'wb') as xml_file:
        book = epub.read_epub(epub_path)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                xml_file.write(item.get_content())

# Parese book.xml to pretty txt format 
def parsexml(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    blacklist = [line.strip() for line in open("blacklist.txt", 'r')]
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

# Save txt to txt file
def xml2txt(xml_path):
    with open('book.txt', 'w') as file:
        xml_file = open(f'{xml_path}', "r", encoding="utf8")
        file.write(parsexml(xml_file))







