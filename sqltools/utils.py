import re
import sqlparse

t = sqlparse.tokens.Token

def get_toks(tokens):
    return list(filter(lambda x:x.ttype != t.Text.Whitespace, tokens))

def find_token(tokens, typ=None, value=None):
    for i in range(len(tokens)):
        if (value is None or tokens[i].value.lower() == value.lower()) and (typ is None or type(tokens[i]) is typ):
            return i
    return -1

def inbetween_toks(tokens, left, left_value, right, right_value):
    l = 0
    r = len(tokens)

    for i in range(len(tokens)):
        if (left is None or type(tokens[i]) is left) and (left_value is None or tokens[i].value.lower() == left_value.lower()):
            l = i
            break

    for i in range(len(tokens)):
        if (right is None or type(tokens[i]) is right) and (right_value is None or tokens[i].value.lower() == right_value.lower()):
            r = i
            break

    return tokens[l+1: r]

def inbetween_toks_multi(tokens, left, left_value, rights):
    l = 0
    r = len(tokens)

    for i in range(len(tokens)):
        if (left is None or type(tokens[i]) is left) and (left_value is None or tokens[i].value.lower() == left_value.lower()):
            l = i
            break

    for right, right_value in rights:
        for i in range(len(tokens)-1, -1, -1):
            if i <= l:
                break


            if (right is None or type(tokens[i]) is right) and (right_value is None or tokens[i].value.lower() == right_value.lower()):
                r = min(r,i)
                break

    return tokens[l: r]
            

def smart_find(sentence, word):
    bracket_count = 0
    dq_count = 0
    sq_count = 0

    for i in range(len(sentence)-len(word)+1):
        if sentence[i] == '(':
            bracket_count += 1
        elif sentence[i] == ')':
            bracket_count -= 1

        if sentence[i] == '"':
            dq_count = 1 - dq_count

        if sentence[i] == '\'':
            sq_count = 1 - sq_count

        if bracket_count != 0 or sq_count != 0:
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
        v = smart_find(sentence.lower(), w.lower())

        if v >= 0:
            x = min(x, v)
            r = w

    return sentence[:x], sentence[x+len(r):], r

def in_between(sentence, left, right):
    l = smart_find(sentence.lower(), left.lower())
    r = smart_find(sentence.lower(), right.lower())

    return sentence[l+len(left):r]

def in_between_mult(sentence, left, words):
    l = smart_find(sentence.lower(), left.lower())
    r = len(sentence) + 1

    for w in words:
        v = smart_find(sentence.lower(), w.lower())

        if v >= 0:
            r = min(x, v)

    return sentence[l+len(left):r]

def split_multiple(new_sql, bools):
    return re.split('|'.join(b.lower() for b in bools), new_sql.lower())

def remove_front_parenthesis(sentence):
    l = sentence.find('(')
    r = sentence.rfind(')')

    if l == -1 or r == -1:
        return sentence

    return sentence[l+1:r]

def remove_front_sqbracket(sentence):
    l = sentence.find('[')
    r = sentence.rfind(']')

    if l == -1 or r == -1:
        return sentence

    return sentence[l+1:r]
