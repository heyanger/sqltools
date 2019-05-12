import unittest
from sqltools.parser import *

class TotreeTest(unittest.TestCase):
    def test_parser(self):
        self.assertEqual(Parser.get_state('col'), State.COL)
        self.assertEqual(Parser.get_state('2'), State.TERMINAL)
        self.assertEqual(Parser.get_state('( SELECT * FROM )'), State.ROOT)
        self.assertEqual(Parser.get_state('"test"'), State.TERMINAL)

    def test_handle_pair(self):
        tn = Parser.handle_pair(TreeNode(State.ROOT), 'a = 2')