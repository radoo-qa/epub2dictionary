import re
import string
from dev_book2dict import book2dict
import pattern
from pattern.en import lexeme, lemma


re_word = re.compile(r'[\w]+')
book_path = 'C:/Python/harry/book.txt'
common_words_path = 'C:/Python/harry/common_1000.txt'

def chapter2list(book_path):
    # Save book to dict num_chapter:str
    book_dict = book2dict(book_path)

    # Convert num_chapter:str to num_chapter:list
    new_dict = {}
    for key, chapter in book_dict.items():
        cache_list = []
        for word in re_word.findall(chapter):
            if len(word) > 2:
                cache_list.append(word.casefold())
        new_dict[key] = cache_list
    return new_dict

# Save common words txt file to dict alph_letter:list
def common_words2dict(words_path):
    with open(f'{words_path}', 'r') as file:
        common_dict = {i: [] for i in list(string.ascii_lowercase)}
        for word in file:
            word = word.lower().split(',')
        for m in range(len(word)):
            common_dict[word[m][0]].append(word[m])
    return common_dict

# Remove common english words from book
def remove_common():
    common_words_dict = common_words2dict(common_words_path)
    book_dict = chapter2list(book_path)
    new_dict = {}

    def word_among_common(word, common_words_dict):
        lemma_word = lemma(word)
        if lemma_word in common_words_dict[word[0]]:
            return True
        else:
            return False

    for chapter, words in book_dict.items():
        cache_list = []
        for word in words:
            if (word[0] in string.ascii_lowercase) and not word_among_common(word, common_words_dict):
                cache_list.append(word)
        new_dict[chapter] = cache_list
    return new_dict

# Remove duplicate word:
def only_unique():
    book = remove_common()
    unique = []
    new_dict = {}

    def unique_word(word2check, unique_words):
        lexeme_words = lexeme(word2check)
        for n in lexeme_words:
            if n in unique_words:
                return False
        return True

    for chapter, words in book.items():
        cache_list = []

        for word in words:
            if (word not in unique) and (unique_word(word, unique)):
                cache_list.append(word)
                unique.append(word)

        new_dict[chapter] = cache_list
    return new_dict



with open('only_unique_words5.txt', 'w') as file:
    save_file = []
    book2 = only_unique()
    for values in book2.values():
        for value in values:
            save_file.append(value)
    for i in save_file:
        file.write(i+'\n')

"""
# def only_unique_words() -
unique = [xxxxxxx]
word = 'misses'

1. 
if word[:-2] (miss) in unique?
> TRUE > ignore
> FALSE > continue

2. 
if word[:-2] (miss) in book?
-> TRUE > ignore
-> FALSE > add word (misses) to unique


def only_unique_words():
    book = remove_duplicates()
    unique = []
    new_dict = {}
    for key, chapter in book.items():
        cache_list = []
        for word in chapter:
            if word[:-2] not in unique:
                if word[:-2] not in book.values():
                 unique.append(word)
        new_dict[key] = cache_list
    return new_dict


with open('only_unique_words.txt', 'w') as file2:
    save_file2 = []
    book2 = only_unique_words()
    for values in book2.values():
        for value in values:
            save_file2.append(value)
    for i in save_file2:
        file2.write(i+'\n')


with open('remove_duplicates.txt', 'w') as file:
    save_file = []
    book = remove_duplicates()
    for values in book.values():
        for value in values:
            save_file.append(value)
    for i in save_file:
        file.write(i+'\n')


"""


