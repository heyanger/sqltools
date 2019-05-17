from sqltools.tree import *
from sqltools.types import *
from sqltools.utils import *

import sqlparse

t = sqlparse.tokens.Token

class Parser:
    IUE = ["intersect", "union", "except"]
    KEYWORDS = [(State.SELECT, None, 'SELECT'), (State.WHERE, sqlparse.sql.Where, None), (State.GROUP_BY, None, 'GROUP BY'),
        (State.ORDER_BY, None, 'ORDER BY'), (State.LIMIT, None, 'LIMIT')]

    def handle(node, token, col_map=None):
        if node.type == State.ROOT:
            Parser.handle_root(node, token, col_map)
        elif node.type == State.NONE:
            Parser.handle_keyword(node, token, col_map)
        elif node.type == State.SELECT:
            Parser.handle_select(node, token, col_map)
        elif node.type == State.WHERE:
            Parser.handle_where(node, token, col_map)
        elif node.type == State.COL:
            Parser.handle_col(node, token, col_map)
        elif node.type == State.ORDER_BY:
            Parser.handle_orderby(node, token, col_map)
        elif node.type == State.GROUP_BY:
            Parser.handle_group(node, token, col_map)
        elif node.type == State.TERMINAL:
            Parser.handle_terminal(node, token, col_map)
        elif node.type == State.LIMIT:
            Parser.handle_limit(node, token, col_map)

    @staticmethod
    def handle_limit(node, tokens, col_map=None):
        for tok in tokens:
            if type(tok) is sqlparse.sql.Token and tok.ttype == t.Literal.Number.Integer:
                node.value = tok.value

    @staticmethod
    def handle_pair(node, tokens, col_map=None):
        cur_tokens = []

        if type(tokens) is sqlparse.sql.Comparison:
            cur_tokens = get_toks(tokens)
        elif type(tokens) is list and len(tokens) == 1:
            cur_tokens = get_toks(tokens[0].tokens)
        else:
            cur_tokens = get_toks(tokens)

        left = cur_tokens[0]
        op = cur_tokens[1].value

        n = TreeNode(State.COL)
        Parser.handle(n, left, col_map)
        node.children.append(n)

        if op.lower() != 'between':

            if len(cur_tokens) > 3:
                op = ' '.join(c.value for c in cur_tokens[1:-1])

            cn = TreeNode(State.OP, value=op.lower())
            n.children.append(cn)

            right = cur_tokens[-1]
            leaf_node = None

            if type(right) is sqlparse.sql.Parenthesis:
                leaf_node = TreeNode(State.ROOT)
                Parser.handle(leaf_node, right, col_map)
            else:
                leaf_node = TreeNode(State.TERMINAL, value=right.value)

            cn.children.append(leaf_node)

        # between
        else:
            cn = TreeNode(State.OP, value=op.lower())
            n.children.append(cn)
            right_1 = cur_tokens[-3]
            right_2 = cur_tokens[-1]
            leaf_node_1 = TreeNode(State.TERMINAL, value=right_1.value)
            leaf_node_2 = TreeNode(State.TERMINAL, value=right_2.value)
            cn.children.append(leaf_node_1)
            cn.children.append(leaf_node_2)


    @staticmethod
    def handle_orderby(node, tokens, col_map=None):
        tok = None
        if type(tokens[-1]) is sqlparse.sql.Token and tokens[-1].ttype == t.Keyword.Order:
            assert(len(tokens) == 3)

            node.value = tokens[-1].value.lower()

            tok = tokens[1]
        else:
            assert(len(tokens) == 2)

            child_tokens = get_toks(tokens[-1].tokens)

            if type(child_tokens[-1]) is sqlparse.sql.Token and child_tokens[-1].ttype == t.Keyword.Order:
                node.value = child_tokens[-1].value.lower()

            child_node = TreeNode(State.COL)

            tok = child_tokens[0]

        child_node = TreeNode(State.COL)
        Parser.handle(child_node, tok)
        node.children.append(child_node)

    @staticmethod
    def handle_col(node, token, col_map=None):
        if type(token) is sqlparse.sql.Function:
            n = TreeNode(State.AGG, value = token.tokens[0].value)
            node.children.append(n)

            node.value = Parser.generate_col_name(token.tokens[-1].tokens[1].value, col_map)
        else:
            node.value = Parser.generate_col_name(token.value, col_map)

    @staticmethod
    def generate_col_map(tokens, table_info):
        col_map = {}

        for tbl in table_info:
            for col in table_info[tbl]:
                col_map[col.lower()] = tbl.lower()+'.'+col.lower()

        return col_map

    @staticmethod
    def generate_col_name(value, col_map=None):
        if value is '*':
            return value

        value = value.lower()
        if col_map is None or value not in col_map:
            return value

        return col_map[value]

    @staticmethod
    def handle_select(node, tokens, col_map=None):
        cur_tokens = get_toks(tokens)
        cols = inbetween_toks(cur_tokens, sqlparse.sql.Token, 'select', sqlparse.sql.Token, 'from')

        Parser.handle_tables(node, cur_tokens, col_map)

        for c in cols:
            if type(c) is sqlparse.sql.IdentifierList:
                for k in c.tokens:
                    if type(k) is sqlparse.sql.Function or type(k) is sqlparse.sql.Identifier or (type(k) is sqlparse.sql.Token and k.value == '*'):
                        new_node = TreeNode(State.COL)
                        Parser.handle(new_node, k, col_map)
                        node.children.append(new_node)

            if type(c) is sqlparse.sql.Function or type(c) is sqlparse.sql.Identifier or (type(c) is sqlparse.sql.Token and c.value == '*'):
                new_node = TreeNode(State.COL)
                Parser.handle(new_node, c, col_map)
                node.children.append(new_node)

    @staticmethod
    def handle_tables(node, tokens, col_map):
        tables = inbetween_toks_multi(tokens, sqlparse.sql.Token, 'from', [(y, z) for x, y, z in Parser.KEYWORDS[1:]])

        node.attr['tables'] = []

        for t in tables[1:]:
            if type(t) is sqlparse.sql.Identifier:
                node.attr['tables'].extend(Parser.generate_table_name(t))

                Parser.update_col_map(t, col_map)

    @staticmethod
    def update_col_map(token, col_map):
        if col_map is None:
            return

        cur_tokens = get_toks(token.tokens)
        col_pair = []

        for idx, tok in enumerate(cur_tokens):
            if type(tok) is sqlparse.sql.Token and tok.ttype is t.Keyword and tok.value.lower() == 'as':
                # assume FROM contains only names, AS and identifiers
                previous = cur_tokens[idx-1].value.lower()+'.'
                nxt = cur_tokens[idx+1].value.lower()+'.'

                col_pair.append((previous, nxt))

        new_mp = {}
        for previous, nxt in col_pair:
            for key in col_map:
                value = col_map[key]
                if value.startswith(previous):
                    new_key = nxt + value.replace(previous, '', 1)
                    new_mp[new_key] = col_map[key]

        for key in new_mp:
            col_map[key] = new_mp[key]


    @staticmethod
    def generate_table_name(token):
        res = []
        for tok in token.tokens:
            if type(tok) is sqlparse.sql.Token and tok.ttype is t.Name:
                res.append(tok.value.lower())

        return res

    staticmethod
    def handle_root(node, tokens, col_map=None):
        tokens = get_toks(tokens)

        for x in Parser.IUE:
            i = find_token(tokens, sqlparse.sql.Token, x.lower())

            if i >= 0:
                left, right = tokens[:i], tokens[i+1:]
                left_node, right_node = TreeNode(State.ROOT), TreeNode(State.ROOT)

                Parser.handle(left_node, left, col_map)
                Parser.handle(right_node, right, col_map)

                new_node = TreeNode(State.IUE, value=x)
                new_node.children.append(left_node)
                new_node.children.append(right_node)

                node.children.append(new_node)
                return

        new_node = TreeNode(State.NONE)
        node.children.append(new_node)
        Parser.handle_keyword(new_node, tokens, col_map)

    @staticmethod
    def handle_op(node, token, col_map=None):
        if token is sqlparse.sql.Identifier:
            n = TreeNode(State.TERMINAL, value = token.tokens[0].value)
            node.children.append(n)

    @staticmethod
    def handle_keyword(node, tokens, col_map=None):
        tokens = get_toks(tokens)

        for state, typ, name in Parser.KEYWORDS:
            i = find_token(tokens, typ=typ, value=name)

            if i >= 0:
                new_node = TreeNode(state)
                new_tokens = inbetween_toks_multi(tokens, typ, name, [(y, z) for x, y, z in Parser.KEYWORDS])
                Parser.handle(new_node, new_tokens, col_map)
                node.children.append(new_node)

    @staticmethod
    def handle_group(node, tokens, col_map=None):
        tokens = get_toks(tokens)

        for i, token in enumerate(tokens):
            if type(token) is sqlparse.sql.Token and token.value.lower() == 'having':
                new_node = TreeNode(State.HAVING)
                Parser.handle_logic(new_node, tokens[i+1:], col_map)
                node.children.append(new_node)
                return

            if type(token) is sqlparse.sql.Identifier:
                new_node = TreeNode(State.COL)
                Parser.handle(new_node, token, col_map)
                node.children.append(new_node)

    @staticmethod
    def handle_where(node, tokens, col_map=None):
        token = get_toks(tokens[0].tokens)

        Parser.handle_logic(node, token[1:], col_map)

    @staticmethod
    def handle_logic(node, tokens, col_map=None):
        tokens = get_toks(tokens)

        print(tokens)
        print([type(t) for t in tokens])

        have_between = False
        process_between = False

        for idx, token in enumerate(tokens):
            if type(token) is sqlparse.sql.Token and token.value.lower() == 'between':
                have_between = True
                continue

            if type(token) is sqlparse.sql.Token and token.value.lower() == 'and':
                if have_between is True and process_between is False:
                    process_between = True
                    continue

                new_node = TreeNode(State.LOGIC, value='and')

                Parser.handle_logic(new_node, tokens[:idx], col_map)
                Parser.handle_logic(new_node, tokens[idx+1:], col_map)

                node.children.append(new_node)

                return

            if type(token) is sqlparse.sql.Token and token.value.lower() == 'or':
                new_node = TreeNode(State.LOGIC, value='or')

                Parser.handle_logic(new_node, tokens[:idx], col_map)
                Parser.handle_logic(new_node, tokens[idx+1:], col_map)

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
        elif node.type == State.LIMIT:
            return Unparser.unparse_limit(node)
        elif node.type == State.ORDER_BY:
            return Unparser.unparse_orderby(node)
        elif node.type == State.GROUP_BY:
            return Unparser.unparse_groupby(node)
        elif node.type == State.HAVING:
            return Unparser.unparse_having(node)
        elif node.type == State.LOGIC:
            return Unparser.unparse_logic(node)
        elif node.type == State.TERMINAL:
            return Unparser.unparse_terminal(node)

        return ""

    def unparse_root(node):
        if len(node.children) > 0:
            return Unparser.unparse(node.children[0])

        return ""

    def unparse_keyword(node):
        res = ""

        Unparser.priority_sort(node)

        for c in node.children:
            res = res + Unparser.unparse(c)

        return res

    def unparse_select(node):
        res = node.type.name.upper() + " "

        cols = []
        for c in node.children:
            cols.append(Unparser.unparse(c))

        res = res + ', '.join(cols)

        res = res + " FROM "

        res = res + ', '.join(node.attr['tables']) + " "

        return res

    def unparse_where(node):
        res = node.type.name.upper() + " "

        for c in node.children:
            res = res + Unparser.unparse(c)

        return res

    def unparse_orderby(node):
        child = []
        for c in node.children:
            child.append(Unparser.unparse(c))

        res = 'order by ' + ', '.join(child)

        if node.value is not None:
            res = res + ' ' + node.value + ' '

        return res

    def unparse_groupby(node):
        child = []
        for c in node.children:
            child.append(Unparser.unparse(c))

        res = 'group by ' + child[0]

        for str in child[1:]:
            if str.startswith('having'):
                res = res + ' ' + str
            else:
                res = res + ', ' + str

        return res

    def unparse_having(node):
        res = node.type.name.lower() + ' '

        for c in node.children:
            res = res + Unparser.unparse(c)

        return res

    def unparse_limit(node):
        return State.LIMIT.name + ' ' + node.value

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

        if node.value.lower() != 'between':
            for c in node.children:
                if c.type == State.ROOT:
                    res = res + '(' + Unparser.unparse(c) + ')'
                else:
                    res = res + Unparser.unparse(c)

        else:
            res = res + Unparser.unparse(node.children[0]) + ' and ' + Unparser.unparse(node.children[1])

        return res

    def unparse_logic(node):
        res = " " + node.value + " "
        res = Unparser.unparse(node.children[0]) + res + Unparser.unparse(node.children[1])
        return res

    def unparse_terminal(node):
        return node.value

    def priority_sort(node):
        # VERY BAD SORTING ALG
        priority_list = [State.SELECT, State.WHERE, State.GROUP_BY, State.ORDER_BY, State.LIMIT]
        ordered_list = []

        for type in priority_list:
            for c in node.children:
                if c.type == type:
                    ordered_list.append(c)

        node.children = ordered_list



def to_tree(sql, table_info=None):
    """Converts a sql string into a tree of type TreeNode
    :param sql: a sql string

    :return: A TreeNode
    """
    if type(sql) is not str:
        raise TypeError("SQL must be a string")

    node = TreeNode(State.ROOT)
    tokens = sqlparse.parse(sql)[0].tokens

    col_map = Parser.generate_col_map(tokens, table_info) if table_info is not None else None

    Parser.handle(node, tokens, col_map)

    return node

def to_sql(root):
    """Converts a Tree Node to an sql string
    :param sql: a sql string

    :return: An String
    """
    if type(root) is not TreeNode:
        raise TypeError("Node is not of type treenode")

    return Unparser.unparse(root)


