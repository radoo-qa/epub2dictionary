import re
import string
import pattern
from pattern.en import lexeme, lemma

re_word = re.compile(r'[\w]+')


def chapters2list(content):
    # Parse dict '{chapter_name}:{chapter_content_str} to {chapter_name}:{list_of_words}
    output = {}
    for chapter_name, chapter_content in content.items():
        cache_list = []
        for w in re_word.findall(chapter_content):
            if len(w) > 2:
                cache_list.append(w.casefold())
        output[chapter_name] = cache_list
    return output


def remove_common(content, common_words_dict):
    # Remove common words
    output = {}

    def is_common(word_to_check):
        # True if base form of word among common words
        lemma_word = lemma(word_to_check)
        if word_to_check in common_words_dict[word_to_check[0]] or lemma_word in common_words_dict[lemma_word[0]]:
            return True
        else:
            return False

    for chapter_name, chapter_words in content.items():
        cache_list = []
        for word in chapter_words:
            if (word[0] in string.ascii_lowercase) and not is_common(word):
                cache_list.append(word)
        output[chapter_name] = cache_list
    return output


def remove_duplicates(content):
    # Remove duplicate words:
    unique_list = []
    output = {}

    def unique_word(word2check):
        # Lexeme_words = list of all forms of a given word.
        lexeme_words = lexeme(word2check)
        for w in lexeme_words:
            if w in unique_list:
                return False
        return True

    for chapter_name, words in content.items():
        cache_list = []

        for word in words:
            if (word not in unique_list) and (unique_word(word)):
                cache_list.append(word)
                unique_list.append(word)

        output[chapter_name] = cache_list

    return output
