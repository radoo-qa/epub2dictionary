import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
epub_file_path = 'book.epub'


def extract_contents_str(epub_file):
    #  book's table of contents to str
    book = epub.read_epub(epub_file_path)
    contents = []
    for item in book.get_items_of_type(ebooklib.ITEM_NAVIGATION):
        contents.append(item.get_content().decode('utf-8'))
    return '\n'.join(contents)


def extract_contents_url(contents_str):
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

def extract_chapters(contents_url):
    # iterate epub by chapter's url and save book to dict {chapter_name:chapter_content}
    book = epub.read_epub(epub_file_path)
    chapters = {}

    for chapter_name, chapter_url in contents_url.items():
        chapter = book.get_item_with_href(chapter_url)
        chapter_content = chapter.get_content().decode('utf-8')
        chapters[chapter_name] = chapter_content

    return chapters

def remove_markups(chapters):
    # remove xml markups from chapters
    blacklist = [line.strip() for line in open("blacklist.txt", 'r')]
    pretty_chapters = {}

    for chapter_name, chapter_content in chapters.items():
        cleaned_chapter = ''

        soup = BeautifulSoup(chapter_content, 'html.parser')
        text = soup.find_all(string=True)

        for t in text:
            if t.parent.name not in blacklist:
                cleaned_chapter += '{} '.format(t)

        pretty_chapters[chapter_name] = cleaned_chapter

    return pretty_chapters


contents_str = extract_contents_str(epub_file_path)
contents_url = extract_contents_url(contents_str)
chapters = extract_chapters(contents_url)
pretty_chapters = remove_markups(chapters)

