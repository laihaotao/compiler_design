class Stack(object):

    def __init__(self):
        self.content = []

    def push(self, obj):
        self.content.append(obj)

    def pop(self):
        return self.content.pop()

    def top(self):
        return self.content[-1]

    def is_empty(self):
        return len(self.content) == 0


class ParseTreeNode(object):

    def __init__(self, val):
        self.val = val
        self.parent = None
        self.children = []

    def __str__(self):
        return self.val

    def add_child(self, child):
        self.children.append(child)

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return len(self.children) == 0

    __repr__ = __str__


class DerivationLogger(object):

    def __init__(self, file_path):
        self.file = open(file_path, 'w')
        self.file.write('**************')
        self.file.write('Derivation Log')
        self.file.write('**************')
        self.file.write('\n')

    def line(self, stack):
        self.file.write(str(stack.content) + '\n')
        self.file.flush()

    def close(self):
        self.file.close()