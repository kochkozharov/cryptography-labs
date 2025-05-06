import random
import string
import urllib.request


CNT_RANDOM_TEXTS = 10
LEN_RANDOM_TEXT = 10 ** 6
URL1 = 'https://www.gutenberg.org/cache/epub/1497/pg1497.txt'
URL2 = 'https://www.gutenberg.org/cache/epub/2701/pg2701.txt'

def match_stat(text1, text2):
    cnt = 0
    for char1, char2 in zip(text1, text2):
        if char1 == char2:
            cnt += 1
    return cnt / min(len(text1), len(text2))


def gen_random_letters(n):
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))

def gen_random_words(n):
    url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'
    response = urllib.request.urlopen(url)
    words = response.read().decode()
    words = words.splitlines()
    text = ''
    while len(text) < n:
        text += ' ' + random.choice(words)
    rem = len(text) - n
    if rem != 0:
        text = text[:-rem]
    return text

def case1():
    print("Case #1: two meaningful texts in natural language.")
    response = urllib.request.urlopen(URL1)
    text1 = response.read().decode()
    print(f"Text 1 len: {len(text1)}")
    response = urllib.request.urlopen(URL2)
    text2 = response.read().decode()
    print(f"Text 2 len: {len(text2)}")
    min_len = min(len(text1), len(text2))
    text1 = text1[:min_len]
    text2 = text2[:min_len]
    print("Text length: {0}".format(min_len))
    print("Match: {0}".format(match_stat(text1, text2)))


def case2():
    print("Case #2: meaningful text and text from random letters.")
    response = urllib.request.urlopen(URL1)
    text1 = response.read().decode()
    s = 0
    for i in range(CNT_RANDOM_TEXTS):
        text2 = gen_random_letters(len(text1))
        s += match_stat(text1, text2)
    s /= CNT_RANDOM_TEXTS
    print("Text length: {0}".format(len(text1)))
    print("Match: {0}".format(s))


def case3():
    print("Case #3: meaningful text and text from random words.")
    response = urllib.request.urlopen(URL1)
    text1 = response.read().decode()
    s = 0
    for i in range(CNT_RANDOM_TEXTS):
        text2 = gen_random_words(len(text1))
        s += match_stat(text1, text2)
    s /= CNT_RANDOM_TEXTS
    print("Text length: {0}".format(len(text1)))
    print("Match: {0}".format(s))


def case4():
    print("Case #4: two texts from random letters.")
    s = 0
    for i in range(CNT_RANDOM_TEXTS):
        text1 = gen_random_letters(LEN_RANDOM_TEXT)
        text2 = gen_random_letters(LEN_RANDOM_TEXT)
        s += match_stat(text1, text2)
    s /= CNT_RANDOM_TEXTS
    print("Text length: {0}".format(LEN_RANDOM_TEXT))
    print("Match: {0}".format(s))


def case5():
    print("Case #5: two texts from random words.")
    s = 0
    for i in range(CNT_RANDOM_TEXTS):
        text1 = gen_random_words(LEN_RANDOM_TEXT)
        text2 = gen_random_words(LEN_RANDOM_TEXT)
        s += match_stat(text1, text2)
    s /= CNT_RANDOM_TEXTS
    print("Text length: {0}".format(LEN_RANDOM_TEXT))
    print("Match: {0}".format(s))

if __name__ == '__main__':
    case1()
    case2()
    case3()
    case4()
    case5()