from sqltools.sequence import *
from sqltools.tree import *
from sqltools.types import *
from sqltools.parser import *
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
        sql2 = "SELECT count(*) FROM professionals WHERE city = 'West Heidi' "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql2(self):
        sql1 = "SELECT * FROM AIRLINES WHERE Airline = \"JetBlue Airways\""
        sql2 = "SELECT country FROM airlines WHERE airline = \"JetBlue Airways\" "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql3(self):
        sql1 = "SELECT Country FROM AIRLINES WHERE Airline  =  \"JetBlue Airways\""
        sql2 = "SELECT * FROM airlines WHERE airline = \"JetBlue Airways\" "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql4(self):
        sql1 = "SELECT * FROM Owners"
        sql2 = "SELECT count(*) FROM owners WHERE state = 'Arizona' "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql5(self):
        sql1 = "select count(*) from dogs where dog_id in ( select dog_id from treatments )"
        sql2 = "SELECT count(*) FROM dogs WHERE dog_id not in (SELECT dog_id FROM treatments ) "
    
        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql6(self):
        sql1 = "select count(*) from owners where state = 'vermont'"
        sql2 = "SELECT first_name, last_name, email_address FROM owners WHERE state like '%north%' "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql7(self):
        sql1 = "select age from dogs order by age"
        sql2 = "SELECT count(*) FROM dogs WHERE age < 4 "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql8(self):
        sql1 = "select transcript_date from transcripts order by transcript_date asc limit 1"
        sql2 = "SELECT transcript_date FROM transcripts order by transcript_date desc LIMIT 1"

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql8(self):
        sql1 = "select transcript_date from transcripts order by transcript_date asc limit 1"
        sql2 = "SELECT transcript_date FROM transcripts group by transcript_date "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql9(self):
        sql1 = "select transcript_date from transcripts order by transcript_date asc limit 1"
        sql2 = "SELECT transcript_date FROM transcripts group by transcript_date having transcript_date = 2 "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql10(self):
        sql1 = "select * from teacher where age = 32"
        sql2 = "SELECT * FROM teacher WHERE age = 32 or age = 33 "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql10(self):
        sql1 = "select * from teacher where age = 32"
        sql2 = "SELECT * FROM teacher WHERE age = 32 and age = 33 "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql11(self):
        sql1 = "select age from singer where country = 'france'"
        sql2 = "SELECT avg(age), min(age), max(age) FROM singer WHERE country = 'france' "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql12(self):
        sql1 = "select * from votes where state = 'ny' or state = 'ca'"
        sql2 = "SELECT count(*) FROM votes WHERE state = 'ny' or state = 'ca' "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_sql_sequence_linear(self):
        sql1 = 'SELECT count(*) FROM Professionals'
        sql2 = "SELECT count(*) FROM Professionals WHERE city = 'West Heidi' "

        self.assertListEqual(generate_sequence_sql(sql1, sql2, linear_insert=True), ['copyandchange', 'copyandchange[WHERE city = \'West Heidi\' ]', 'copy'])

    def test_applysql_sequence_linear(self):
        sql1 = 'SELECT count(*) FROM professionals'
        sql2 = "SELECT count(*) FROM professionals WHERE city = 'West Heidi' "

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear2(self):
        sql1 = "select count(*) from owners where state = 'vermont'"
        sql2 = "SELECT first_name, last_name, email_address, avg(num) FROM owners WHERE state = 'vermont' "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear3(self):
        sql1 = "select count(*) from owners where state = 'vermont'"
        sql2 = "SELECT first_name, last_name, email_address FROM owners WHERE state like '%north%' "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear4(self):
        sql1 = "select count(*) from owners where state = 'vermont'"
        sql2 = "SELECT first_name, last_name, email_address FROM owners WHERE state not in '%north%' "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear5(self):
        sql1 = "select count(*) from owners where state = 'vermont'"
        sql2 = "SELECT first_name, last_name, email_address FROM owners WHERE state not in '%north%' "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear6(self):
        sql1 = "SELECT * FROM AIRLINES WHERE Airline = \"JetBlue Airways\""
        sql2 = "SELECT country FROM airlines WHERE airline = \"JetBlue Airways\" "

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear7(self):
        sql1 = "SELECT Country FROM AIRLINES WHERE Airline  =  \"JetBlue Airways\""
        sql2 = "SELECT * FROM airlines WHERE airline = \"JetBlue Airways\" "

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear8(self):
        sql1 = "SELECT * FROM Owners"
        sql2 = "SELECT count(*) FROM owners WHERE state = 'Arizona' "

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear9(self):
        sql1 = "select count(*) from dogs where dog_id in ( select dog_id from treatments )"
        sql2 = "SELECT count(*) FROM dogs WHERE dog_id not in (SELECT dog_id FROM treatments ) "

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear10(self):
        sql1 = "select age from dogs order by age"
        sql2 = "SELECT count(*) FROM dogs WHERE age < 4 "

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    # def test_applysql_sequence_linear11(self):
    #     sql1 = "select transcript_date from transcripts order by transcript_date asc limit 1"
    #     sql2 = "SELECT transcript_date FROM transcripts order by transcript_date desc LIMIT 1"

    #     self.assertEqual(
    #         apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear12(self):
        sql1 = "select transcript_date from transcripts order by transcript_date asc limit 1"
        sql2 = "SELECT transcript_date FROM transcripts group by transcript_date "

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear13(self):
        sql1 = "select transcript_date from transcripts order by transcript_date asc limit 1"
        sql2 = "SELECT transcript_date FROM transcripts group by transcript_date having transcript_date = 2 "

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    # def test_applysql_sequence_linear14(self):
    #     sql1 = "select * from teacher where age = 32"
    #     sql2 = "SELECT * FROM teacher WHERE age = 32 or age = 33"

    #     self.assertEqual(
    #         apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    # def test_applysql_sequence_linear15(self):
    #     sql1 = "select * from teacher where age = 32"
    #     sql2 = "SELECT * FROM teacher WHERE age = 32 and age = 33 "

    #     self.assertEqual(
    #         apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear16(self):
        sql1 = "select age from singer where country = 'france'"
        sql2 = "SELECT avg(age), min(age), max(age) FROM singer WHERE country = 'france' "

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_applysql_sequence_linear17(self):
        sql1 = "select * from votes where state = 'ny' or state = 'ca'"
        sql2 = "SELECT count(*) FROM votes WHERE state = 'ny' or state = 'ca' "

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True), linear_insert=True), sql2)

    def test_apply_sequence_ignore_linear1(self):
        sql1 = "select count(distinct hiring.shop_id)"
        sql2 = "SELECT shop.name "

        ignore = {
            State.FROM: True
        }

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True, ignore=ignore), linear_insert=True, ignore=ignore), sql2)

    def test_apply_sequence_ignore_1(self):
        sql1 = "select employee.name"
        sql2 = "select employee.name where employee.employee_id not in (select evaluation.employee_id ) "

        ignore = {
            State.FROM: True
        }

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, ignore=ignore), ignore=ignore).lower(), sql2)

    # def test_apply_sequence_sql13(self):
    #     sql1 = "select carrier from device"
    #     sql2 = "SELECT count(DISTINCT carrier) FROM device"
    #
    #     tree_print(to_tree(sql2))
    #     print(generate_sequence_sql(sql1, sql2))
    #
    #     self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_apply_sequence_sql14(self):
        sql1 = "select country from singer where age > 20"
        sql2 = "SELECT DISTINCT country FROM singer WHERE age > 20 "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    # def test_apply_sequence_sql15(self):
    #     sql1 = "select distinct car_names.model from tbl"
    #     sql2 = "select car_names.model , car_names.make from tbl"

    #     self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    # def test_distinct_multiple(self):
    #     sql1 = "select distinct paintings.medium"
    #     sql2 = "select avg(paintings.height_mm), paintings.medium group by paintings.medium"

    #     ignore={
    #         State.FROM: True
    #     }

    #     self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, ignore=ignore), ignore=ignore), sql2)

    # def test_get_node_from_sequence(self):
    #     sql1 = 'SELECT count(*) FROM Professionals'
    #     sql2 = "SELECT count(*) FROM Professionals WHERE city = 'West Heidi'"

    #     tree = to_tree(sql1)

    #     self.assertTreeEqual(get_node_from_sequence(tree, sequence[:2]), tree.children[0].children[0])

    def test_apply_sequence_sql16(self):
        sql1 = "select name, number_products from shop"
        sql2 = "SELECT avg(number_products) FROM shop "

        self.assertEqual(apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2)), sql2)

    def test_conv_ignore_linear_1(self):
        sql1 = "select * where student.sex = value"
        sql2 = "SELECT * WHERE student.sex = value and pets.pettype = value "


        ignore = {
            State.FROM: True
        }

        self.assertEqual(
            apply_sequence_sql(sql1, generate_sequence_sql(sql1, sql2, linear_insert=True, ignore=ignore), linear_insert=True, ignore=ignore), sql2)
