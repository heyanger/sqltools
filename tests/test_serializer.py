from sqltools.sequence import *
from sqltools.tree import *
from sqltools.types import *
from tests.testclass import SqltoolsTest
from sqltools.serializer import *

class SerializeTest(SqltoolsTest):
    def test_serialize(self):
        left = TreeNode(State.SELECT)
        left.children.append(TreeNode(State.COL, value="salary"))
        left.children[0].children.append(TreeNode(State.AGG, value="max"))
        left.children.append(TreeNode(State.COL, value="department_name"))

        str = Serializer.serialize(left)
        print(str)

        self.assertEqual(str, "SELECT(COL[salary](AGG[max]),COL[department_name])")

    def test_deserialize(self):
        str = "SELECT(COL[salary](AGG[max]),COL[department_name])"

        left = TreeNode(State.SELECT)
        left.children.append(TreeNode(State.COL, value="salary"))
        left.children[0].children.append(TreeNode(State.AGG, value="max"))
        left.children.append(TreeNode(State.COL, value="department_name"))

        tree_print(left)
        tree_print(Serializer.deserialize(str))

        self.assertTreeEqual(Serializer.deserialize(str), left)

    def test_smart_split(self):
        str = "COL[salary](AGG[max]),COL[department_name],SELECT"
        strlist = ['COL[salary](AGG[max])', 'COL[department_name]', 'SELECT']

        print(Serializer.smart_split(str, ','))

        self.assertEqual(Serializer.smart_split(str, ','), strlist)