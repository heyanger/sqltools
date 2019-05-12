from sqltools.tree import *
from sqltools.types import *
from sqltools.utils import *

class Parser:
    IUE = ["intersect", "union", "except"]
    KEYWORD = ["select ", " where ", " group by ", " order by ", " having ", " limit "]
    KEYWORD_STATE = [State.SELECT, State.WHERE, State.GROUP, State.ORDER, State.HAVING, State.LIMIT]
    BOOLS = ["AND", "OR"]
    OPS = [' = ', ' < ', ' > ', ' >= ', ' <= ', ' != ', ' LIKE ', ' NOT IN ', ' BETWEEN ']
    AGG = ["max", "min", "avg", "sum", "count"]

    @staticmethod
    def handle(node, sql):
        if node.type == State.ROOT:
            Parser.handle_root(node, sql)
        elif node.type == State.SELECT:
            Parser.handle_select(node, sql)
        elif node.type == State.WHERE:
            Parser.handle_where(node, sql)
        elif node.type == State.COL:
            Parser.handle_col(node, sql)
        elif node.type == State.GROUP:
            Parser.handle_group(node, sql)

    @staticmethod
    def handle_group(node, sql):
        _, sql = split_string(sql, ' group by ')
        new_sql, _, _ = split_string_seq(sql, Parser.KEYWORD)
        
        cols = new_sql.split(',')

        for c in cols:
            c = c.strip()
            new_node = TreeNode(State.COL)
            Parser.handle(new_node, c)
            node.children.append(new_node)

        if sql.lower().find(' having ') >= 0:
            new_node = TreeNode(State.HAVING)
            _, new_sql = split_string(sql, ' having ')
            new_sql, _, _ = split_string_seq(new_sql, Parser.KEYWORD)

            print(sql)

            Parser.handle_logic(new_node, new_sql)
            node.children.append(new_node)

    @staticmethod
    def handle_root(node, sql):
        for x in Parser.IUE:
            if sql.lower().find(x) >= 0:
                left, right = split_string(sql, x)
                left_node, right_node = TreeNode(State.ROOT), TreeNode(State.ROOT)

                Parser.handle(left_node, left)
                Parser.handle(right_node, right)

                return

        Parser.handle_keyword(node, sql)

    @staticmethod
    def handle_select(node, sql):
        cols = in_between(sql, 'SELECT', 'FROM').split(',')

        for c in cols:
            new_node = TreeNode(State.COL)
            Parser.handle(new_node, c)
            node.children.append(new_node)
        
        
    @staticmethod
    def handle_where(node, sql):
        _, new_sql = split_string(sql, ' where ')
        new_sql, _, _ = split_string_seq(new_sql, Parser.KEYWORD[1:])

        Parser.handle_logic(node, new_sql)

    @staticmethod
    def handle_logic(node, sql):
        # conds = split_multiple(new_sql, [' and ', ' or '])
        # TODO: AND/OR
        Parser.handle_pair(node, sql)

    @staticmethod
    def handle_pair(node, sql):
        left, right, op = split_string_seq(sql, Parser.OPS)

        l = Parser.get_state(left)
        r = Parser.get_state(right)

        assert(l == State.COL or r == State.COL)

        col, comp, comp_state = None, None, None

        if l == State.COL:
            col = left
            comp = right
            comp_state = r
        else:
            col = right
            comp = left
            comp_state = l

        left_node = TreeNode(State.COL)
        Parser.handle(left_node, left)

        right_node = TreeNode(State.OP)
        right_node.attr['value'] = op.strip()

        child_node = None
        
        if comp_state == State.TERMINAL:
            child_node = TreeNode(State.TERMINAL)
            child_node.attr['value'] = comp
        else:
            child_node = TreeNode(State.ROOT)
            Parser.handle(child_node, remove_front_parenthesis(comp))

        right_node.children.append(child_node)

        node.children.append(left_node)
        node.children.append(right_node)

    @staticmethod
    def handle_col(node, sql):
        sql = sql.strip()
        node.attr['value'] = remove_front_parenthesis(sql)

        for agg in Parser.AGG:
            agg = agg.lower()

            if sql.find(agg+'(') == 0:    
                tn = TreeNode(State.AGG)
                node.children.append(tn)
                tn.attr['value'] = agg
                return

    @staticmethod
    def get_state(sql):
        if sql[0] == "(":
            return State.ROOT
        elif sql[0] == "\"" or sql[0].isdigit():
            return State.TERMINAL
        
        return State.COL

    @staticmethod
    def handle_keyword(node, sql):
        for idx, w in enumerate(Parser.KEYWORD[:-2]):
            state = Parser.KEYWORD_STATE[idx]
            
            if sql.lower().find(w) >= 0:
                new_node = TreeNode(state)
                Parser.handle(new_node, sql)
                node.children.append(new_node)
                    

def to_tree(sql):
    """Converts a sql string into a tree of type TreeNode 
    :param sql: a sql string

    :return: A TreeNode
    """
    if type(sql) is not str:
        raise TypeError("SQL must be a string")

    node = TreeNode(State.ROOT)
    Parser.handle(node, sql)

    return node

def to_sql(root):
    """Converts a Tree Node to an sql string 
    :param sql: a sql string

    :return: An String
    """
    if type(root) is not TreeNode:
        raise TypeError("Node is not of type treenode")

    