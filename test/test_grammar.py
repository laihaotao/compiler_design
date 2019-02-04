import unittest
import grammar as tst


"""
E -> T X
T -> ( E ) | int Y
X -> + E | ϵ
Y -> * T | ϵ

*******************************
first set of E, {'(', 'int'}
first set of T, {'(', 'int'}
first set of X, {'+', 'EPSILON'}
first set of Y, {'*', 'EPSILON'}

follow set of E, {'$', ')'}
follow set of X, {'$', ')'}
follow set of T, {'+', '$', ')'}
follow set of Y, {'+', '$', ')'}
*******************************
"""


class TestGrammar(unittest.TestCase):

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
            'Y': {'$', ')', '+'}
        }
        self.assertDictEqual(expected, grammar.follow_sets)
        # for nt in grammar.nonterminals:
        #     print('follow set of {}: {}'.format(nt, grammar.follow_sets[nt]))
