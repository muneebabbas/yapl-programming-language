import ply.lex as lex

precedence = (
        ('left', 'MINUS'),
        ('left', 'OROR'),
        ('left', 'ANDAND'),
        ('left', 'EQUALEQUAL'),
        ('left', 'LT', 'LE', 'GT', 'GE'),
        ('left', 'PLUS'),
        ('right', 'NOT'),
        ('left', 'TIMES', 'DIVIDE'),
)

reserved = {
	'if': 'IF',
	'elsif': 'ELSIF',
	'while': 'WHILE',
	'do': 'DO',
	'end': 'END',
	'return': 'RETURN',
	'true': 'TRUE',
	'false': 'FALSE',
	'else' : 'ELSE',
    'print' : 'PRINT',
    'for' : 'FOR',
    'in' : 'IN',
    'def' : 'DEF'
}

tokens = [
        'ANDAND',       # &&
        'EQUAL',        # =
        'EQUALEQUAL',   # ==
        'GE',           # >=
        'GT',           # >
        'LE',           # <=
        'LPAREN',       # (
        'LT',           # <
        'MINUS',        # -
        'NOT',          # !
        'NUMBER',       #### Not used in this problem.
        'OROR',         # ||
        'PLUS',         # +
        'RPAREN',       # )
        'TIMES',        # *
        'STRING',
        'IDENTIFIER',    # variable names
        'NOTEQUAL',
        'MOD',
        'DIVIDE',
        'LSQUARE',
        'RSQUARE',
]

literals = [',', '.', '[', ']']

tokens += list(reserved.values())
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_DIVIDE = r'/'
t_ANDAND =  r'&&'
t_EQUALEQUAL = r'=='
t_EQUAL = r'='
t_GE =  r'>='
t_GT =   r'>'
t_LE =  r'<='
t_LPAREN =   r'\('
t_LT = r'<'
t_NOT = r'!'
t_OROR = r'\|\|'
t_PLUS = r'\+'
t_RPAREN =  r'\)'
t_TIMES = r'\*'
t_NOTEQUAL = r'!='
t_ignore                = ' \t\v\r' # shortcut for whitespace

states = (
        ('yaplcomment','exclusive'),
)

def t_yaplcomment(t):
    r'\#'
    t.lexer.begin('yaplcomment')

def t_yaplcomment_end(t):
    r'\n'
    t.lexer.begin('INITIAL')

t_yaplcomment_ignore = r'.'

def t_yaplcomment_error(t):
    t.lexer.skip(1)

def t_MOD(t):
    r'mod'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

def t_NUMBER(token):
        r'[0-9]+(?:\.[0-9]+)?'
        token.value = float(token.value)
        return token

def t_MINUS(token):
    r'-'
    return token

def t_STRING(t):
        r'"[^"]*"'
        t.value = t.value[1:-1] # drop "surrounding quotes"
        return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()
# f = open('code.in', 'r')
# code = f.read()
# lexer.input(code)
# while True:
#         tok = lexer.token()
#         if not tok: break
#         print tok

