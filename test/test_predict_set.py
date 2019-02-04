import unittest
import predict_set as ps


class Test(unittest.TestCase):

    def test_merge(self):
        # merge set1 to set2, except 'd'
        sset1 = {'a', 'b', 'c', 'd'}
        sset2 = {'e', 'f', 'g', 'h'}
        expected = {'a', 'b', 'c', 'h', 'e', 'f', 'g'}
        actual = ps.merge(sset2, sset1, 'd')
        self.assertSetEqual(expected, actual)


    def test_get_rhs(self):
        rules = {
            'key1': [
                ['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['a', 'b', 'r', 'p']
            ]
        }
        expected = [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['a', 'b', 'r', 'p']]
        ps.rules = rules
        rhs = ps.get_rhs('key1')
        self.assertListEqual(expected, rhs)
        ps.rules = {}

    def test_get_prod_with_rhs(self):
        rules = {
            'key1': [
                ['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['a', 'b', 'r', 'p']
            ]
        }
        expected = {'key1': [['a', 'b', 'c', 'd'], ['a', 'b', 'r', 'p']]}
        ps.rules = rules
        prod = ps.get_prod_with_rhs('a')
        self.assertDictEqual(expected, prod)
        ps.rules = {}

    def test_has_epsilon(self):
        rules = {
            'key1': [
                ['a', 'b', 'EPSILON', 'd'], ['e', 'f', 'g', 'h'], ['a', 'b', 'r', 'p']
            ]
        }
        prods = rules['key1']
        actual = []
        expected = [True, False, False]
        for idx in range(0, 3):
            actual.append(ps.has_epsilon(prods[idx]))
        self.assertListEqual(expected, actual)

    def test_can_derive_empty(self):
        """
        Grammar
        -------
        E           -> T EPrime
        EPrime      -> EPSILON | '+' T EPrime
        T           -> F TPrime
        TPrime      -> EPSILON | '*' F TPrime
        F           -> '(' E ')' | '0' | '1'
        """
        rules = {
            'E': [['T', 'EPrime']],
            'EPrime': [['EPSILON'], ['+', 'T', 'EPrime']],
            'T': [['F', 'TPrime']],
            'TPrime': [['EPSILON'], ['*', 'F', 'TPrime']],
            'F': [['(', 'E', ')'], ['0'], ['1']]
        }
        ps.rules = rules
        acutal1 = ps.can_derive_empty('F', set())
        acutal2 = ps.can_derive_empty('E', set())
        self.assertFalse(acutal1)
        self.assertTrue(acutal2)
