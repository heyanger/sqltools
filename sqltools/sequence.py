from sqltools.parser import *
from sqltools.serializer import *

class Sequence:
    @staticmethod
    def compare(left, right):
        if left.value != right.value or left.type != right.type:
            left.attr['status'] = Seq.remove
            return False

        candidate = True

        for l in left.children:            
            found = False
            for r in right.children:
                if r.value == l.value and r.type == l.type:
                    res = Sequence.compare(l, r)
                    candidate = candidate and res
                    found = True 

                    if res:
                        l.attr['status'] = Seq.copy
                    break

            if not found:
                l.attr['status'] = Seq.remove

        left.attr['insert'] = []

        for r in right.children:
            found = False
            for l in left.children:       
                if r.value == l.value and r.type == l.type:
                    found = True
                    break

            if not found:
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
    def generate_sequence(left, right):
        if left is None or right is None:
            return []

        Sequence.compare(left, right)

        res = []
        Sequence.generate_sequence_text(left, res)
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
    def generate_sequence_text(node, ls):
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
            sql_string = Serializer.serialize(attr['insert'][0])
            ls.append(Seq.copyandchange.name + '[' + sql_string + ']')

        for c in node.children:
            Sequence.generate_sequence_text(c, ls)

    @staticmethod
    def apply_sequence(node, sequence, idx):
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
                idx = Sequence.apply_sequence(c, sequence, idx)

        node.children = list(filter(lambda x: 'remove' not in x.attr, node.children))

        if idn < len(sequence):
            if not sequence[idn] == Seq.copyandchange.name:
                inseq = remove_front_sqbracket(sequence[idn])
                Sequence.apply_insert_sequence(node, inseq)

        return idx

    def apply_insert_sequence(node, inseq):
        if len(inseq) == 0:
            return

        node.children.append(Serializer.deserialize(inseq))

def generate_sequence(left, right):
    left, right = left.clone(), right.clone()
    Sequence.compare(left, right)

    return Sequence.generate_sequence(left, right)

def generate_sequence_sql(left, right, table_info=None):
    left, right = to_tree(left, table_info), to_tree(right, table_info)
    Sequence.compare(left, right)

    # tree_print(left, highlights=['status', 'insert'])

    seq = Sequence.generate_sequence(left, right)
    return seq

def apply_sequence(tree, sequence):
    Sequence.apply_sequence(tree, sequence, 0)
    return tree

def apply_sequence_sql(sql, sequence, table_info=None):
    tree = to_tree(sql, table_info)
    new_tree = apply_sequence(tree, sequence)
    return to_sql(new_tree)

def get_sequence_nodes(tree, sequence):
    """Returns a list of TreeNodes where each element in the list corresponds to the TreeNode
    where the sequence is applied
    :param sql: a TreeNode

    :return: List of TreeNode
    """
    return []
