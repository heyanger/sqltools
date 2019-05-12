from sqltools.parser import *
from tests.testclass import SqltoolsTest

class TotreeTest(SqltoolsTest):
    def test_parser(self):
        self.assertEqual(Parser.get_state('col'), State.COL)
        self.assertEqual(Parser.get_state('2'), State.TERMINAL)
        self.assertEqual(Parser.get_state('( SELECT * FROM )'), State.ROOT)
        self.assertEqual(Parser.get_state('"test"'), State.TERMINAL)

    def test_handle_pair1(self):
        node = TreeNode(State.ROOT)
        left = TreeNode(State.COL)
        left.attr['value'] = 'a'
        right = TreeNode(State.OP)
        right.attr['value'] = '='
        child = TreeNode(State.TERMINAL)
        child.attr['value'] = '2'

        node.children.append(left)
        node.children.append(right)
        right.children.append(child)

        tn = TreeNode(State.ROOT)
        Parser.handle_pair(tn, 'a = 2')
        
        self.assertTreeEqual(tn, node)

    def test_handle_pair2(self):
        node = TreeNode(State.ROOT)
        left = TreeNode(State.COL)
        left.attr['value'] = 'a'
        left_child = TreeNode(State.AGG)
        left_child.attr['value'] = 'min'

        right = TreeNode(State.OP)
        right.attr['value'] = '='
        child = TreeNode(State.TERMINAL)
        child.attr['value'] = '2'

        node.children.append(left)
        node.children.append(right)
        left.children.append(left_child)
        right.children.append(child)

        tn = TreeNode(State.ROOT)
        Parser.handle_pair(tn, 'min(a) = 2')
        
        self.assertTreeEqual(tn, node)

    def test_select1(self):
        node = TreeNode(State.SELECT)
        left = TreeNode(State.COL)
        left.attr['value'] = 'salary'
        left_child = TreeNode(State.AGG)
        left_child.attr['value'] = 'max'
        right = TreeNode(State.COL)
        right.attr['value'] = 'department_name'

        left.children.append(left_child)
        node.children.append(left)
        node.children.append(right)

        sql = "SELECT max(salary), department_name FROM instructor"

        tn = TreeNode(State.SELECT)
        Parser.handle_select(tn, sql)

        self.assertTreeEqual(tn, node)

    def test_root2(self):
        root = TreeNode(State.ROOT)

        node = TreeNode(State.SELECT)
        left = TreeNode(State.COL)
        left.attr['value'] = 'salary'
        left_child = TreeNode(State.AGG)
        left_child.attr['value'] = 'max'
        right = TreeNode(State.COL)
        right.attr['value'] = 'department_name'

        node2 = TreeNode(State.WHERE)
        left2 = TreeNode(State.COL)
        left2.attr['value'] = 'a'
        right2 = TreeNode(State.OP)
        right2.attr['value'] = '='
        right_child2 = TreeNode(State.TERMINAL)
        right_child2.attr['value'] = '2'
        right2.children.append(right_child2)
        node2.children.append(left2)
        node2.children.append(right2)

        left.children.append(left_child)
        node.children.append(left)
        node.children.append(right)

        root.children.append(node)
        root.children.append(node2)

        sql = "SELECT max(salary), department_name FROM instructor WHERE a = 2"

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, sql)

        self.assertTreeEqual(tn, root)

    def test_root1(self):
        root = TreeNode(State.ROOT)
        node = TreeNode(State.SELECT)
        left = TreeNode(State.COL)
        left.attr['value'] = 'salary'
        left_child = TreeNode(State.AGG)
        left_child.attr['value'] = 'max'
        right = TreeNode(State.COL)
        right.attr['value'] = 'department_name'

        left.children.append(left_child)
        node.children.append(left)
        node.children.append(right)
        root.children.append(node)

        sql = "SELECT max(salary), department_name FROM instructor"

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, sql)

        self.assertTreeEqual(tn, root)

    def test_root3(self):
        root = TreeNode(State.ROOT)
        node = TreeNode(State.SELECT)
        left = TreeNode(State.COL)
        left.attr['value'] = 'salary'
        left_child = TreeNode(State.AGG)
        left_child.attr['value'] = 'max'
        right = TreeNode(State.COL)
        right.attr['value'] = 'department_name'

        node2 = TreeNode(State.GROUP)
        child2 = TreeNode(State.COL)
        child2.attr['value'] = 'department_name'
        node2.children.append(child2)

        left.children.append(left_child)
        node.children.append(left)
        node.children.append(right)
        root.children.append(node)
        root.children.append(node2)

        sql = "SELECT max(salary), department_name FROM instructor GROUP BY department_name"

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, sql)

        self.assertTreeEqual(tn, root)

    def test_group1(self):
        root = TreeNode(State.GROUP)
        n1 = TreeNode(State.COL)
        n1.attr['value'] = 'department_name'
        root.children.append(n1)

        sql = "GROUP BY department_name LIMIT 1"
        tn = TreeNode(State.GROUP)
        Parser.handle_group(tn, sql)
        
        self.assertTreeEqual(tn, root)

    def test_group2(self):
        root = TreeNode(State.GROUP)
        n1 = TreeNode(State.COL)
        n1.attr['value'] = 'department_name'
        
        n2 = TreeNode(State.HAVING)
        cn2 = TreeNode(State.COL)
        cn2.attr['value'] = 'salary'
        ccn2 = TreeNode(State.AGG)
        ccn2.attr['value'] = 'avg'
        cn3 = TreeNode(State.OP)
        cn3.attr['value'] = '>'
        ccn3 = TreeNode(State.TERMINAL)
        ccn3.attr['value'] = '1'

        root.children.append(n1)
        root.children.append(n2)
        n2.children.append(cn2)
        n2.children.append(cn3)
        cn2.children.append(ccn2)
        cn3.children.append(ccn3)

        sql = "GROUP BY department_name HAVING avg(salary) > 1"
        tn = TreeNode(State.GROUP)
        Parser.handle_group(tn, sql)
        
        self.assertTreeEqual(tn, root)

    def test_group3(self):
        root = TreeNode(State.GROUP)
        n1 = TreeNode(State.COL)
        n1.attr['value'] = 'department_name'
        
        n2 = TreeNode(State.HAVING)
        cn2 = TreeNode(State.COL)
        cn2.attr['value'] = 'salary'
        ccn2 = TreeNode(State.AGG)
        ccn2.attr['value'] = 'avg'
        cn3 = TreeNode(State.OP)
        cn3.attr['value'] = '>'
        
        nroot = TreeNode(State.ROOT)
        nselect = TreeNode(State.SELECT)
        nsalary = TreeNode(State.COL)
        nsalary.attr['value'] = 'salary'
        navg = TreeNode(State.AGG)
        navg.attr['value'] = 'avg'

        root.children.append(n1)
        root.children.append(n2)
        n2.children.append(cn2)
        n2.children.append(cn3)
        cn2.children.append(ccn2)
        cn3.children.append(nroot)

        nroot.children.append(nselect)
        nselect.children.append(nsalary)
        nsalary.children.append(navg)

        sql = "GROUP BY department_name HAVING avg(salary) > (SELECT avg(salary) FROM instructor)"
        tn = TreeNode(State.GROUP)
        Parser.handle_group(tn, sql)
        
        self.assertTreeEqual(tn, root)

