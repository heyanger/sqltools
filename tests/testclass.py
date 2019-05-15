import unittest
from collections import deque

from sqltools.utils import *

class SqltoolsTest(unittest.TestCase):
    def assertTreeEqual(self, left, right):
        self.assertIsNotNone(left)
        self.assertIsNotNone(right)

        self.assertEqual(left.type, right.type)
        self.assertEqual(left.value, right.value)
        self.assertDictEqual(left.attr, right.attr)
        self.assertEqual(len(left.children), len(right.children))
    
        for i in range(len(left.children)):
            self.assertTreeEqual(left.children[i], right.children[i])
    
    def print_tree(self, node, highlights=None):
        tree_print(node, highlights)

    