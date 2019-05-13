from sqltools.parser import *
from tests.testclass import SqltoolsTest

class TreeTest(SqltoolsTest):
    def test_clone(self):
        root = TreeNode(State.ROOT)
        root.children.append(TreeNode(State.NONE))
        root.children[0].children.append(TreeNode(State.SELECT))
        root.children[0].children[0].children.append(TreeNode(State.COL, value="AirportName"))
        root.children[0].children.append(TreeNode(State.WHERE))
        root.children[0].children[1].children.append(TreeNode(State.COL, value="AirportCode"))
        root.children[0].children[1].children[0].children.append(TreeNode(State.OP, value="not in"))

        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.IUE, value="union"))
        node.children[0].children.append(TreeNode(State.ROOT))
        node.children[0].children[0].children.append(TreeNode(State.NONE))
        node.children[0].children[0].children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.COL, value="SourceAirport"))
        node.children[0].children.append(TreeNode(State.ROOT))
        node.children[0].children[1].children.append(TreeNode(State.NONE))
        node.children[0].children[1].children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.COL, value="DestAirport"))

        root.children[0].children[1].children[0].children[0].children.append(node)

        new_root = root.clone()
       
        self.assertTreeEqual(root, new_root)
