from sqltools.tree import *
from sqltools.types import *
from sqltools.utils import *

class Parser:
    IUE = ["intersect", "union", "except"]
    KEYWORD = ["select", "where", "group by", "order by", "having"]
    KEYWORD_STATE = [State.SELECT, State.WHERE, State.GROUP, State.ORDER, State.HAVING]
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

    @staticmethod
    def handle_root(node, sql):
        for x in IUE:
            if sql.lower().find(x) >= 0:
                left, right = split_string(sql, x)
                left_node, right_node = TreeNode(State.ROOT), TreeNode(State.ROOT)

                Parser.handle(left_node, left)
                Parser.handle(right_node, right)

                return

        handle_keyword(node, sql)

    @staticmethod
    def handle_select(node, sql):
        cols = in_between(new_sql, 'SELECT', 'FROM').split(',')

        for c in cols:
            new_node = TreeNode(State.COL)
            new_node.attr['value'] = c.strip()
        
    @staticmethod
    def handle_where(node, sql):
        new_sql = split_string(sql, 'where')
        new_sql, _ = split_string_seq(new_sql, Parser.KEYWORD[1:])
        # conds = split_multiple(new_sql, [' and ', ' or '])
        # TODO: AND/OR
        handle_pair(node, new_sql)

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
        left_node.attr['value'] = left.strip()

        right_node = TreeNode(State.OP)
        right_node.attr['value'] = op

        child_node = None
        
        if comp_state == State.TERMINAL:
            child_node = TreeNode(State.TERMINAL)
            child_node.attr['value'] = comp
        else:
            child_node = TreeNode(State.ROOT)
            Parser.handle(child_node, remove_front_parenthesis(comp))

        right_node.append(child_node)

        node.append(left_node, right_node)

    @staticmethod
    def get_state(sql):
        if sql[0] == "(":
            return State.ROOT
        elif sql[0] == "\"" or sql[0].isdigit():
            return State.TERMINAL
        
        return State.COL

    @staticmethod
    def handle_keyword(node, sql):
        for idx, w in enumerate(Parser.KEYWORD):
            state = Parser.KEYWORD_STATE[idx]
            if sql.lower().find(w) >= 0:
                new_node = TreeNode(state)
                Parser.handle(new_node, sql)
                    

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

    