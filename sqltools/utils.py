import re

def split_string(sentence, word):
    x = sentence.lower().find(word)

    return sentence[:x], sentence[x+len(word):]

def split_string_seq(sentence, words):
    x = len(sentence) + 1
    r = ""

    for w in words:
        v = sentence.lower().find(w) 

        if v >= 0:
            x = min(x, v)
            r = w

    return sentence[:x], sentence[x+len(r):], r

def in_between(sentence, left, right):
    l = sentence.lower().find(left.lower())
    r = sentence.lower().find(right.lower())

    return sentence[l+len(left):r]

def split_multiple(new_sql, bools):
    return re.split('|'.join(b.lower() for b in bools), new_sql.lower())

def remove_front_parenthesis(sentence):
    l = sentence.find('(')
    r = sentence.rfind(')')

    return sentence[l+1:r]