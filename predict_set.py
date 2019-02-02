import re
import sys


# two sets contains all terminal and nontermian respectively
terminals     = set()
non_terminals = set()

# the collection of rule
#  key[string]: the left hand side of the production
#  value[list of string]: the right hand side of the prodcution
rules = {}

first_sets  = {}
follow_sets = {}


def split_production(production_str):
    prods = re.split(r'\s+\|\s+', production_str)
    prods_ = []
    for s in prods:
        val_arr = re.split(r'\s+', s)
        tmp = []
        for v in val_arr:
            if v[0] == "'":
                t = v[1:-1]
                terminals.add(t)
                v = t
            else:
                non_terminals.add(v)
            tmp.append(v)
        prods_.append(tmp)
    return prods_


def construct(file_path, start_symbol, debug=False):
    global START_SYMBOL
    START_SYMBOL = start_symbol
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            # if the first char is '|'
            if line[0] == '|':
                production_str = line[1:].strip()
                split_production(production_str)                
                
            # if it is a new line of rule
            else:
                parts = re.split(r'\s+\->\s+', line)
                key = parts[0]
                non_terminals.add(key)
                
                production_str = parts[1]
                prods = split_production(production_str)
                rules[key] = list(prods)
    # remove EPSILON from the nonterminal
    non_terminals.remove('EPSILON')

    print('total number of rule: {}'.format(str(len(rules))))
    print('total number of nonterminal: {}'.format(str(len(non_terminals))))
    print('total number of terminal: {}'.format(str(len(terminals))))

    if debug:
        print('rules:\n {} \n'.format(rules))
        print('nonterminals:\n {} \n'.format(non_terminals))
        print('terminals:\n {} \n'.format(terminals))


# reference: https://gist.github.com/DmitrySoshnikov/924ceefb1784b30c5ca6
def first_of(symbol):
    # if already built
    if symbol in first_sets:
        return first_sets[symbol]
    
    # if not build yet, create an new entry
    first = first_sets[symbol] = set()
    
    # if it is a terminal, then the first set just itself
    if symbol in terminals or symbol == 'EPSILON':
        first_sets[symbol].add(symbol)
        return first_sets[symbol]
    
    # if it is not a terminal
    #   1. it may be a nonterminal
    #   2. it may contains EPSILON
    prods = rules[symbol]
    for p in prods:
        for prod_symbol in p:
            # if there is epsilon is one of the production
            if prod_symbol == 'EPSILON':
                first.add('EPSILON')
                break
            # if there is no epsilon, don't need to check follow set
            first_of_nonterminal = first_of(prod_symbol)
            if 'EPSILON' not in first_of_nonterminal:
                first = first.union(first_of_nonterminal)
                break
            
            # if we have epsilon in the first nonterminal
            first_of_nonterminal.add('EPSILON')
            first = first.union(first_of_nonterminal)
    first_sets[symbol] = first
    return first


def get_prod_with_rhs(symbol):
    prods = {}
    for lhs, rhs in rules.items():
        for production in rhs:
            for term in production:
                if term == symbol and term not in prods:
                    prods[lhs] = list(production)
                elif term == symbol and term in prods:
                    prods[lhs].append(production)
    return prods


def follow_of(symbol):
    # if already built
    if symbol in follow_sets:
        return follow_sets[symbol]

    follow = follow_sets[symbol] = set()
    if symbol == START_SYMBOL:
        follow_sets[symbol].add('$')
    
    prods_with_sym = get_prod_with_rhs(symbol)
    for key, prods in prods_with_sym.items():
        symbol_idx = prods.index(symbol)
        follow_idx = symbol_idx + 1

        while True:
            if follow_idx == len(prods):
                if key != symbol:
                    follow = follow.union(follow_of(key))
                break
        
            follow_symbol = prods[follow_idx]
            first_of_follow = first_of(follow_symbol)

            if  'EPSILON' not in first_of_follow:
                follow = follow.union(first_of_follow)
                break
            
            # first_of_follow.add('EPSILON')
            follow = follow.union(first_of_follow)
            follow.remove('EPSILON')
            follow_idx += 1

    follow_sets[symbol] = follow
    return follow

if __name__ == "__main__":
    # file_path = './working_grammar.txt'
    # construct(file_path, 'S', debug=True)

    file_path = './simple_grammar.txt'
    construct(file_path, 'E', debug=False)
    
    for n in non_terminals:
        s = first_of(n)
        print('first set of {}: {}'.format(n, s))
        
    for n in non_terminals:
        f = follow_of(n)
        print('follow set of {}: {}'.format(n, f))

