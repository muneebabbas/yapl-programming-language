 # This function will handle all the expressions
import random
import sys
globalVars = (None, {})
functions = {}
def eval_exp(p, variables):
	nodetype = p[0]

	if nodetype == "expression":
		return eval_exp(p[1], variables)

	elif nodetype == 'true':
		return True

	elif nodetype == 'false':
		return False
		
	elif nodetype == "string":
		return p[1]

	elif nodetype == "array_index":
		arr = get(p[1], variables)
		arr_ind = int(eval_exp(p[2], variables))
		return arr[arr_ind-1]

	elif nodetype == "factor":
		return eval_exp(p[1], variables)
	elif nodetype == "term":
		return eval_exp(p[1], variables)

	elif nodetype == "number":
		num = float(p[1])
		if (round(num) == num):
			return int(num)
		else:
			return num

	elif nodetype == "negative":
		return -float(p[1])

	elif (nodetype == "string"):
		return p[1]

	elif nodetype == "paren":
		return eval_exp(p[1], variables)

	elif nodetype == "identifier":
		val = get(p[1], variables)
		if val != None:
			return val
		else:
			raise NameError('Error: Name ' + p[1] + ' is not defined')

	elif nodetype == "print":
		val = eval_exp(p[1], variables)
		print val

	elif nodetype == "function-call":
		if p[1] == "input_int":
			args = p[2]
			val = raw_input(eval_exp(args[0], variables))
			return int(val)
		elif p[1] == "input_string":
			args = p[2]
			val = raw_input(eval_exp(args[0], variables))
			return val

		elif p[1] == "randint":
			args = p[2]
			if (len(args) != 2):
				raise "Error: randint must be called with two integers"
			range_start = eval_exp(args[0], variables)
			range_end = eval_exp(args[1], variables)
			return random.randint(range_start, range_end)

		elif p[1] == "print_raw":
			args = p[2]
			string = ""
			for arg in args:
				string = string + str(eval_exp(arg, variables))
			print string
			return None


		argsNum = len(p[2])
		funcName = p[1] + '-' + str(argsNum)
		if funcName not in functions:
			print "No matching definition for %s found" % funcName
			exit(-1)
		function = functions[funcName]
		if argsNum != function[1]:
			print "Error: %s takes exactly %d arguments (%d given)" % (funcName, function[1], argsNum)
			exit(-1)
		stack = {}
		params = function[2]
		args = p[2]
		for i in range(0, argsNum):
			var = params[i]
			val = getVal(args[i], variables)
			stack[var] = val

		for statement in function[3]:
			if (statement[0] == 'return'):
				retval = eval_exp(statement[1], (globalVars, stack))
				return retval
			retval = eval_statement(statement, (globalVars, stack))
			if (retval != None):
				return retval

	elif nodetype == "binop":
		left_child = p[1]
		operator = p[2]
		right_child = p[3]
		left_val = eval_exp(left_child, variables)
		right_val = eval_exp(right_child, variables)

		if operator == "+":
			return left_val + right_val
		elif operator == "-":
			return left_val - right_val 
		elif operator == "*":
			return left_val * right_val
		elif operator == "/":
			return left_val/right_val
		elif operator == "!=":
			return left_val != right_val
		elif operator == "==":
			return left_val == right_val
		elif operator == "&&":
			return left_val and right_val
		elif operator == "||":
			return left_val or right_val
		elif operator == "<":
			return left_val < right_val
		elif operator == ">":
			return left_val > right_val
		elif operator == "<=":
			return left_val <= right_val
		elif operator == ">=":
			return left_val >= right_val
		elif operator == "mod":
			return left_val % right_val

def get(var, variables):
	if (variables == None):
		return None
	dictionary = variables[1]
	if var in dictionary:
		return dictionary[var]
	else:
		return get(var, variables[0])

def set(var, val, variables):
	variables[1][var] = val

# ************************************************************************************************
#  START of evaluate function
# ************************************************************************************************

# Function to evaluate statements. If a statement returns a value other than a None
#  that value is returned, also if a statement has another substatement that is of type
# 'return', the expression that follows is returned. This forms a nice chains of returns
# that has the effect of returning correct values from functions in situations where the
# return is nested deeply in any number of while's if's or for's

def eval_statement(p, variables):
	nodetype = p[0]
#==========================================================================================
# Interpreting If statements
#==========================================================================================

	if nodetype == "if":
		cond = eval_exp(p[1], variables)
		if cond is not True and cond is not False:
			raise TypeError('Expected a conditional expression')
		if cond is True:
			for statement in p[2]:
				if statement[0] == "return":
					return eval_exp(statement[1], variables)				
				retval = eval_statement(statement, variables)
				if (retval != None):
					return retval
#==========================================================================================
# Interpreting If Else statements
#==========================================================================================

	elif nodetype == "if-else":
		cond = eval_exp(p[1], variables)
		statements = p[2] if cond else p[3]
		for statement in statements:
			if statement[0] == "return":
				return eval_exp(statement[1], variables)
			retval = eval_statement(statement, variables)
			if (retval != None):
				return retval
#==========================================================================================
# Interpreting if-elsif-else statements
#==========================================================================================

	elif nodetype == "if-elsif-else":
		cond = eval_exp(p[1], variables)
		if cond is not True and cond is not False:
			raise TypeError('Expected a conditional expression')
		if cond is True:
			for statement in p[2]:
				if statement[0] == "return":
					return eval_exp(statement[1], variables)				
				retval = eval_statement(statement, variables)
				if (retval != None):
					return retval
		else:
			for elsifs in p[3]:
				elsif_cond = eval_exp(elsifs[1], variables)
				if elsif_cond is True:
					for statement in elsifs[2]:
						if statement[0] == "return":
							return eval_exp(statement[1], variables)					
						retval = eval_statement(statement, variables)
						if (retval != None):
							return retval
					return
			for statement in p[4]:
				if statement[0] == "return":
					return eval_exp(statement[1], variables)				
				retval = eval_statement(statement, variables)
				if (retval != None):
					return retval


#==========================================================================================
# Interpreting if-elsif statements
#==========================================================================================

	elif nodetype == "if-elsif":
		cond = eval_exp(p[1], variables)
		if cond is not True and cond is not False:
			raise TypeError('Expected a conditional expression')
		if cond is True:
			for statement in p[2]:
				if statement[0] == "return":
					return eval_exp(statement[1], variables)				
				retval = eval_statement(statement, variables)
				if (retval != None):
					return retval
		else:
			for elsifs in p[3]:
				elsif_cond = eval_exp(elsifs[1], variables)
				if elsif_cond is True:
					for statement in elsifs[2]:
						if statement[0] == "return":
							return eval_exp(statement[1], variables)					
						retval = eval_statement(statement, variables)
						if (retval != None):
							return retval
#==========================================================================================
# Assignment and Expression
#==========================================================================================
	elif nodetype == "assignment":
		val = eval_exp(p[2], variables)
		set(p[1], val, variables)

	elif nodetype == 'expression':
		eval_exp(p[1], variables)

	elif nodetype == "paren":
		return eval_exp(p[1], variables)
#==========================================================================================
# While loops
#==========================================================================================
	elif nodetype == "while":
		while eval_exp(p[1], variables) is True:
			for statement in p[2]:
				if statement[0] == "return":
					return eval_exp(statement[1], variables)				
				retval = eval_statement(statement, variables)
				if (retval != None):
					return retval
#==========================================================================================
# Ranged for loops with default increment of 1
#==========================================================================================
	elif nodetype == "ranged-for":
		loopVar = eval_exp(p[2], variables)
		loopLimit = eval_exp(p[3], variables)
		set(p[1], loopVar, variables)
		while (loopVar <= loopLimit):
			for statement in p[4]:
				if statement[0] == "return":
					return eval_exp(statement[1], variables)				
				retval = eval_statement(statement, variables)
				if (retval != None):
					return retval
			loopVar += 1
			set(p[1], loopVar, variables)
#==========================================================================================
# Ranged for loops where an offset is given
#==========================================================================================
	elif nodetype == "ranged-for-offset":
		loopVar = eval_exp(p[2], variables)
		loopInc = eval_exp(p[3], variables)
		loopLimit = eval_exp(p[4], variables)
		set(p[1], loopVar, variables)
		offset = loopInc - loopVar
		if (offset > 0):
			while(loopVar <= loopLimit):
				for statement in p[5]:
					retval = eval_statement(statement, variables)
					if (retval != None):
						return retval
				loopVar += offset
				set(p[1], loopVar, variables)
		elif(offset < 0):
			while(loopVar >= loopLimit):
				for statement in p[5]:
					retval = eval_statement(statement, variables)
					if retval != None:
						return retval
				loopVar += offset
				set(p[1], loopVar, variables)
		else:
			print "Warning, Loop variable not changing"
			exit(-1)
#==========================================================================================
# A function definition is saved in a special function map
#==========================================================================================
	elif nodetype == "function":
		argsNum = len(p[2])
		funcName = p[1] + '-' + str(argsNum)
		if funcName in functions:
			print "Redefinition of function not allowed"
			exit(-1)
		functions[funcName] = (funcName, argsNum, p[2], p[3])

#==========================================================================================
# Array assignment
#==========================================================================================
	elif nodetype == "array_assignment":
		val = []
		for item in p[2]:
			val.append(eval_exp(item, variables))
		set(p[1], val, variables)

#==========================================================================================
#  ranged array
#==========================================================================================
	elif nodetype == "ranged_array":
		val = []
		loopVar = eval_exp(p[2], variables)
		loopLimit = eval_exp(p[3], variables)
		while (loopVar <= loopLimit):
			val.append(loopVar)
			loopVar += 1
		set(p[1], val, variables)
#==========================================================================================
# ranged arrays with offset
#==========================================================================================
	elif nodetype == "ranged_array_offset":
		val = []
		loopVar = eval_exp(p[2], variables)
		loopInc = eval_exp(p[3], variables)
		loopLimit = eval_exp(p[4], variables)
		offset = loopInc - loopVar
		if (offset > 0):
			while(loopVar <= loopLimit):
				val.append(loopVar)
				loopVar += offset
		elif(offset < 0):
			while(loopVar >= loopLimit):
				val.append(loopVar)
				loopVar += offset
		else:
			print "Warning, infinite array, variable not changing"
			exit(-1)
		set(p[1], val, variables)
#==========================================================================================
# for loops over arrays
#==========================================================================================
	elif nodetype == "loop_array":
		loopVar = p[1];
		array = get(p[2], variables)
		if type(array) is list:
			for elem in array:
				set(loopVar, elem, variables)
				for statement in p[3]:
					retval = eval_statement(statement, variables)
					if retval != None:
						return retval
		else:
			print "Error: iterating over a non iteratable"
			exit(-1)

#==========================================================================================
# accessing and changing elements of the array
#==========================================================================================
	elif nodetype == "array_element_assign":
		array = get(p[1], variables)
		if array == None:
			print "Error: accessing an array which does not exist"
			exit(-1)
		index = int(eval_exp(p[2], variables))
		val = eval_exp(p[3], variables)
		array[index-1] = val

# ************************************************************************************************
#  END of Evaluate function
# ************************************************************************************************

def getVal(argument, variables):
	argtype = argument[0]
	if argtype == "number" or argtype == "string":
		return argument[1]
	elif argtype == "identifier":
		return get(argument[1], variables)
	elif argtype == "expression":
		val = eval_exp(argument[1], variables)
		return val
	else:
		return eval_exp(argument[1], variables)