import string


def set_language_level():
    words_known = input("How many common words should dictionary skip? Input a number. Choice:\n"
                        "1000 - e.g.: baby, face, eye, worry, notice, order, need, quiet, each\n"
                        "1500 - consider, prove, speech, require, create, describe, occur, purpose, allow, figure\n"
                        "2500 - belong, replace, favor, obvious, amuse, surround, insist, stick, interrupt, impress\n"
                        "3500 - contribution, headquarters, retirement, precisely, prayer, justice, barrel\n")

    if int(words_known) in [1000, 1500, 2500, 3500]:
        with open(f'common_{words_known}.txt', 'r') as file:
            common_words = {i: [] for i in list(string.ascii_lowercase)}
            for words in file:
                words = words.lower().split(',')
            for word in words:
                common_words[word[0]].append(word)
        return common_words
    else:
        raise ValueError('Number is not on the list: 1000, 1500, 2500, 3500')
