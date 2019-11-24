import ply.lex as lex
import lex_rules
import sys
import os


keywords_set    = set(lex_rules.reserved.values())
operators_set   = set(lex_rules.operators_)
punctuation_set = set(lex_rules.punctuation_)

def get_lexer():
    return lex.lex(module=lex_rules)

if __name__=='__main__':
    args = sys.argv
    args_len = len(args)
    if args_len == 1:   
        data = '''
            // comment
            /* comment */
            /* 
            comment 
            */
            hello if else ifthen
            123 023 0.123 00.123
        '''
    elif args_len == 2:
        input_path = args[1]
        input_path = os.path.expanduser(os.path.expanduser(input_path))
        with open(input_path) as f:
            data = f.read()
    else:
        print('too many arguments.')
        exit()

    lexer = lex.lex(module=lex_rules)
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

