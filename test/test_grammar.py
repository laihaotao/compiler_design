import unittest
import grammar as tst


"""
Grammar For Testing
-------------------

E -> T X
T -> ( E ) | int Y
X -> + E | ϵ
Y -> * T | ϵ
"""


class TestGrammar(unittest.TestCase):

    def test_gen_table1(self):
        file = '../grammar/simple_grammar3.txt'
        grammar = tst.Grammar(file, 'E')
        grammar.gen_table()

    def test_gen_table2(self):
        file = '../grammar/simple_grammar1.txt'
        grammar = tst.Grammar(file, 'E')
        grammar.gen_table()
        pass

    def test_first_set(self):
        file = '../grammar/simple_grammar3.txt'
        grammar = tst.Grammar(file, 'E')
        expected = {
            'T': {'int', '('},
            'E': {'int', '('},
            'X': {'EPSILON', '+'},
            'Y': {'EPSILON', '*'},
            'int': {'int'},
            '(': {'('},
            ')': {')'},
            '+': {'+'},
            '*': {'*'}
        }
        self.assertDictEqual(expected, grammar.first_sets)
        # for nt in grammar.nonterminals:
        #     print('first set of {}: {}'.format(nt, grammar.first_sets[nt]))

    def test_follow_set(self):
        file = '../grammar/simple_grammar3.txt'
        grammar = tst.Grammar(file, 'E')
        expected = {
            'T': {'$', ')', '+'},
            'E': {'$', ')'},
            'X': {'$', ')'},
            'Y': {'$', ')', '+'},
            '*': {'int', '('},
            'int': {'*', '$', ')', '+'},
            ')': {'$', ')', '+'},
            '(': {'int', '('},
            '+': {'int', '('}
        }
        self.assertDictEqual(expected, grammar.follow_sets)
        # for t in grammar.terminals:
        #     print('follow set of {}: {}'.format(t, grammar.follow_sets[t]))
        # for nt in grammar.nonterminals:
        #     print('follow set of {}: {}'.format(nt, grammar.follow_sets[nt]))
