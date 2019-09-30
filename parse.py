# CS3210 - Principles of Programming Languages - Fall 2019
# A Syntax Analyzer for an expression
# Author: Thyago Mota
# Contributors:
#   Conor McCandless
#   Casey Jones

import sys
from termcolor import colored
from lex import Lexer
from tree import Tree

SYMBOLS = {
    'period':         '.',
    'colon':          ':',
    'semicolon':      ';',
    'assignment':     ':=',
    'addition':       '+',
    'subtraction':    '-',
    'multiplication': '*',
    'greater':        '>',
    'greater_eq':     '>=',
    'equal':          '=',
    'less_equal':     '<=',
    'less':           '<'
    }

ERROR_MAPPING = {  # tuples of missing tokens mapped to corresponding errors

    ('identifier',):
        7,  # Identifier expected.

    ('$',):
        6,  # EOF expected.

    tuple(sorted(['var', 'begin'])):
        8,  # Special word missing.

    (':=',):
        9,  # Symbol missing.

    tuple(sorted(['+', '-', '<', '<=', '>', '>=', '='])):
        9,  # Symbol missing.

    tuple(sorted(['integer_type',
                  'boolean_type'])):
        10,  # Data type expected.

    tuple(sorted(['identifier',
                  'integer_literal',
                  'true', 'false'])):
        11  # Identifier or literal value expected.
}

ERROR = {  # error codes mapped to their type and message
    1:  ValueError  (colored("Error #1", 'red') + ": "
                     + colored("Source file missing.", 'yellow')),
    2:  IOError     (colored("Error #2", 'red') + ": "
                     + colored("Could not open source file.", 'yellow')),
    3:  Exception   (colored("Error #3", 'red') + ": "
                     + colored("Lexical error", 'yellow')),
    4:  IOError     (colored("Error #4", 'red') + ": "
                     + colored("Couldn’t open grammar file.", 'yellow')),
    5:  IOError     (colored("Error #5", 'red') + ": "
                     + colored("Couldn’t open SLR table file.", 'yellow')),
    6:  SyntaxError (colored("Error #6", 'red') + ": "
                     + colored("EOF expected.", 'yellow')),
    7:  SyntaxError (colored("Error #7", 'red') + ": "
                     + colored("Identifier expected.", 'yellow')),
    8:  SyntaxError (colored("Error #8", 'red') + ": "
                     + colored("Special word missing.", 'yellow')),
    9:  SyntaxError (colored("Error #9", 'red') + ": "
                     + colored("Symbol missing.", 'yellow')),
    10: SyntaxError (colored("Error #10", 'red') + ": "
                     + colored("Data type expected.", 'yellow')),
    11: SyntaxError (colored("Error #11", 'red') + ": "
                     + colored("Identifier or literal value expected.", 'yellow')),
    99: SyntaxError (colored("Error #99", 'red') + ": "
                     + colored("Syntax error!", 'yellow'))
}


def loadGrammar(input_):
    """reads the given input,
       returns the grammar as a list of productions"""

    grammar = []

    for line in input_:
        grammar.append(line.strip())

    return grammar


def getLHS(production):
    '''returns the left-hand side of a given production'''

    return production.split("->")[0].strip()


def getRHS(production):
    '''returns the right-hand side of a given production'''

    return production.split("->")[1].strip().split(" ")


def printGrammar(grammar):
    '''prints the productions of a given grammar, one per line'''

    for production in grammar:
        print(getLHS(production), end=" -> ")
        print(getRHS(production))


def loadTable(input_):
    """reads the given input containing an SLR parsing table,
       returns the "actions" and "gotos" as dictionaries"""

    actions = {}
    gotos = {}
    header = input_.readline().strip().split(",")[1:]
    end = header.index("$")
    tokens = []
    tokens = header[:end + 1]
    # print('tokens:', tokens)
    variables = header[end + 1:]
    # print('variables:', variables)

    for line in input_:

        # print('line:', line)
        row = line.strip().split(",")
        state = int(row[0])
        # print('state:', state)

        for i in range(len(tokens)):
            token = tokens[i]
            # print('token:', tokens[i])
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
        print(key, "->", actions[key])


def printGotos(gotos):
    '''prints the given gotos, one per line'''

    for key in gotos:
        print(key, "->", gotos[key])


def parse(tokens, grammar, actions, gotos):
    """given an input (a source program), grammar, actions, and gotos,
       returns Tree object if input accepted, or None if not"""

    tokens = {key:
              SYMBOLS[token]
              if token in SYMBOLS
              else token
              for key, token
              in tokens.items()}

    trees = []
    stack = []
    stack.append(0)
    keys = list(tokens.keys())

    while True:

        # print("stack: ", stack)
        # print("input: ", tokens)
        state = stack[-1]
        token = tokens[keys[0]]
        action = actions[(state, token)]
        # print("action: ", end="")
        # print(action)

        if action is None:

            print("stack:",  ', '.join([str(element)
                                        for element
                                        in stack]))

            print("input:", ', '.join([element
                                       for element
                                       in tokens.values()]))

            expected_tokens = [action[1]
                               for action in actions
                               if actions[action]
                               and action[0] == stack[-1]]

            expected_tokens = [SYMBOLS[token]
                               if token in SYMBOLS
                               else token
                               for token in expected_tokens]

            print(colored("Syntax error at "
                          + "line " + str(keys[0][0]) + ', '
                          + "column " + str(keys[0][1]) + "!",
                          'red'))

            print(colored("  Expected: "
                          + ' or '.join(expected_tokens),
                          'yellow'))

            expected_tokens = tuple(sorted(expected_tokens))
            if expected_tokens in ERROR_MAPPING:
                raise ERROR[ERROR_MAPPING[expected_tokens]]
            else:
                raise ERROR[99]

            return None

        if 's' in action:  # shift
            # read last value in input, push state to stack

            sNumber = int(action[1:])
            stack.append(tokens.pop(keys[0]))
            keys.pop(0)
            stack.append(sNumber)

            newTree = Tree()  # create new tree
            newTree.data = token  # set data to token
            trees.append(newTree)  # append to list of trees

        if 'r' in action:  # pop value & state from the stack, reduce

            sNumber = int(action[1:])

            rhs = getRHS(grammar[sNumber])  # right-hand side of reduction
            del stack[-len(rhs) * 2:]  # pop 2x reduction length from stack

            lhs = getLHS(grammar[sNumber])  # left-hand side of reduction
            stack.append(lhs)  # push reduction change to stack

            goto = gotos[stack[-2], stack[-1]]  # push goto # to stack
            stack.append(int(goto))

            # create new tree, set data to LHS
            newerTree = Tree()
            newerTree.data = lhs

            # add len(rhs) trees from list as children of new tree
            for tree in trees[-len(rhs):]:
                newerTree.add(tree)

            trees = trees[:-len(rhs)]  # remove these from list

            trees.append(newerTree)  # append new tree to list of trees

        if 'acc' in action:  # accept

            production = grammar[0]
            lhs = getLHS(production)
            rhs = getRHS(production)

            # same as reduce but with first rule of grammar
            root = Tree()
            root.data = lhs
            for tree in trees:
                root.add(tree)

            return root  # return the new tree


if __name__ == "__main__":

    if len(sys.argv) != 2:  # check that source path argument was passed
        raise ERROR[1]  # Source file missing.

    try:  # check that source file can be read
        with open(sys.argv[1], "rt") as source:
            input_ = source.read()
    except IOError:
        raise ERROR[2]  # Could not open source file.

    try:  # check that grammar file can be read
        with open("grammar.txt", "rt") as f:
            grammar = loadGrammar(f)
            # printGrammar(grammar)
    except IOError:
        raise ERROR[4]  # Couldn’t open grammar file.

    try:  # check that SLR table can be read
        with open("slr_table.csv", "rt") as f:
            actions, gotos = loadTable(f)
            # printActions(actions)
    except IOError:
        raise ERROR[5]  # Couldn’t open SLR table file.

    # in the beginning we will write the input...
    # as a sequence of terminal symbols, ending by $
    # the input will be the output of the lexical analyzer

    output = []

    try:
        lexer = Lexer(input_)
        tokens = {key: result[1].name.lower() # result = (lexeme, token)
                  for key, result
                  in lexer.output.items()}
    except:
        raise ERROR[3]  # Lexical error

    tree = parse(tokens, grammar, actions, gotos)

    if tree:
        print("Input is syntactically correct!")
        tree.print()
    else:
        print("Code has syntax errors!")
