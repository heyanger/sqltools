from sqltools.sequence import *
from sqltools.tree import *
from sqltools.types import *
from tests.testclass import SqltoolsTest

class SequenceTest(SqltoolsTest):
    def test_select1(self):
        left = TreeNode(State.SELECT)
        left.children.append(TreeNode(State.COL, value="salary"))
        left.children[0].children.append(TreeNode(State.AGG, value="max"))
        left.children.append(TreeNode(State.COL, value="department_name"))
        
        right = left.clone()

        seq = generate_sequence(left, right)

        self.assertListEqual(seq, ['copy'])

    def test_sql_sequence(self):
        sql1 = 'SELECT count(*) FROM Professionals'
        sql2 = "SELECT count(*) FROM Professionals WHERE city = 'West Heidi'"

        self.assertListEqual(generate_sequence_sql(sql1, sql2), ['copyandchange', 'copyandchange', 'copy', 'WHERE', 'COL[city]', 'OP[=]', 'TERMINAL[West Heidi]'])

    def test_apply1(self):
        sql1 = 'SELECT count(*) FROM Professionals'
        sql2 = "SELECT count(*) FROM Professionals WHERE city = 'West Heidi'"
        sequence = ['copyandchange', 'copyandchange', 'copy', 'WHERE', 'COL[city]', 'OP[=]', 'TERMINAL[West Heidi]']

        # self.assertEqual(apply_sequence(sql1, sequence), sql2)

    # def test_root2(self):
    #     node = TreeNode(State.ROOT)
    #     node.children.append(TreeNode(State.NONE))
    #     node.children[0].children.append(TreeNode(State.SELECT))
    #     node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
    #     node.children[0].children[0].children[0].children.append(TreeNode(State.AGG, value="max"))
    #     node.children[0].children[0].children.append(TreeNode(State.COL, value="department_name"))
    #     node.children[0].children.append(TreeNode(State.WHERE))
    #     node.children[0].children[1].children.append(TreeNode(State.COL, value="a"))
    #     node.children[0].children[1].children[0].children.append(TreeNode(State.OP, value="="))
    #     node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.TERMINAL, value="2"))

    #     sql = "SELECT max(salary), department_name FROM instructor WHERE a = 2"

    #     tn = TreeNode(State.ROOT)
    #     Parser.handle(tn, sql)

    #     self.assertTreeEqual(tn, node)

    # def test_root1(self):
    #     node = TreeNode(State.ROOT)
    #     node.children.append(TreeNode(State.NONE))
    #     node.children[0].children.append(TreeNode(State.SELECT))
    #     node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
    #     node.children[0].children[0].children[0].children.append(TreeNode(State.AGG, value="max"))
    #     node.children[0].children[0].children.append(TreeNode(State.COL, value="department_name"))

    #     sql = "SELECT max(salary), department_name FROM instructor"

    #     tn = TreeNode(State.ROOT)
    #     Parser.handle(tn, sql)

    #     self.assertTreeEqual(tn, node)

    # def test_root3(self):
    #     node = TreeNode(State.ROOT)
    #     node.children.append(TreeNode(State.NONE))
    #     node.children[0].children.append(TreeNode(State.SELECT))
    #     node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
    #     node.children[0].children[0].children[0].children.append(TreeNode(State.AGG, value="max"))
    #     node.children[0].children[0].children.append(TreeNode(State.COL, value="department_name"))
    #     node.children[0].children.append(TreeNode(State.GROUP))
    #     node.children[0].children[1].children.append(TreeNode(State.COL, value="department_name"))

    #     sql = "SELECT max(salary), department_name FROM instructor GROUP BY department_name"

    #     tn = TreeNode(State.ROOT)
    #     Parser.handle(tn, sql)

    #     self.assertTreeEqual(tn, node)

    # def test_group1(self):
    #     node = TreeNode(State.GROUP)
    #     node.children.append(TreeNode(State.COL, value="department_name"))

    #     sql = "GROUP BY department_name LIMIT 1"
    #     tn = TreeNode(State.GROUP)
    #     Parser.handle_group(tn, sql)
        
    #     self.assertTreeEqual(tn, node)

    # def test_group2(self):
    #     node = TreeNode(State.GROUP)
    #     node.children.append(TreeNode(State.COL, value="department_name"))
    #     node.children.append(TreeNode(State.HAVING))
    #     node.children[1].children.append(TreeNode(State.COL, value="salary"))
    #     node.children[1].children[0].children.append(TreeNode(State.AGG, value="avg"))
    #     node.children[1].children[0].children.append(TreeNode(State.OP, value=">"))
    #     node.children[1].children[0].children[1].children.append(TreeNode(State.TERMINAL, value="1"))

    #     sql = "GROUP BY department_name HAVING avg(salary) > 1"
    #     tn = TreeNode(State.GROUP)
    #     Parser.handle_group(tn, sql)
        
    #     self.assertTreeEqual(tn, node)

    # def test_group3(self):
    #     node = TreeNode(State.GROUP)
    #     node.children.append(TreeNode(State.COL, value="department_name"))
    #     node.children.append(TreeNode(State.HAVING))
    #     node.children[1].children.append(TreeNode(State.COL, value="salary"))
    #     node.children[1].children[0].children.append(TreeNode(State.AGG, value="avg"))
    #     node.children[1].children[0].children.append(TreeNode(State.OP, value=">"))

    #     newroot = TreeNode(State.ROOT)
    #     node.children[1].children[0].children[1].children.append(newroot)

    #     newroot.children.append(TreeNode(State.NONE))
    #     newroot.children[0].children.append(TreeNode(State.SELECT))
    #     newroot.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
    #     newroot.children[0].children[0].children[0].children.append(TreeNode(State.AGG, value="avg"))

    #     sql = "GROUP BY department_name HAVING avg(salary) > (SELECT avg(salary) FROM instructor)"
    #     tn = TreeNode(State.GROUP)
    #     Parser.handle_group(tn, sql)
        
    #     self.assertTreeEqual(tn, node)

    # def test_or(self):
    #     node = TreeNode(State.WHERE)
    #     node.children.append(TreeNode(State.LOGIC, value="or"))
    #     node.children[0].children.append(TreeNode(State.COL, value="city"))
    #     node.children[0].children[0].children.append(TreeNode(State.OP, value="="))
    #     node.children[0].children[0].children[0].children.append(TreeNode(State.TERMINAL, value="Aberdeen"))
    #     node.children[0].children.append(TreeNode(State.COL, value="city"))
    #     node.children[0].children[1].children.append(TreeNode(State.OP, value="="))
    #     node.children[0].children[1].children[0].children.append(TreeNode(State.TERMINAL, value="Abilene"))

    #     sql = 'WHERE city  =  "Aberdeen" OR city  =  "Abilene"'
    #     tn = TreeNode(State.WHERE)
    #     Parser.handle_where(tn, sql)

    #     self.assertTreeEqual(tn, node)

    # def test_union(self):
    #     node = TreeNode(State.ROOT)
    #     node.children.append(TreeNode(State.IUE, value="union"))
    #     node.children[0].children.append(TreeNode(State.ROOT))
    #     node.children[0].children[0].children.append(TreeNode(State.NONE))
    #     node.children[0].children[0].children[0].children.append(TreeNode(State.SELECT))
    #     node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.COL, value="SourceAirport"))
    #     node.children[0].children.append(TreeNode(State.ROOT))
    #     node.children[0].children[1].children.append(TreeNode(State.NONE))
    #     node.children[0].children[1].children[0].children.append(TreeNode(State.SELECT))
    #     node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.COL, value="DestAirport"))

    #     sql = "SELECT SourceAirport FROM Flights UNION SELECT DestAirport FROM Flights"

    #     tn = TreeNode(State.ROOT)
    #     Parser.handle(tn, sql)
        
    #     self.assertTreeEqual(tn, node)

    # def test_complex(self):
    #     root = TreeNode(State.ROOT)
    #     root.children.append(TreeNode(State.NONE))
    #     root.children[0].children.append(TreeNode(State.SELECT))
    #     root.children[0].children[0].children.append(TreeNode(State.COL, value="AirportName"))
    #     root.children[0].children.append(TreeNode(State.WHERE))
    #     root.children[0].children[1].children.append(TreeNode(State.COL, value="AirportCode"))
    #     root.children[0].children[1].children[0].children.append(TreeNode(State.OP, value="not in"))

    #     node = TreeNode(State.ROOT)
    #     node.children.append(TreeNode(State.IUE, value="union"))
    #     node.children[0].children.append(TreeNode(State.ROOT))
    #     node.children[0].children[0].children.append(TreeNode(State.NONE))
    #     node.children[0].children[0].children[0].children.append(TreeNode(State.SELECT))
    #     node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.COL, value="SourceAirport"))
    #     node.children[0].children.append(TreeNode(State.ROOT))
    #     node.children[0].children[1].children.append(TreeNode(State.NONE))
    #     node.children[0].children[1].children[0].children.append(TreeNode(State.SELECT))
    #     node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.COL, value="DestAirport"))

    #     root.children[0].children[1].children[0].children[0].children.append(node)

    #     sql = "SELECT AirportName FROM Airports WHERE AirportCode NOT IN (SELECT SourceAirport FROM Flights UNION SELECT DestAirport FROM Flights)"

    #     tn = TreeNode(State.ROOT)
    #     Parser.handle(tn, sql)
        
    #     self.assertTreeEqual(tn, root)
