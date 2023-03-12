import string
import re

words_path = 'C:\Python\harry\common_1000.txt'
book_path = 'C:\Python\harry\chapters\harry_chapter1.txt'

def difficulty(words_path):
    with open(f'{words_path}', 'r') as file:
        common_dics = {i: [] for i in list(string.ascii_lowercase)}
        for word in file:
            word = word.lower().split(',')
        for m in range(len(word)):
            common_dics[word[m][0]].append(word[m])
    return common_dics

re_word = re.compile(r'[\w-]+')

def cleanbook(book_path):
    output = ''
    output2 = ''
    with open(book_path, 'r') as file:
        for line in file.readlines():
            for word in re_word.findall(line):
                output += '{} '.format(word.casefold())
    for x in ''.strip(output):
        print(x)

cleanbook(book_path)