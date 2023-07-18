import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
epub_file_path = 'book.epub'


def extract_contents_str(epub_file_path):
    #  extract book's table of contents to str
    book = epub.read_epub(epub_file_path)
    contents = []
    for item in book.get_items_of_type(ebooklib.ITEM_NAVIGATION):
        contents.append(item.get_content().decode('utf-8'))
    return '\n'.join(contents)


def extract_contents_url():
    contents_str = extract_contents_str(epub_file_path)
    # book's table of contents to dict {chapter_name:chapter_url}
    ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
    root = ET.fromstring(contents_str)

    navpoints = root.findall('.//ncx:navPoint', ns)
    contents = {}

    for navpoint in navpoints:
        text = navpoint.find('ncx:navLabel/ncx:text', ns).text
        content = navpoint.find('ncx:content', ns).attrib['src']
        contents[text] = content

    return contents