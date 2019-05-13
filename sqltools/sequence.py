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
                    candidate = candidate and Sequence.compare(l, r)
                    found = True
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
                candidate = False
                left.attr['insert'].append(r)
        
        if candidate:
            left.attr['status'] = Seq.copy
        else:
            left.attr['status'] = Seq.copyandchange

        return candidate

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

        for c in children:
            if sequence[idx] == Seq.remove.name:
                c.attr['remove'] = True
                idx += 1
            elif sequence[idx] == Seq.copy.name or sequence[idx] == Seq.copyandchange.name:
                idx = Sequence.apply_sequence(c, sequence, idx)

        node.children = list(filter(lambda x: 'remove' in x.attr and x.attr['remove'], node.children))

        permutes = [Seq.copy.name, Seq.remove.name, Seq.copyandchange.name]

        while sequence[idx] not in permutes:
            idx += 1

        return idx

def generate_sequence(left, right):
    left, right = left.clone(), right.clone()
    Sequence.compare(left, right)

    return Sequence.generate_sequence(left, right)

def generate_sequence_sql(left, right):
    left, right = to_tree(left), to_tree(right)
    Sequence.compare(left, right)

    return Sequence.generate_sequence(left, right)

def apply_sequence(sql, sequence):
    tree = Sequence.apply(to_tree(sql), sequence, 0)
    return to_sql(tree)
