from sqltools.tree import *
from sqltools.types import *
from sqltools.utils import *

import sqlparse

t = sqlparse.tokens.Token

class Parser:
    IUE = ["intersect", "union", "except"]
    KEYWORDS = [(State.SELECT, None, 'SELECT'), (State.WHERE, sqlparse.sql.Where, None), (State.GROUP_BY, None, 'GROUP BY'), 
        (State.LIMIT, None, 'LIMIT') , (State.ORDER_BY, None, 'ORDER BY')]

    def handle(node, token):
        if node.type == State.ROOT:
            Parser.handle_root(node, token)
        elif node.type == State.NONE:
            Parser.handle_keyword(node, token)
        elif node.type == State.SELECT:
            Parser.handle_select(node, token)
        elif node.type == State.WHERE:
            Parser.handle_where(node, token)
        elif node.type == State.COL:
            Parser.handle_col(node, token)
        elif node.type == State.GROUP_BY:
            Parser.handle_group(node, token)
        elif node.type == State.TERMINAL:
            Parser.handle_terminal(node, token)
        elif node.type == State.LIMIT:
            Parser.handle_limit(node, token)
    
    @staticmethod
    def handle_limit(node, tokens):
        for tok in tokens:
            if type(tok) is sqlparse.sql.Token and tok.ttype == t.Literal.Number.Integer:
                node.value = tok.value

    @staticmethod
    def handle_pair(node, tokens):
        cur_tokens = []

        if type(tokens) is sqlparse.sql.Comparison:
            cur_tokens = get_toks(tokens)
        elif type(tokens) is list and len(tokens) == 1:
            cur_tokens = get_toks(tokens[0].tokens)
        else:
            cur_tokens = get_toks(tokens)

        left = cur_tokens[0]
        op = cur_tokens[1].value
        right = cur_tokens[-1]

        if len(cur_tokens) > 3:
            op = ' '.join(c.value for c in cur_tokens[1:-1])

        n = TreeNode(State.COL)
        Parser.handle(n, left)
        node.children.append(n)

        cn = TreeNode(State.OP, value=op.lower())
        n.children.append(cn)

        leaf_node = None

        if type(right) is sqlparse.sql.Parenthesis:
            leaf_node = TreeNode(State.ROOT)
            Parser.handle(leaf_node, right)
        else:
            leaf_node = TreeNode(State.TERMINAL, value=right.value)

        cn.children.append(leaf_node)
            
    @staticmethod
    def handle_col(node, token):
        if type(token) is sqlparse.sql.Function:
            n = TreeNode(State.AGG, value = token.tokens[0].value)
            node.children.append(n)
            node.value = token.tokens[-1].tokens[1].value
        else:
            node.value = token.value

    @staticmethod
    def handle_select(node, tokens):
        cur_tokens = get_toks(tokens)
        cols = inbetween_toks(cur_tokens, sqlparse.sql.Token, 'select', sqlparse.sql.Token, 'from')

        for c in cols:
            if type(c) is sqlparse.sql.IdentifierList:
                for k in c.tokens:
                    if type(k) is sqlparse.sql.Function or type(k) is sqlparse.sql.Identifier or (type(k) is sqlparse.sql.Token and k.value == '*'):
                        new_node = TreeNode(State.COL)
                        Parser.handle(new_node, k)
                        node.children.append(new_node)

            if type(c) is sqlparse.sql.Function or type(c) is sqlparse.sql.Identifier or (type(c) is sqlparse.sql.Token and c.value == '*'):
                new_node = TreeNode(State.COL)
                Parser.handle(new_node, c)
                node.children.append(new_node)
        
        tables = inbetween_toks_multi(cur_tokens, sqlparse.sql.Token, 'from', [(y, z) for x, y, z in Parser.KEYWORDS[1:]])

        node.attr['tables'] = []

        for t in tables[1:]:
            if type(t) is sqlparse.sql.Identifier:
                node.attr['tables'].append(t.value)
        
    staticmethod
    def handle_root(node, tokens):
        tokens = get_toks(tokens)

        for x in Parser.IUE:
            i = find_token(tokens, sqlparse.sql.Token, x.lower())

            if i >= 0:
                left, right = tokens[:i], tokens[i+1:]
                left_node, right_node = TreeNode(State.ROOT), TreeNode(State.ROOT)

                Parser.handle(left_node, left)
                Parser.handle(right_node, right)

                new_node = TreeNode(State.IUE, value=x)
                new_node.children.append(left_node)
                new_node.children.append(right_node)

                node.children.append(new_node)
                return

        new_node = TreeNode(State.NONE)
        node.children.append(new_node)
        Parser.handle_keyword(new_node, tokens)

    @staticmethod
    def handle_op(node, token):
        if token is sqlparse.sql.Identifier:
            n = TreeNode(State.TERMINAL, value = token.tokens[0].value)
            node.children.append(n)

    @staticmethod
    def handle_keyword(node, tokens):
        tokens = get_toks(tokens)

        for state, typ, name in Parser.KEYWORDS:
            i = find_token(tokens, typ=typ, value=name)
            
            if i >= 0:
                new_node = TreeNode(state)
                new_tokens = inbetween_toks_multi(tokens, typ, name, [(y, z) for x, y, z in Parser.KEYWORDS])
                Parser.handle(new_node, new_tokens)
                node.children.append(new_node)

    @staticmethod
    def handle_group(node, tokens):
        tokens = get_toks(tokens)

        for i, token in enumerate(tokens):
            if type(token) is sqlparse.sql.Token and token.value.lower() == 'having':
                new_node = TreeNode(State.HAVING)
                Parser.handle_logic(new_node, tokens[i+1:])
                node.children.append(new_node)
                return

            if type(token) is sqlparse.sql.Identifier:
                new_node = TreeNode(State.COL)
                Parser.handle(new_node, token)
                node.children.append(new_node)

    @staticmethod
    def handle_where(node, tokens):
        token = get_toks(tokens[0].tokens)

        Parser.handle_logic(node, token[1:])

    @staticmethod
    def handle_logic(node, tokens):
        tokens = get_toks(tokens)

        for idx, token in enumerate(tokens):
            if type(token) is sqlparse.sql.Token and token.value.lower() == 'and':
                new_node = TreeNode(State.LOGIC, value='and')
                
                Parser.handle_logic(new_node, tokens[:idx])
                Parser.handle_logic(new_node, tokens[idx+1:])

                node.children.append(new_node)

                return

            if type(token) is sqlparse.sql.Token and token.value.lower() == 'or':
                new_node = TreeNode(State.LOGIC, value='or')
                
                Parser.handle_logic(new_node, tokens[:idx])
                Parser.handle_logic(new_node, tokens[idx+1:])

                node.children.append(new_node)

                return

        Parser.handle_pair(node, tokens)

class Unparser:
    def unparse(node):
        if node.type == State.ROOT:
            return Unparser.unparse_root(node)
        elif node.type == State.NONE:
            return Unparser.unparse_keyword(node)
        elif node.type == State.SELECT:
            return Unparser.unparse_select(node)
        elif node.type == State.WHERE:
            return Unparser.unparse_where(node)
        elif node.type == State.COL:
            return Unparser.unparse_col(node)
        elif node.type == State.OP:
            return Unparser.unparse_op(node)
        elif node.type == State.TERMINAL:
            return Unparser.unparse_terminal(node)
        
        return ""

    def unparse_root(node):
        if len(node.children) > 0:
            return Unparser.unparse(node.children[0])

        return ""

    def unparse_keyword(node):
        res = ""

        for c in node.children:
            res = res + Unparser.unparse(c)

        return res

    def unparse_select(node):
        res = node.type.name.upper() + " "

        for c in node.children:
            res = res + Unparser.unparse(c)

        res = res + " FROM "

        res = res + ', '.join(node.attr['tables']) + " "

        return res

    def unparse_where(node):
        res = node.type.name.upper() + " "

        for c in node.children:
            res = res + Unparser.unparse(c)

        return res
    
    def unparse_col(node):
        res = node.value

        for c in node.children:
            if c.type == State.AGG:
                res = c.value + '(' + res + ')'
            else:
                res = res + Unparser.unparse(c)
        
        return res

    def unparse_op(node):
        res = " " + node.value + " "

        for c in node.children:
            if c.type == State.ROOT:
                res = res + '(' + Unparser.unparse(c) + ')'
            else:
                res = res + Unparser.unparse(c)
        return res

    def unparse_terminal(node):
        return node.value

def to_tree(sql, tables=None):
    """Converts a sql string into a tree of type TreeNode 
    :param sql: a sql string

    :return: A TreeNode
    """
    if type(sql) is not str:
        raise TypeError("SQL must be a string")

    node = TreeNode(State.ROOT)
    tables = {} if tables is None else tables
    tokens = sqlparse.parse(sql)[0].tokens

    Parser.handle(node, tokens)

    return node

def to_sql(root):
    """Converts a Tree Node to an sql string 
    :param sql: a sql string

    :return: An String
    """
    if type(root) is not TreeNode:
        raise TypeError("Node is not of type treenode")

    return Unparser.unparse(root)

    