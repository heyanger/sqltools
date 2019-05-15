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

        self.assertListEqual(generate_sequence_sql(sql1, sql2), ['copyandchange', 'copyandchange[WHERE,COL[city],OP[=],TERMINAL[\'West Heidi\']]', 'copy'])

    def test_apply_sequence_sql1(self):
        sql1 = 'SELECT count(*) FROM Professionals'
        sql2 = "SELECT count(*) FROM professionals WHERE city = 'West Heidi'"

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql2(self):
        sql1 = "SELECT * FROM AIRLINES WHERE Airline = \"JetBlue Airways\""
        sql2 = "SELECT country FROM airlines WHERE airline = \"JetBlue Airways\""

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql3(self):
        sql1 = "SELECT Country FROM AIRLINES WHERE Airline  =  \"JetBlue Airways\""
        sql2 = "SELECT * FROM airlines WHERE airline = \"JetBlue Airways\""

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    # def test_apply_sequence_sql4(self):
    #     sql1 = "SELECT * FROM Owners"
    #     sql2 = "SELECT count(*) FROM Owners WHERE state = 'Arizona'"

    #     self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)
