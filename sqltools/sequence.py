from sqltools.parser import *

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
        
        ls.append(Seq.copyandchange.name)   

        for c in node.children:
            Sequence.generate_sequence_text(c, ls)

        if 'insert' in attr:
            for i in attr['insert']:
                ls.extend(Sequence.node_to_sequence(i))

    @staticmethod
    def apply_sequence(node, sequence, idx):
        if idx >= len(sequence):
            return idx

        if sequence[idx] == Seq.copy.name:
            return idx + 1
        
        idx += 1

        for c in node.children:
            if sequence[idx] == Seq.remove.name:
                c.attr['remove'] = True
                idx += 1
            elif sequence[idx] == Seq.copy.name or sequence[idx] == Seq.copyandchange.name:
                idx = Sequence.apply_sequence(c, sequence, idx)

        node.children = list(filter(lambda x: 'remove' not in x.attr, node.children))

        permutes = [Seq.copy.name, Seq.remove.name, Seq.copyandchange.name]

        while idx < len(sequence) and sequence[idx] not in permutes:
            if '[' in sequence[idx]:
                if sequence[idx][:3] == 'COL':
                    col = remove_front_sqbracket(sequence[idx])
                    n = TreeNode(State.COL, value=col)
                    node.children.append(n)
                else:
                    col = remove_front_sqbracket(sequence[idx])
                    n = TreeNode(State.AGG, value=col)
                    node.children.append(n)
            else:
                break
            idx += 1

        new_sequence = []
        while idx < len(sequence) and sequence[idx] not in permutes:
            new_sequence.append(sequence[idx])
            idx += 1

        Sequence.insert_np_sequence(node, new_sequence)

        return idx

    def insert_np_sequence(node, sequence):
        if len(sequence) == 0:
            return

        seq = ' '.join(remove_front_sqbracket(s) for s in sequence)
        token = sqlparse.parse(seq)[0]
        Parser.handle(node, token)

def generate_sequence(left, right):
    left, right = left.clone(), right.clone()
    Sequence.compare(left, right)

    return Sequence.generate_sequence(left, right)

def generate_sequence_sql(left, right):
    left, right = to_tree(left), to_tree(right)
    Sequence.compare(left, right)

    seq = Sequence.generate_sequence(left, right)
    return seq

def apply_sequence(tree, sequence):
    Sequence.apply_sequence(tree, sequence, 0)
    return tree

def apply_sequence_sql(sql, sequence):
    tree = to_tree(sql)
    new_tree = apply_sequence(tree, sequence)
    return to_sql(new_tree)