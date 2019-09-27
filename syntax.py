# CS3210 - Principles of Programming Languages - Fall 2019
# A Syntax Analyzer for an expression

import sys
import lex

def loadGrammar(input_):
    """reads the given input,
       returns the grammar as a list of productions"""
    grammar = []
    for line in input_:
        grammar.append(line.strip())
    return grammar


def getLHS(production):
    '''returns the LHS (left hand side) of a given production'''
    return production.split("->")[0].strip()


def getRHS(production):
    '''returns the RHS (right hand side) of a given production'''
    return production.split("->")[1].strip().split(" ")


def printGrammar(grammar):
    '''prints the productions of a given grammar - one per line'''
    for production in grammar:
        print(getLHS(production), end=" -> ")
        print(getRHS(production))


def loadTable(input_):
    """reads the given input containing an SLR parsing table,
       returns the "actions" and "gotos" as dictionaries"""
    actions = {}
    gotos = {}
    header = input_.readline().strip().split(",")
    end = header.index("$")
    tokens = []
    for field in header[1:end + 1]:
        tokens.append(field)
        # tokens.append(int(field))
    variables = header[end + 1:]
    for line in input_:
        row = line.strip().split(",")
        state = int(row[0])
        for i in range(len(tokens)):
            token = tokens[i]
            key = (state, token)
            value = row[i + 1]
            if len(value) == 0:
                value = None
            actions[key] = value
        for i in range(len(variables)):
            variable = variables[i]
            key = (state, variable)
            value = row[i + len(tokens) + 1]
            if len(value) == 0:
                value = None
            gotos[key] = value
    return (actions, gotos)


def printActions(actions):
    '''prints the given actions, one per line'''
    for key in actions:
        print(key, end=" -> ")
        print(actions[key])


def printGotos(gotos):
    '''prints the given gotos, one per line'''
    for key in gotos:
        print(key, end=" -> ")
        print(gotos[key])


def parse(input_, grammar, actions, gotos):
    """given an input (a source program), grammar, actions, and gotos,
       returns true/false depending whether the input should be accepted or not"""

    stack = []
    stack.append(0)
    while True:
        print("stack: ", end="")
        print(stack, end=" ")
        print("input_: ", end="")
        print(input_, end=" ")
        state = stack[-1]
        token = input_[0]
        action = actions[(state, token)]
        print("action: ", end="")
        print(action)
        if action is None:
            return False

        # TODO: implement the shift operation
            # (reads last value in imput and stores that as well as the state in the stack)

        if 's' in action:
            sNumber = int(action[1:])
            stack.append(input_.pop(0))
            stack.append(sNumber)

            # TODO: implement the reduce operation(pops the value and state from the stack and reduces)
        if 'r' in action:
            sNumber = int(action[1:])
            # gets the right hand side of the reduction from grammar
            reduction = getRHS(grammar[sNumber])
            # removes 2 times the length of the reduction from the stack
            del stack[-len(reduction) * 2:]
            # gets the left hand side of the reduction from grammar
            reduction = getLHS(grammar[sNumber])
            # appends the reduction change to the stack
            stack.append(reduction)
            reduction = gotos[stack[-2], stack[-1]]
            # appends the new goto number to the stack cast as an integer
            stack.append(int(reduction))

        # TODO: not a shift or reduce operation, must be an "accept" operation
        if 'acc' in action:
            return True


if __name__ == "__main__":

    # check if source file was passed and exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file!")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Could not open source file.")
    text = source.read()
    source.close()
    output = []

    with open("grammar.txt", "rt") as f:
        grammar = loadGrammar(f)
        printGrammar(grammar)

    with open("slr_table.csv", "rt") as f:
        actions, gotos = loadTable(f)
        printActions(actions)
        printGotos(gotos)

    # in the beginning we will write the input...
    # as a sequence of terminal symbols, ending by $
    # the input will be the output of the lexical analyzer

    output = []

    while True:
        text, lexeme, token = lex.lex(text) # lex() returns (lexeme, token)
        if not token:
            break
        output.append(token)

    if parse(output, grammar, actions, gotos):
        print("Input is syntactically correct!")
    else:
        print("Code has syntax errors!")
