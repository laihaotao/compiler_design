# -*- coding: utf-8 -*-

# This file only used for the language rule definition respect
# to the given language specification

from ply.lex import TOKEN

reserved = {
    'if'      : 'IF',
    'then'    : 'THEN',
    'else'    : 'ELSE',
    'for'     : 'FOR',
    'class'   : 'CLASS',
    'integer' : 'INTEGER',
    'float'   : 'FLOAT',
    'read'    : 'READ',
    'write'   : 'WRITE',
    'return'  : 'RETURN',
    'main'    : 'MAIN'
}

tokens = (
    'ID', 'FLOAT_VAL', 'INT_VAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LP', 'RP', 'LB', 'RB', 'LSB', 'RSB',
    'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE',
    'AND', 'OR', 'NOT',
    'DOT', 'COLON', 'SEMICOL', 'SCOPE', 'COMMA',
    'ASG'
) + tuple(reserved.values())

t_EQ      = r'=='
t_NEQ     = r'<>'
t_LE      = r'<='
t_GE      = r'>='
t_SCOPE   = r'::'
t_AND     = r'&&'
t_OR      = r'\|\|'
t_LT      = r'<'
t_GT      = r'>'
t_NOT     = r'!'
t_ASG     = r'='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_COMMA   = r','
t_SEMICOL = r';'
t_COLON   = r':'
t_LB  = r'{'
t_RB  = r'}'
t_LSB = r'\['
t_RSB = r'\]'
t_LP  = r'\('
t_RP  = r'\)'
t_DOT = r'\.'


'''
Language Specification
----------------------

id       ::= letter alphanum*
alphanum ::= letter | digit | _
integer  ::= nonzero digit* | 0
float    ::= integer fraction [e[+|−] integer]
fraction ::= .digit* nonzero | .0
letter   ::= a..z |A..Z
digit    ::= 0..9
nonzero  ::= 1..9
'''

_reg_nonzero  = r'([1-9])'
_reg_digit    = r'([0-9])'
_reg_letter   = r'([a-z] | [A-Z])'
_reg_fraction = r'(\.' + _reg_digit + r'*' + _reg_nonzero + r'|\.0)'
_reg_integer  = r'(' + _reg_nonzero + _reg_digit + r'*' + r'|0)'
_reg_flt_op   = r'(e(\+|-)?' + _reg_integer + r')'
_reg_float    = r'(' + _reg_integer + _reg_fraction +  _reg_flt_op + r'?)'
_reg_alphanum = r'(' + _reg_letter + r'|' + _reg_digit + r'|' + r'_)'
_reg_id = r'(' + _reg_letter + _reg_alphanum + r'*)'

t_INT_VAL = _reg_integer
t_FLOAT_VAL = _reg_float

t_ignore  = ' \t'

def t_COMMENT(t):
    r'//.*|/\*(.|[\r\n])*?\*/'
    pass

@TOKEN(_reg_id)
def t_ID(t):
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '{}', at line: {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
