import re


class Production(object):

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.separator = '->'

    def __str__(self):
        return self.lhs + ' ' + self.separator + ' ' + str(self.rhs)

    __repr__ = __str__


class Grammar(object):

    def __init__(self, file_path, start_symbol):
        self.productions  = {}
        self.terminals    = set()
        self.nonterminals = set()
        self.start_symbol = start_symbol
        self.first_sets   = {}
        self.follow_sets  = {}
        self.table        = {}
        self.table_error  = {}

        self.table_error['LL(1)'] = set()
        self._construct(file_path)

    def summary(self):
        print('*******************************')
        print('start symbol: {}'.format(self.start_symbol))
        print('= = = = = = = =')
        print('terminal #{}:'.format(len(self.terminals)))
        print(self.terminals)
        print('= = = = = = = =')
        print('nonterminal #{}:'.format(len(self.nonterminals)))
        print(self.nonterminals)
        print('= = = = = = = =')
        print('productions')
        for key, val in self.productions.items():
            for prod in val:
                print(prod)
        print('*******************************')
        for key, val in self.first_sets.items():
            if key not in self.terminals:
                print('first set of {}, {}'.format(key, val))
        print()
        for key, val in self.follow_sets.items():
            print('follow set of {}, {}'.format(key, val))
        print('*******************************')

    def _construct(self, file_path, debug=False):
        with open(file_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                # split the by the separator '->'
                parts = re.split(r'\s+->\s+', line)
                lhs_ = parts[0]
                rhs_ = parts[1]
                self._add_nonterminal(lhs_)

                # create an new entry for the new nonterminal, it will contains
                # a list of productions leading with that nonterminal
                self.productions[lhs_] = []

                # rhs may contains '|', for example: EPrime -> EPSILON | '+' T EPrime
                prods = re.split(r'\s+\|\s+', rhs_)
                for prod in prods:
                    tmp = re.split(r'\s+', prod)
                    rhs__ = []

                    for term in tmp:
                        if term[0] == "'":
                            tmp_ = term[1:-1]
                            self._add_terminal(tmp_)
                            rhs__.append(tmp_)
                        else:
                            rhs__.append(term)
                    self._create_production(lhs_, rhs__)

        for t in self.terminals:
            self.first_of(t)
        for nt in self.nonterminals:
            self.first_of(nt)
        for t in self.terminals:
            self.follow_of(t)
        for nt in self.nonterminals:
            self.follow_of(nt)

    def _create_production(self, nonterminal, rhs):
        p = Production(nonterminal, rhs)
        self.productions[nonterminal].append(p)

    def _add_nonterminal(self, nonterminal):
        self.nonterminals.add(nonterminal)

    def _add_terminal(self, terminal):
        self.terminals.add(terminal)

    def production_for(selfs, nonterminal):
        return selfs.productions[nonterminal]

    def rhs_occurrences(self, symbol):
        res = []
        for key, prod_list in self.productions.items():
            for prod in prod_list:
                for term in prod.rhs:
                    if term == symbol and prod not in res:
                        res.append(prod)
        return res

    def can_derive_epsilon(self, symbol):
        return self.can_derive_epsilon_(symbol, set())

    def can_derive_epsilon_(self, symbol, visited):
        if symbol in self.nonterminals:
            prods = self.production_for(symbol)
            for p in prods:
                # check if epsilon in current production
                res = self.production_contains_epsilon(p)
                if res:
                    return True
                # check the rhs of current production
                for term in p.rhs:
                    if term in self.nonterminals and term not in visited:
                        visited.add(term)
                        res = self.can_derive_epsilon_(term, visited)
                        if res:
                            return True
        return False

    def first_of(self, symbol):
        if symbol in self.first_sets:
            return self.first_sets[symbol]

        first = self.first_sets[symbol] = set()

        # symbol is a terminal, return itself as first set
        if symbol in self.terminals or symbol == 'EPSILON':
            first.add(symbol)
            return first

        # symbol is a nonterminal
        prods = self.productions[symbol]
        for p in prods:
            for term in p.rhs:
                # if the production start with epsilon
                if term == 'EPSILON':
                    first.add(term)
                    break
                # have to copy, cannot use the set itself since may remove epsilon
                ffirst = self.first_of(term).copy()
                if 'EPSILON' not in ffirst:
                    # if no epsilon, means the first cannot go to next nonterminal
                    # just merge ffirst and first
                    self.merge(first, ffirst)
                    break
                else:
                    # if there is epsilon, need to keep tracking the next nonterminal
                    self.merge(first, ffirst, 'EPSILON')
        self.first_sets[symbol] = first
        return first

    def follow_of(self, symbol):
        if symbol in self.follow_sets:
            return self.follow_sets[symbol]

        follow = self.follow_sets[symbol] = set()

        if symbol == self.start_symbol:
            follow.add('$')

        prods_with_sym = self.rhs_occurrences(symbol)

        for prod in prods_with_sym:
            symbol_idx = prod.rhs.index(symbol)
            follow_idx = symbol_idx + 1

            while True:
                # symbol: B
                # A -> a B
                if follow_idx == len(prod.rhs):
                    if prod.lhs != symbol:
                        self.merge(follow, self.follow_of(prod.lhs))
                    break

                # symbol: B
                # A -> gama B beta
                follow_symbol = prod.rhs[follow_idx]

                first_of_follow = self.first_of(follow_symbol).copy()

                if 'EPSILON' not in first_of_follow:
                    self.merge(follow, first_of_follow)
                    break

                self.merge(follow, first_of_follow, 'EPSILON')
                follow_idx += 1

        self.follow_sets[symbol] = follow
        return follow

    def first_of_prod_rhs(self, prod):
        if len(prod.rhs) == 1 and prod.rhs[0] == 'EPSILON':
            s = set()
            s.add('EPSILON')
            return s

        ffirst = set()
        for term in prod.rhs:
            first = self.first_sets[term]
            if 'EPSILON' not in first:
                return first
            self.merge(ffirst, first, 'EPSILON')
        ffirst.add('EPSILON')
        return ffirst

    def gen_table(self):
        for prod_key in self.productions:
            for prod in self.productions[prod_key]:
                first_set = self.first_of_prod_rhs(prod)
                for term in first_set:
                    if term in self.terminals:
                        self.table_entry_check(prod, term)
                if 'EPSILON' in first_set:
                    follow_set = self.follow_sets[prod.lhs]
                    for term in follow_set:
                        self.table_entry_check(prod, term)
                    if '$' in follow_set:
                        self.table[prod.lhs, '$'] = prod

    def table_entry_check(self, prod, term):
        if (prod.lhs, term) in self.table:
            self.table_error['LL(1)'].add(prod)
        else:
            self.table[prod.lhs, term] = prod

    def is_LL1(self):
        if len(self.table_error['LL(1)']) == 0:
            print('the grammar is LL(1) grammar')
        else:
            print('the grammar is NOT LL(1) grammar')
            print('something wrong with the following productions')
            for p in self.table_error['LL(1)']:
                print(p)

    @staticmethod
    def merge(to, from_, exclude=''):
        for x in from_:
            if x != exclude:
                to.add(x)

    @staticmethod
    def production_contains_epsilon(production):
        rhs_ = production.rhs
        for term in rhs_:
            if term == 'EPSILON':
                return True
        return False
