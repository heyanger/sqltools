import re

def smart_find(sentence, word):
    count = 0
    for i in range(len(sentence)-len(word)+1):
        if sentence[i] == '(':
            count += 1
        elif sentence[i] == ')':
            count -= 1

        if count != 0:
            continue

        if sentence[i:i+len(word)] == word:
            return i

    return -1

def split_string(sentence, word):
    x = smart_find(sentence.lower(), word)

    return sentence[:x], sentence[x+len(word):]

def split_string_seq(sentence, words):
    x = len(sentence) + 1
    r = ""

    for w in words:
        v = smart_find(sentence.lower(), w)

        if v >= 0:
            x = min(x, v)
            r = w

    return sentence[:x], sentence[x+len(r):], r

def in_between(sentence, left, right):
    l = smart_find(sentence.lower(), left.lower())
    r = smart_find(sentence.lower(), right.lower())

    return sentence[l+len(left):r]

def split_multiple(new_sql, bools):
    return re.split('|'.join(b.lower() for b in bools), new_sql.lower())

def remove_front_parenthesis(sentence):
    l = sentence.find('(')
    r = sentence.rfind(')')

    if l == -1 or r == -1:
        return sentence

    return sentence[l+1:r]