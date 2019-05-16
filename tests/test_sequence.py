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

        self.assertListEqual(generate_sequence_sql(sql1, sql2), ['copyandchange', 'copyandchange[WHERE(COL[city](OP[=](TERMINAL[\'West Heidi\'])))]', 'copy'])

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

    def test_apply_sequence_sql4(self):
        sql1 = "SELECT * FROM Owners"
        sql2 = "SELECT count(*) FROM owners WHERE state = 'Arizona'"

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    # def test_apply_sequence_sql5(self):
    #     sql1 = "select count(*) from dogs where dog_id in ( select dog_id from treatments )"
    #     sql2 = "select count(*) from dogs where dog_id not in ( select dog_id from treatments )"
    #
    #     self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql6(self):
        sql1 = "select count(*) from owners where state = 'vermont'"
        sql2 = "SELECT first_name, last_name, email_address FROM owners WHERE state like '%north%'"

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql7(self):
        sql1 = "select age from dogs order by age"
        sql2 = "SELECT count(*) FROM dogs WHERE age < 4"

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql8(self):
        sql1 = "select transcript_date from transcripts order by transcript_date asc limit 1"
        sql2 = "SELECT transcript_date FROM transcripts order by transcript_date desc LIMIT 1"

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql8(self):
        sql1 = "select transcript_date from transcripts order by transcript_date asc limit 1"
        sql2 = "SELECT transcript_date FROM transcripts group by transcript_date"

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql9(self):
        sql1 = "select transcript_date from transcripts order by transcript_date asc limit 1"
        sql2 = "SELECT transcript_date FROM transcripts group by transcript_date having transcript_date = 2"

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql10(self):
        sql1 = "select * from teacher where age = 32"
        sql2 = "SELECT * FROM teacher WHERE age = 32 or age = 33"

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql10(self):
        sql1 = "select * from teacher where age = 32"
        sql2 = "SELECT * FROM teacher WHERE age = 32 and age = 33"

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)
