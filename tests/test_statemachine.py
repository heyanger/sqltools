# from sqltools.parser import *
# from sqltools.utils import *
# from tests.testclass import SqltoolsTest
#
# import sqlparse
#
# class ParserTest(SqltoolsTest):
#     def test_state_1(self):
#         sql = "WHERE city  =  'West Heidi'"
#         token = sqlparse.parse(sql)[0]
#         tn = TreeNode(State.NONE)
#         Parser.handle(tn, token)
#
#         self.print_tree(tn)
#
#     def test_state_2(self):
#         sql = "not in (SELECT dog_id FROM treatments)"
#         token = sqlparse.parse(sql)[0]
#         tn = TreeNode(State.COL)
#         Parser.handle(tn, token)
#
#         self.print_tree(tn)
#
#         self.assertEqual(True, False)