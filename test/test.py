import lexer as scanner
import grammar as gr
import parser as pr
import visualizer as vl

grammar_file = '../grammar/simple_grammar1_with_action11.txt'
start_symbol = 'E'
lexer_input  = '0 + 1 * 2'

# start_symbol = 'S'
# lexer_input  = '0 + 1'

lexer = scanner.get_lexer()
lexer.input(lexer_input)
grammar = gr.Grammar(grammar_file, start_symbol)
parser = pr.Parser(lexer, grammar)
# parser.parse()
print('parsing result: ' + str(parser.parse()))

# tree_vl = vl.TreeVisualizer(parser.ptree_root, parser.ptree_nodes,'../output/parse_tree')
# tree_vl.draw()
