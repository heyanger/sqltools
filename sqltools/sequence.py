from sqltools.parser import *
from sqltools.serializer import *

import sqlparse

class Sequence:
    @staticmethod
    def compare(left, right):
        if left.value != right.value or left.type != right.type:
            left.attr['status'] = Seq.remove
            return False

        candidate = True

        idxt = 0
        for idxl, l in enumerate(left.children):
            found = False
            for r in right.children[idxl-idxt:]:
                if r.value == l.value and r.type == l.type:
                    res = Sequence.compare(l, r)
                    candidate = candidate and res
                    found = True

                    if res:
                        l.attr['status'] = Seq.copy
                    break

            if not found:
                l.attr['status'] = Seq.remove
                idxt += 1

        left.attr['insert'] = []

        num_same = 0
        for r in right.children:
            found = False
            for l in left.children:
                if r.value == l.value and r.type == l.type:
                    found = True
                    num_same += 1
                    break

            if not found or num_same > len(left.children):
                left.attr['insert'].append(r)

        for l in left.children:
            if l.attr['status'] != Seq.copy:
                left.attr['status'] = Seq.copyandchange
                return False

        if len(left.attr['insert']) > 0:
            left.attr['status'] = Seq.copyandchange
            return False

        left.attr['status'] = Seq.copy
        return True

    @staticmethod
    def generate_sequence(left, right, table_info=None, linear_insert=False):
        if left is None or right is None:
            return []

        Sequence.compare(left, right)

        res = []
        Sequence.generate_sequence_text(left, res, linear_insert)
        return res + []

    @staticmethod
    def node_to_sequence(node):
        def recurse(n, ls):
            if n.value is not None:
                ls.append(n.type.name + '[' + n.value + ']')
            else:
                ls.append(n.type.name)

            for c in n.children:
                recurse(c, ls)

        ls = []
        recurse(node, ls)
        return ls

    @staticmethod
    def generate_sequence_text(node, ls, linear_insert=False):
        if node is None:
            return

        attr = node.attr

        if 'status' not in attr:
            return

        if attr['status'] == Seq.copy or attr['status'] == Seq.remove:
            ls.append(attr['status'].name)
            return

        if len(attr['insert']) == 0:
            ls.append(Seq.copyandchange.name)
        else:
            if linear_insert is False:
                sql_string = Serializer.serialize(attr['insert'][0])
                for i, n in enumerate(attr['insert']):
                    if i != 0:
                        sql_string = sql_string + ',' + Serializer.serialize(n)
                ls.append(Seq.copyandchange.name + '[' + sql_string + ']')
            else:
                sql_string = Unparser.unparse(attr['insert'][0])
                for i, n in enumerate(attr['insert']):
                    if i != 0:
                        sql_string = sql_string + ',' + Unparser.unparse(n)
                ls.append(Seq.copyandchange.name + '[' + sql_string + ']')

        for c in node.children:
            Sequence.generate_sequence_text(c, ls, linear_insert)

    @staticmethod
    def apply_sequence(node, sequence, idx, linear_insert=False):
        if idx >= len(sequence):
            return idx

        if sequence[idx] == Seq.copy.name:
            return idx + 1

        idn = idx
        idx += 1

        for c in node.children:
            if sequence[idx] == Seq.remove.name:
                c.attr['remove'] = True
                idx += 1
            elif sequence[idx] == Seq.copy.name or sequence[idx].startswith(Seq.copyandchange.name):
                idx = Sequence.apply_sequence(c, sequence, idx, linear_insert)

        node.children = list(filter(lambda x: 'remove' not in x.attr, node.children))

        if idn < len(sequence):
            if not sequence[idn] == Seq.copyandchange.name:
                inseq = remove_front_sqbracket(sequence[idn])
                Sequence.apply_insert_sequence(node, inseq, linear_insert)

        return idx

    def apply_insert_sequence(node, inseq, linear_insert=False):
        if len(inseq) == 0:
            return

        content = Serializer.smart_split(inseq, ',')
        for c in content:
            if linear_insert is False:
                node.children.append(Serializer.deserialize(c))
            else:
                tokens = sqlparse.parse(c)[0].tokens

                if linear_insert:
                    Parser.handle(node, tokens, ignore={State.FROM: True})
                else:
                    Parser.handle(node, tokens)

def generate_sequence(left, right, table_info=None, linear_insert=False):
    """Generates a sequence for two trees
    :param left: A TreeNode
    :param right: A TreeNode

    :return: A List of sequence
    """
    left, right = left.clone(), right.clone()
    Sequence.compare(left, right)
    return Sequence.generate_sequence(left, right, table_info, linear_insert)

def generate_sequence_sql(left, right, table_info=None, ignore=None, linear_insert=False):
    left, right = to_tree(left, table_info=table_info, ignore=ignore), to_tree(right, table_info=table_info, ignore=ignore)
    
    return generate_sequence(left, right, table_info, linear_insert)

def apply_sequence(tree, sequence, linear_insert=False):
    Sequence.apply_sequence(tree, sequence, 0, linear_insert)
    return tree

def apply_sequence_sql(sql, sequence, table_info=None, ignore=None, linear_insert=False):
    tree = to_tree(sql, table_info=table_info, ignore=ignore)
    new_tree = apply_sequence(tree, sequence, linear_insert=linear_insert)


    return to_sql(new_tree)

def get_node_from_sequence(tree, sequence):
    """Returns the TreeNode corresponding to the instruction immediately succeeding the sliced sequence
    :param sql: a TreeNode and a sliced sequence

    :return: a TreeNode
    """
    def recurse(node, sequence, idx):
        if node is None or idx >= len(sequence):
            return node, idx

        idx += 1
        new_node = None
        for c in node.children:
            new_node, idx = recurse(c, sequence, idx)
            if new_node is not None:
                break

        return new_node, idx

    return recurse(tree, sequence, 0)[0]
