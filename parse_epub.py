import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
epub_file_path = 'book.epub'


def extract_chapters(chapter_urls):
    # iterate epub by chapter's url and save book to dict {chapter_name:chapter_content_xml}
    book = epub.read_epub(epub_file_path)
    chapters_xml = {}

    for chapter_name, chapter_url in chapter_urls.items():
        chapter = book.get_item_with_href(chapter_url)
        chapter_content = chapter.get_content().decode('utf-8')
        chapters_xml[chapter_name] = chapter_content

    return chapters_xml


def remove_markups(chapters_xml):
    # remove xml markups from chapters
    blacklist = [line.strip() for line in open("blacklist.txt", 'r')]
    chapters = {}

    for chapter_name, chapter_content in chapters_xml.items():
        cleaned_chapter = ''

        soup = BeautifulSoup(chapter_content, 'html.parser')
        text = soup.find_all(string=True)

        for t in text:
            if t.parent.name not in blacklist:
                cleaned_chapter += '{} '.format(t)

        chapters[chapter_name] = cleaned_chapter

    return chapters
