import copy

class TreeNode:
    def __init__(self, t, value = None):
        self.type = t
        self.children = []
        self.value = value
        
        self.attr = {}

    def clone(self):
        new_node = TreeNode(self.type, value = self.value)
        new_node.attr = copy.deepcopy(self.attr)

        for c in self.children:
            new_node.children.append(c.clone())
        
        return new_node

    def num_child(self):
        return len(self.children)
