import ast


class Node(object):

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


class Stack(object):

    def __init__(self):
        self.content = []

    def push(self, obj):
        self.content.append(obj)

    def pop(self):
        return self.content.pop()

    def top(self):
        return self.content[-1]


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


class Parser(object):

    def __init__(self, lexer, grammar):
        self.lexer = lexer
        self.grammar = grammar
        self.stack = Stack()
        self.has_error = False
        self.deri_logger = DerivationLogger('/Users/ERIC_LAI/Downloads/project/compiler/output/derivation.txt')
        self.cur_token = None
        self.tree = ast.AST()
        self.ptree_nodes = set()

    def parse(self):
        self.ptree_root = self.create_ptree_node(self.grammar.start_symbol)
        self.stack.push(self.create_ptree_node(self.grammar.ending_symbol))
        self.stack.push(self.ptree_root)

        self.cur_token = self.lexer.token()

        while self.stack.top() != self.grammar.ending_symbol:
            self.deri_logger.line(self.stack)

            top = self.stack.top().val
            # if top rule is a terminal
            if top in self.grammar.terminals:
                if top == self.cur_token.value:
                    self.stack.pop()
                    self.cur_token = self.lexer.token()
                    if not self.cur_token: break
                else:
                    self.skip_error(top, self.stack)
                    self.has_error = True

            # if top rule is a nonterminal
            else:
                if (top, self.cur_token.value) in self.grammar.table:
                    # expand the nonterminal and insert its rhs to the stack
                    parent_node = self.stack.pop()
                    prod = self.grammar.table[top, self.cur_token.value]
                    new_nodes = self.inverse_rhs_push(prod)

                    # every time expand a nonterminal, construct the parse tree
                    self.construct_parse_tree(parent_node, new_nodes)

                    # if the production associate with a semantic action
                    if prod.action is not None:

                        pass
                else:
                    self.skip_error(top, self.stack)
                    self.has_error = True

        # release the resources
        self.deri_logger.close()

        if self.cur_token != self.grammar.ending_symbol and self.has_error:
            return False
        else:
            return True

    def inverse_rhs_push(self, prod):
        new_nodes = []
        reversed_rhs = reversed(prod.rhs)
        for term in reversed_rhs:
            if term != 'EPSILON':
                n = self.create_ptree_node(term)
                new_nodes.append(n)
                self.stack.push(n)
        return new_nodes

    def skip_error(self, x, stack):
        print('syntax error at: {}'.format(self.cur_token.lineno))
        lookahead = self.cur_token.value
        if lookahead == '$' or lookahead in self.grammar.follow_sets[x]:
            stack.pop()
        else:
            while (
                    lookahead not in self.grammar.follow_sets[x]
                    or ('EPSILON' in self.grammar.first_sets[x]
                        and lookahead not in self.grammar.follow_sets[x])
            ):
                self.cur_token = self.lexer.token()
                if not self.cur_token:
                    return

    def create_ptree_node(self, val):
        node = Node(val)
        self.ptree_nodes.add(node)
        return node

    @staticmethod
    def construct_parse_tree(parent, children):
        for child in reversed(children):
            child.parent = parent
            parent.add_child(child)
