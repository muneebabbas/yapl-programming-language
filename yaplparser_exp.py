import ply.yacc as yacc
from yapltokens import tokens
from yapl_interpret import*
import sys
start = "yapl"

#==================================================================================
# start symbol mentioning that program consists of statements
#==================================================================================
def p_yapl(p):
	'yapl : statements yapl'
	p[0] = [p[1]] + p[2]

def p_yapl_empty(p):
	'yapl : '
	p[0] = []

def p_statements(p):
	'statements : statement statements'
	p[0] = [p[1]] + p[2]

def p_statements_empty(p):
	'statements : '
	p[0] = [ ]
#==================================================================================
# All definitions for conditional statements
#==================================================================================
def p_statement_if(p):
	'statement : IF expression DO statements END'
	p[0] = ('if', p[2], p[4])

def p_statement_ifelse(p):
	'statement : IF expression DO statements ELSE DO statements END'
	p[0] = ('if-else', p[2], p[4], p[7])

def p_statement_ifelsif(p):
	'statement : IF expression DO statements elsifs END'
	p[0] = ('if-elsif', p[2], p[4], p[5])

def p_statement_ifelsifelse(p):
	'statement : IF expression DO statements elsifs ELSE DO statements END'
	p[0] = ('if-elsif-else', p[2], p[4], p[5], p[8])

def p_elsifs(p):
	'elsifs : elsif elsifs'
	p[0] = [p[1]] + p[2]

def p_elsifs_empty(p):
	'elsifs : '
	p[0] = [ ]

def p_elsif(p):
	'elsif : ELSIF expression DO statements'
	p[0] = ('elsif', p[2], p[4])
#==================================================================================
# Loops
#==================================================================================
def p_while(p):
	'statement : WHILE expression DO statements END'
	p[0] = ('while', p[2], p[4])

def p_ranged_for(p):
	'''statement : FOR IDENTIFIER IN LPAREN loopvar '.' '.' loopvar RPAREN DO statements END'''
	p[0] = ('ranged-for', p[2], p[5], p[8], p[11])

def p_ranged_for_offset(p):
	'''statement : FOR IDENTIFIER IN LPAREN loopvar ',' loopvar '.' '.' loopvar RPAREN DO statements END'''
	p[0] = ('ranged-for-offset', p[2], p[5], p[7], p[10], p[13])

def p_loopavar_num_neg(p):
	'loopvar : MINUS NUMBER'
	p[0] = ('negative', p[2])

def p_loopvar_num(p):
	'loopvar : NUMBER'
	p[0] = ('number', p[1])

def p_loopvar_id(p):
	'loopvar : IDENTIFIER'
	p[0] = ('identifier', p[1])

def p_loop_array(p):
	'statement : FOR IDENTIFIER IN IDENTIFIER DO statements END'
	p[0] = ('loop_array', p[2], p[4], p[6])
#==================================================================================
# Functions
#==================================================================================

def p_function_call(p):
	'''expression : IDENTIFIER LPAREN args RPAREN'''
	p[0] = ('function-call', p[1], p[3])

def p_args(p):
	'''args : literal ',' args'''
	p[0] = [p[1]] + p[3]

def p_args_single(p):
	'args : literal'
	p[0] = [p[1]]

def p_args_empty(p):
	'args : '
	p[0] = []

def p_literal_expression(p):
	'literal : expression'
	p[0] = ('expression', p[1])

def p_literal_id(p):
	'literal : IDENTIFIER'
	p[0] = ('identifier', p[1])

def p_literal_number(p):
	'literal : NUMBER'
	p[0] = ('number', p[1])

def p_literal_string(p):
	'literal : STRING'
	p[0] = ('string', p[1])

def p_function(p):
	'''statement : DEF IDENTIFIER LPAREN params RPAREN MINUS GT DO statements END'''
	p[0] = ('function', p[2], p[4], p[9])
def p_function_empty(p):
	'''statement : DEF IDENTIFIER LPAREN RPAREN MINUS GT DO statements END'''
	p[0] = ('function', p[2], [], p[8])

def p_params_empty(p):
	'params : '
	p[0] = []
def p_params(p):
	'''params : IDENTIFIER ',' params'''
	p[0] = [p[1]] + p[3]
def p_params_single(p):
	'params : IDENTIFIER'
	p[0] = [p[1]]

#==================================================================================
# Arrays
#==================================================================================

def p_array_declaration_range(p):
	'''statement : IDENTIFIER EQUAL LPAREN loopvar '.' '.' loopvar RPAREN'''
	p[0] = ("ranged_array", p[1], p[4], p[7])

def p_array_declaration_ranged(p):
	'''statement : IDENTIFIER EQUAL LPAREN loopvar ',' loopvar '.' '.' loopvar RPAREN'''
	p[0] = ("ranged_array_offset", p[1], p[4], p[6], p[9])

def p_array_declaration(p):
	'''statement : IDENTIFIER EQUAL LSQUARE args RSQUARE'''
	p[0] = ("array_assignment", p[1], p[4])

def p_array_assign(p):
	'statement : IDENTIFIER LSQUARE expression RSQUARE EQUAL expression'
	p[0] = ("array_element_assign", p[1], p[3], p[6])

#==================================================================================
# All definitions for expressions and assignment
#==================================================================================

def p_statement_expression(p):
	'statement : expression'
	p[0] = ("expression", p[1])

def p_statement_assignment(p):
	'statement : IDENTIFIER EQUAL expression'
	p[0] = ('assignment', p[1], p[3])

def p_statement_return(p):
	'statement : RETURN expression'
	p[0] = ('return', p[2])

def p_expression_binop(p):
	'''expression : expression PLUS term
			   	  | expression MINUS term
			      | expression TIMES term
			      | expression ANDAND term
			      | expression NOTEQUAL term
			      | expression EQUALEQUAL term
			      | expression GE term
			      | expression GT term
			      | expression LE term
			      | expression LT term
			      | expression OROR term
			      | expression MOD term'''
	p[0] = ('binop', p[1], p[2], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = ('term', p[1])

def p_function_call(p):
	'''term : IDENTIFIER LPAREN args RPAREN'''
	p[0] = ('function-call', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = ('factor', p[1])

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = ('number', p[1])

def p_factor_negative(p):
	'factor : MINUS NUMBER'
	p[0] = ('negative', p[2])

def p_factor_id(p):
	'factor : IDENTIFIER'
	p[0] = ('identifier', p[1])

def p_factor_array(p):
	'factor : IDENTIFIER LSQUARE expression RSQUARE'
	p[0] = ('array_index', p[1], p[3])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = ('expression', p[2])

def p_factor_true(p):
	'term : TRUE'
	p[0] = ('true', p[1])

def p_factor_false(p):
	'term : FALSE'
	p[0] = ('false', p[1])

def p_expression_id(p):
	'expression : IDENTIFIER'
	p[0] = ('identifier', p[1])

def p_expression_true(p):
	'expression : TRUE'
	p[0] = ('true', p[1])


def p_expression_return(p):
	'expression : RETURN expression'
	p[0] = ('return', p[2])

def p_expression_print(p):
	'expression : PRINT factor'
	p[0] = ('print', p[2])


def p_factor_string(p):
	'factor : STRING'
	p[0] = ('string', p[1])

def p_error(p):
    print("Syntax error in input!")
    print p
    exit(1)

parser = yacc.yacc()
f = open(sys.argv[1], 'r')
code = f.read()
parser = yacc.yacc()
result = parser.parse(code)
parse_tree = result[0]

for statement in parse_tree:
	# print statement
	eval_statement(statement, globalVars)


