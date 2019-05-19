from sqltools.parser import *
from tests.testclass import SqltoolsTest

import sqlparse

class ParserTest(SqltoolsTest):
    def test_handle_pair1(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.COL, value="a"))
        node.children[0].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[0].children.append(TreeNode(State.TERMINAL, value="2"))

        tn = TreeNode(State.ROOT)
        tokens= sqlparse.parse('a = 2')[0].tokens[0].tokens

        Parser.handle_pair(tn, tokens)

        self.assertTreeEqual(tn, node)

    def test_handle_pair2(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.COL, value="a"))
        node.children[0].children.append(TreeNode(State.AGG, value="min"))
        node.children[0].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[1].children.append(TreeNode(State.TERMINAL, value="2"))

        tn = TreeNode(State.ROOT)
        Parser.handle_pair(tn, sqlparse.parse('min(a) = 2')[0].tokens[0])

        self.assertTreeEqual(tn, node)

    def test_handle_pair3(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.COL, value="a"))
        node.children[0].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[0].children.append(TreeNode(State.TERMINAL, value="'2'"))

        tn = TreeNode(State.ROOT)
        Parser.handle_pair(tn, sqlparse.parse("a = '2'")[0].tokens[0])

        self.assertTreeEqual(tn, node)

    def test_select1(self):
        node = TreeNode(State.SELECT)
        node.children.append(TreeNode(State.FROM))
        node.children[0].children.append(TreeNode(State.TABLE, value='instructor'))
        node.children.append(TreeNode(State.COL, value="salary"))
        node.children[1].children.append(TreeNode(State.AGG, value="max"))
        node.children.append(TreeNode(State.COL, value="department_name"))

        sql = "SELECT max( salary ), department_name FROM instructor"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.SELECT)
        Parser.handle_select(tn, token)

        self.assertTreeEqual(tn, node)

    def test_select2(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        sql = "SELECT salary FROM instructor LIMIT 1"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)


    def test_root2(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value='instructor'))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        node.children[0].children[0].children[1].children.append(TreeNode(State.AGG, value="max"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="department_name"))
        node.children[0].children.append(TreeNode(State.WHERE))
        node.children[0].children[1].children.append(TreeNode(State.COL, value="a"))
        node.children[0].children[1].children[0].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.TERMINAL, value="2"))

        sql = "SELECT max(salary), department_name FROM instructor WHERE a = 2"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)

    def test_root_ge(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value='instructor'))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        node.children[0].children[0].children[1].children.append(TreeNode(State.AGG, value="max"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="department_name"))
        node.children[0].children.append(TreeNode(State.WHERE))
        node.children[0].children[1].children.append(TreeNode(State.COL, value="a"))
        node.children[0].children[1].children[0].children.append(TreeNode(State.OP, value=">="))
        node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.TERMINAL, value="2"))

        sql = "SELECT max(salary), department_name FROM instructor WHERE a >= 2"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)

    def test_root1(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value='instructor'))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        node.children[0].children[0].children[1].children.append(TreeNode(State.AGG, value="max"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="department_name"))

        sql = "SELECT max(salary), department_name FROM instructor"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)

    def test_root3(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value='instructor'))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        node.children[0].children[0].children[1].children.append(TreeNode(State.AGG, value="max"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="department_name"))
        node.children[0].children.append(TreeNode(State.GROUP_BY))
        node.children[0].children[1].children.append(TreeNode(State.COL, value="department_name"))

        sql = "SELECT max(salary), department_name FROM instructor GROUP BY department_name"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)

    def test_group1(self):
        node = TreeNode(State.GROUP_BY)
        node.children.append(TreeNode(State.COL, value="department_name"))

        sql = "GROUP BY department_name LIMIT 1"
        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.GROUP_BY)

        Parser.handle_group(tn, token)

        self.assertTreeEqual(tn, node)

    def test_select4(self):
        node = TreeNode(State.SELECT)
        node.children.append(TreeNode(State.FROM))
        node.children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        node.children.append(TreeNode(State.COL, value="*"))

        sql = "SELECT * FROM instructor"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.SELECT)
        Parser.handle_select(tn, token)

        self.assertTreeEqual(tn, node)

    def test_select3(self):
        node = TreeNode(State.SELECT)
        node.children.append(TreeNode(State.FROM))
        node.children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        node.children.append(TreeNode(State.COL, value="*"))
        node.children.append(TreeNode(State.COL, value="department_name"))

        sql = "SELECT *, department_name FROM instructor"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.SELECT)
        Parser.handle_select(tn, token)

        self.assertTreeEqual(tn, node)

    def test_group2(self):
        node = TreeNode(State.GROUP_BY)
        node.children.append(TreeNode(State.COL, value="department_name"))
        node.children.append(TreeNode(State.HAVING))
        node.children[1].children.append(TreeNode(State.COL, value="salary"))
        node.children[1].children[0].children.append(TreeNode(State.AGG, value="avg"))
        node.children[1].children[0].children.append(TreeNode(State.OP, value=">"))
        node.children[1].children[0].children[1].children.append(TreeNode(State.TERMINAL, value="1"))

        sql = "GROUP BY department_name HAVING avg(salary) > 1"
        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.GROUP_BY)
        Parser.handle_group(tn, token)

        self.assertTreeEqual(tn, node)

    def test_group3(self):
        node = TreeNode(State.GROUP_BY)
        node.children.append(TreeNode(State.COL, value="department_name"))
        node.children.append(TreeNode(State.HAVING))
        node.children[1].children.append(TreeNode(State.COL, value="salary"))
        node.children[1].children[0].children.append(TreeNode(State.AGG, value="avg"))
        node.children[1].children[0].children.append(TreeNode(State.OP, value=">"))

        newroot = TreeNode(State.ROOT)
        node.children[1].children[0].children[1].children.append(newroot)

        newroot.children.append(TreeNode(State.NONE))
        newroot.children[0].children.append(TreeNode(State.SELECT))
        newroot.children[0].children[0].children.append(TreeNode(State.FROM))
        newroot.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        newroot.children[0].children[0].children.append(TreeNode(State.COL, value="salary"))
        newroot.children[0].children[0].children[1].children.append(TreeNode(State.AGG, value="avg"))

        sql = "GROUP BY department_name HAVING avg(salary) > (SELECT avg(salary) FROM instructor)"
        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.GROUP_BY)
        Parser.handle_group(tn, token)

        self.assertTreeEqual(tn, node)

    def test_or(self):
        node = TreeNode(State.WHERE)
        node.children.append(TreeNode(State.LOGIC, value="or"))
        node.children[0].children.append(TreeNode(State.COL, value="city"))
        node.children[0].children[0].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TERMINAL, value='"Aberdeen"'))
        node.children[0].children.append(TreeNode(State.COL, value="city"))
        node.children[0].children[1].children.append(TreeNode(State.OP, value="="))
        node.children[0].children[1].children[0].children.append(TreeNode(State.TERMINAL, value='"Abilene"'))

        sql = 'WHERE city  =  "Aberdeen" OR city  =  "Abilene"'
        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.WHERE)
        Parser.handle_where(tn, token)

        self.assertTreeEqual(tn, node)

    def test_union(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.IUE, value="union"))
        node.children[0].children.append(TreeNode(State.ROOT))
        node.children[0].children[0].children.append(TreeNode(State.NONE))
        node.children[0].children[0].children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value='flights'))
        node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.COL, value="sourceairport"))
        node.children[0].children.append(TreeNode(State.ROOT))
        node.children[0].children[1].children.append(TreeNode(State.NONE))
        node.children[0].children[1].children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[1].children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value='flights'))
        node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.COL, value="destairport"))

        sql = "SELECT SourceAirport FROM Flights UNION SELECT DestAirport FROM Flights"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)

    def test_complex(self):
        root = TreeNode(State.ROOT)
        root.children.append(TreeNode(State.NONE))
        root.children[0].children.append(TreeNode(State.SELECT))
        root.children[0].children[0].children.append(TreeNode(State.FROM))
        root.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="airports"))
        root.children[0].children[0].children.append(TreeNode(State.COL, value="airportname"))
        root.children[0].children.append(TreeNode(State.WHERE))
        root.children[0].children[1].children.append(TreeNode(State.COL, value="airportcode"))
        root.children[0].children[1].children[0].children.append(TreeNode(State.OP, value="not in"))

        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.IUE, value="union"))
        node.children[0].children.append(TreeNode(State.ROOT))
        node.children[0].children[0].children.append(TreeNode(State.NONE))
        node.children[0].children[0].children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="flights"))
        node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.COL, value="sourceairport"))
        node.children[0].children.append(TreeNode(State.ROOT))
        node.children[0].children[1].children.append(TreeNode(State.NONE))
        node.children[0].children[1].children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[1].children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="flights"))
        node.children[0].children[1].children[0].children[0].children.append(TreeNode(State.COL, value="destairport"))

        root.children[0].children[1].children[0].children[0].children.append(node)

        sql = "SELECT AirportName FROM Airports WHERE AirportCode NOT IN (SELECT SourceAirport FROM Flights UNION SELECT DestAirport FROM Flights)"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, root)

    def test_tables_1(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        sql = "SELECT salary FROM instructor LIMIT 1"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token, col_map={'salary': 'instructor.salary'})

        self.assertTreeEqual(tn, node)

    def test_tables_2(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        sql = "SELECT t1.salary FROM instructor AS t1 LIMIT 1"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token, col_map={'t1.salary': 'instructor.salary'})

        self.assertTreeEqual(tn, node)

    def test_tables_3(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="othertable"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        sql = "SELECT t1.salary FROM instructor AS t1 JOIN othertable AS t2 LIMIT 1"
        token = sqlparse.parse(sql)[0]

        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token, col_map={'t1.salary': 'instructor.salary'})

        self.assertTreeEqual(tn, node)

    def test_tables_3(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        sql = "SELECT salary FROM instructor AS t1 LIMIT 1"

        table_info = {
            'instructor': ['salary', 'hours'],
            'othertable': ['abc']
        }

        tn = to_tree(sql, table_info=table_info)

        self.assertTreeEqual(tn, node)

    def test_tables_4(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        sql = "SELECT instructor.salary FROM instructor AS t1 LIMIT 1"

        table_info = {
            'instructor': ['salary', 'hours'],
            'othertable': ['abc']
        }

        tn = to_tree(sql, table_info=table_info)

        self.assertTreeEqual(tn, node)

    def test_tables_5(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        sql = "SELECT t1.salary FROM instructor AS t1 LIMIT 1"

        table_info = {
            'instructor': ['salary', 'hours'],
            'othertable': ['abc']
        }

        tn = to_tree(sql, table_info=table_info)

        self.assertTreeEqual(tn, node)

    def test_tables_6(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="instructor"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.salary"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="instructor.hours"))
        node.children[0].children.append(TreeNode(State.LIMIT, value='1'))

        sql = "SELECT salary, hours FROM insTructor LIMIT 1"

        table_info = {
            'Instructor': ['salary', 'hours'],
            'othertable': ['abc']
        }

        tn = to_tree(sql, table_info=table_info)

        self.assertTreeEqual(tn, node)

    def test_tables_7(self):
        table_info = {
            'airports': ['city', 'airportcode', 'airportname', 'country', 'countryabbrev', 'apid', 'name', 'city', 'country', 'x', 'y', 'elevation', 'iata', 'icao']
        }

        sql1 = 'select airports.city, airports.airportcode from airports where airports.city = "anthony" '
        sql2 = to_sql(to_tree(sql1, table_info=table_info)).lower()
        
        self.assertEqual(sql1, sql2)

    def test_conv1(self):
        sql1 = "select cost_of_treatment from treatments limit 1"
        sql2 = to_sql(to_tree(sql1)).lower()

        self.assertEqual(sql1, sql2)
    
    def test_orderby_1(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="treatments"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="cost_of_treatment"))
        node.children[0].children.append(TreeNode(State.ORDER_BY, value='desc'))
        node.children[0].children[1].children.append(TreeNode(State.COL, value="date_of_treatment"))

        sql = "select cost_of_treatment from treatments order by date_of_treatment DESC"

        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)

    def test_orderby_1(self):
        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="treatments"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="cost_of_treatment"))
        node.children[0].children.append(TreeNode(State.ORDER_BY, value='desc'))
        node.children[0].children[1].children.append(TreeNode(State.COL, value="*"))
        node.children[0].children[1].children[0].children.append(TreeNode(State.AGG, value="count"))

        sql = "select cost_of_treatment from treatments order by count(*) DESC"

        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)

    # def test_conv10(self):
    #     sql1 = "select cost_of_treatment from treatments order by date_of_treatment desc limit 1"
    #     sql2 = to_sql(to_tree(sql1)).lower()

    #     self.assertEqual(sql1, sql2)

    def test_between_1(self):
        node = TreeNode(State.WHERE)
        node.children.append(TreeNode(State.COL, value="col"))
        node.children[0].children.append(TreeNode(State.OP, value='between'))
        node.children[0].children[0].children.append(TreeNode(State.TERMINAL, value="1"))
        node.children[0].children[0].children.append(TreeNode(State.TERMINAL, value="2"))

        sql = "WHERE col between 1 and 2"
        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.WHERE)
        Parser.handle_where(tn, token)

        self.assertTreeEqual(tn, node)

    def test_join(self):
        sql = "select a from owners as t1 join dogs as t2 on t1.owner_id  =  t2.owner_id"

        node = TreeNode(State.ROOT)
        node.children.append(TreeNode(State.NONE))
        node.children[0].children.append(TreeNode(State.SELECT))
        node.children[0].children[0].children.append(TreeNode(State.FROM))
        node.children[0].children[0].children[0].children.append(TreeNode(State.JOIN))
        node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="owners"))
        node.children[0].children[0].children[0].children[0].children[0].children.append(TreeNode(State.COL, value="owner_id"))
        node.children[0].children[0].children[0].children[0].children.append(TreeNode(State.TABLE, value="dogs"))
        node.children[0].children[0].children[0].children[0].children[1].children.append(TreeNode(State.COL, value="owner_id"))
        node.children[0].children[0].children.append(TreeNode(State.COL, value="a"))

        token = sqlparse.parse(sql)[0]
        tn = TreeNode(State.ROOT)
        Parser.handle(tn, token)

        self.assertTreeEqual(tn, node)

    def test_join_conv(self):
        sql1 = "select a from owners as t1 join dogs as t2 on t1.owner_id  =  t2.owner_id"
        sql2 = to_sql(to_tree(sql1))
        new_sql = "select a from owners join dogs on owners.owner_id = dogs.owner_id "

        self.assertEqual(sql2.lower(), new_sql.lower())

    def test_join_conv_2(self):
        sql1 = "select a from owners join dogs on owners.owner_id = dogs.owner_id "
        sql2 = to_sql(to_tree(sql1))

        self.assertEqual(sql1.lower(), sql2.lower())

    def test_conv2(self):
        sql1 = "select * from mytable "
        sql2 = to_sql(to_tree(sql1))

        self.assertEqual(sql1.lower(), sql2.lower())

    def test_conv2(self):
        sql1 = "select * from mytable WHERE col between 1 and 2 "
        sql2 = to_sql(to_tree(sql1))

        self.assertEqual(sql1.lower(), sql2.lower())

    def test_conv3(self):
        sql1 = "select DISTINCT col from mytable WHERE col between 1 and 2 "
        sql2 = to_sql(to_tree(sql1))

        self.assertEqual(sql1.lower(), sql2.lower())

    def test_ignore(self):
        sql1 = "select documents.*"
        tree = to_tree(sql1, ignore={
            State.FROM: True
        })
        sql2 = to_sql(tree).strip()

        self.assertEqual(sql1.lower(), sql2.lower())
