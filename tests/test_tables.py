from sqltools.parser import *
from tests.testclass import SqltoolsTest

import sqlparse

class TableTest(SqltoolsTest):
    def test_basic_1(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))        
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="instructor"))        
        node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))        

        sql = "SELECT salary FROM instructor"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)