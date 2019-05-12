import unittest
from sqltools.utils import *

class TotreeTest(unittest.TestCase):
    def test_splitstring(self):
        left, right = split_string('(SELECT * FROM table1) INTERSECT (SELECT * FROM table2)', 'intersect')
        self.assertEqual(left, '(SELECT * FROM table1) ')
        self.assertEqual(right, ' (SELECT * FROM table2)')

    def test_splitstringseq(self):
        words = [
            'SELECT * FROM table1 JOIN lorem ipsum', 
            'SELECT * FROM table1 WHERE lorem ipsum',
            'SELECT * FROM table1 GROUP BY lorem ipsum',
            'SELECT * FROM table1 ORDER BY lorem ipsum',
            'SELECT * FROM table1 HAVING lorem ipsum',
            'SELECT * FROM table1 lorem ipsum',
        ]
        KEYWORD = ["select", " join ", " where ", " group by ", " order by ", " having "]

        for w in words[:-1]:
            res, _, _ = split_string_seq(w, KEYWORD[1:])
            self.assertEqual(res, 'SELECT * FROM table1')
        
        res, _, _ = split_string_seq(words[-1], KEYWORD[1:])
        self.assertEqual(res, 'SELECT * FROM table1 lorem ipsum')

    def test_splitstringseq_op(self):
        words = [
            'abc = def'
        ]
        OPS = [' = ', ' < ', ' > ', ' >= ', ' <= ', ' != ', ' LIKE ', ' NOT IN ', ' BETWEEN ']

        for w in words:
            l, r, m = split_string_seq(w, OPS)
            self.assertEqual(l, 'abc')
            self.assertEqual(r, 'def')
            self.assertEqual(m, ' = ')

    def test_inbetween(self):
        word = 'SELECT * FROM table1 JOIN lorem ipsum'
        
        self.assertEqual(in_between(word, 'SELECT', 'FROM'), ' * ')

    def test_split_multiple(self):
        word = 'lorem AND ipsum OR dolor AND sid'

        self.assertEqual(split_multiple(word, [' and ', ' or ']), ['lorem', 'ipsum', 'dolor', 'sid'])

    def test_remove_front_parenthesis(self):
        self.assertEqual(remove_front_parenthesis('(SELECT * FROM table1 JOIN lorem ipsum)'), 'SELECT * FROM table1 JOIN lorem ipsum')
        self.assertEqual(remove_front_parenthesis('min(avg)'),'avg')
        self.assertEqual(remove_front_parenthesis('avg'),'avg')

    def test_smart_find(self):
        self.assertEqual(smart_find('abc', 'a'),0)
        self.assertEqual(smart_find('abc', 'bc'),1)
        self.assertEqual(smart_find('abc', 'c'),2)
        self.assertEqual(smart_find('abc', 'd'),-1)
        self.assertEqual(smart_find('o a (select)', 'select'),-1)
        self.assertEqual(smart_find('o a (select)select', 'select'),12)
