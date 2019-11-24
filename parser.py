from astnodes import BinaryOperationNode, IntLiteralNode, FloatLiteralNode, IdLiteralNode
from ply.lex import LexToken
from utils import Stack, ParseTreeNode, DerivationLogger


class Parser(object):

    def __init__(self, lexer, grammar):
        self.lexer = lexer
        self.grammar = grammar
        self.grammar.gen_table()
        self.pstack = Stack()       # parsing stack
        self.sstack = Stack()       # semantic stack
        self.has_error = False
        self.deri_logger = DerivationLogger('/Users/ERIC_LAI/Downloads/project/compiler/output/derivation.txt')
        self.cur_token = None
        self.ptree_nodes = set()
        self.astroot = None

    def parse(self):
        self.ptree_root = self.create_ptree_node(self.grammar.start_symbol)
        self.pstack.push(self.create_ptree_node(self.grammar.ending_symbol))
        self.pstack.push(self.ptree_root)

        self.cur_token = self.lexer.token()

        while self.pstack.top().val != self.grammar.ending_symbol:
            self.deri_logger.line(self.pstack)

            top = self.pstack.top().val
            # if top rule is a terminal
            if top in self.grammar.terminals:
                if top == self.cur_token.value:
                    self.pstack.pop()
                    self.cur_token = self.lexer.token()
                    if not self.cur_token:
                        self.cur_token = LexToken()
                        self.cur_token.value = '$'
                else:
                    self.skip_error(top, self.pstack)
                    self.has_error = True

            # if top rule is a nonterminal
            elif top in self.grammar.nonterminals:
                if (top, self.cur_token.value) in self.grammar.table:
                    # expand the nonterminal and insert its rhs to the stack
                    parent_node = self.pstack.pop()
                    prod = self.grammar.table[top, self.cur_token.value].sem_prod

                    # add the rhs into the stack
                    new_nodes = self.inverse_rhs_push(prod)
                    # every time expand a nonterminal, construct the parse tree
                    self.construct_parse_tree(parent_node, new_nodes)
                else:
                    self.skip_error(top, self.pstack)
                    self.has_error = True

            # if it is an action
            elif top[0] == '#':
                action = top[2:]
                self.pstack.pop()
                if action == 'INT':
                    lexeme = self.pstack.top()
                    node = IntLiteralNode(lexeme)
                    self.sstack.push(node)
                elif action == 'FLOAT':
                    lexeme = self.pstack.top()
                    node = FloatLiteralNode(lexeme)
                    self.sstack.push(node)
                elif action == 'ID':
                    lexeme = self.pstack.top()
                    node = IdLiteralNode(lexeme)
                    self.sstack.push(node)
                elif action == 'BI_MUL':
                    node = BinaryOperationNode('*')
                    operand2 = self.sstack.pop()
                    operand1 = self.sstack.pop()
                    node.left_expr = operand1
                    node.right_expr = operand2
                    self.sstack.push(node)
                elif action == 'BI_PLUS':
                    node = BinaryOperationNode('+')
                    operand2 = self.sstack.pop()
                    operand1 = self.sstack.pop()
                    node.left_expr = operand1
                    node.right_expr = operand2
                    self.sstack.push(node)

        if self.cur_token.value != self.grammar.ending_symbol and self.has_error:
            res = False
        else:
            res = True
            self.deri_logger.line(self.pstack)

        # AST root
        self.astroot = self.sstack.pop()
        # release the resources
        self.deri_logger.close()
        return res

    def inverse_rhs_push(self, prod):
        new_nodes = []
        reversed_rhs = reversed(prod.rhs)
        for term in reversed_rhs:
            if term != 'EPSILON':
                n = self.create_ptree_node(term)
                new_nodes.append(n)
                self.pstack.push(n)
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
        node = ParseTreeNode(val)
        self.ptree_nodes.add(node)
        return node


    # ********************************************************************** #

    @staticmethod
    def construct_parse_tree(parent, children):
        for child in reversed(children):
            child.parent = parent
            parent.add_child(child)
