import pandas as pd
from table_of_contents import extract_contents_url
from settings import choose_chapter, set_previous_words, chapters_to_parse
from language_level import set_language_level
from parse_epub import extract_chapters, remove_markups
from clean_words import chapters2list, remove_common, remove_duplicates
from scraping import translate_words

contents_url = extract_contents_url()
chose_chapter = choose_chapter(contents_url)
words_already_occur = set_previous_words(chose_chapter, contents_url)

chapters_url = chapters_to_parse(chose_chapter, contents_url, words_already_occur)
language_level = set_language_level()

extracted_content_xml = extract_chapters(chapters_url)
parsed_content_str = remove_markups(extracted_content_xml)

content_words_list = chapters2list(parsed_content_str)
content_without_common = remove_common(content_words_list, language_level)
content_without_duplicated = remove_duplicates(content_without_common)

words_to_translate = {chose_chapter: content_without_duplicated[chose_chapter]}

FILE = r'_temporary.csv'
df = translate_words(words_to_translate)
df.to_csv(FILE)
