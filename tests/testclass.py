import unittest
from collections import deque

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
    
    def print_tree(self, node):
        q = deque([[node, 0]])
        cur_level = 0

        while q:
            node, level = q.pop()
            
            if level != cur_level:
                print()
                print('-----')
                cur_level = level
            
            if node.value:
                print(node.type.name+'['+node.value+']', end=',')
            else:
                print(node.type.name, end = ',')

            for c in node.children:
                q.appendleft([c, level + 1])


    