# CS3210 - Principles of Programming Languages - Fall 2019
# A Syntax Analyzer for an expression
# Author: Thyago Mota
# Contributors:
#   Conor McCandless
#   Casey Jones

import sys
import lex
from tree import Tree

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
    header = input_.readline().strip().split(",")[1:]
    end = header.index("$")
    tokens = []
    tokens = header[:end + 1]
    print('tokens:', tokens)
    variables = header[end + 1:]
    print('variables:', variables)
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


def parse(input_, grammar, actions, gotos):
    """given an input (a source program), grammar, actions, and gotos,
       returns true/false depending whether the input should be accepted or not"""

    trees = []
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
            print("Expected:",
                  ' or '.join(
                      action[1] for action in actions
                      if actions[action]
                      and action[0] == stack[-1]))
            return False

        if 's' in action: # shift
            # read last value in input, push state to stack

            sNumber = int(action[1:])
            stack.append(input_.pop(0))
            stack.append(sNumber)

            newTree = Tree() # create new tree
            newTree.data = token # set data to token
            trees.append(newTree) # append to list of trees


        if 'r' in action: # pop value & state from the stack, reduce

            sNumber = int(action[1:])

            rhs = getRHS(grammar[sNumber]) # right-hand side of reduction
            del stack[-len(rhs) * 2:] # pop 2x reduction length from stack

            lhs = getLHS(grammar[sNumber]) # left-hand side of reduction
            stack.append(lhs) # push reduction change to stack

            goto = gotos[stack[-2], stack[-1]] # push goto # to stack
            stack.append(int(goto))

            # create new tree, set data to LHS
            newerTree = Tree()
            newerTree.data = lhs

            # add len(rhs) trees from list as children of new tree
            for tree in trees[-len(rhs):]:
                newerTree.add(tree)

            trees = trees[:-len(rhs)] # remove these from list

            trees.append(newerTree) # append new tree to list of trees


        if 'acc' in action: # accept

            production = grammar[0]
            lhs = getLHS(production)
            rhs = getRHS(production)

            # same as reduce but with first rule of grammar
            root = Tree()
            root.data = lhs
            for tree in trees:
                root.add(tree)

            return root # return the new tree


if __name__ == "__main__":

    if len(sys.argv) != 2: # check that source path argument was passed
        raise ValueError("Error #1: Source file missing.")
    
    try: # check that source file can be read
        with open(sys.argv[1], "rt") as source:
            text = source.read()
    except IOError:
        raise IOError("Error #2: Could not open source file.")

    try: # check that grammar file can be read
        with open("grammar.txt", "rt") as f:
            grammar = loadGrammar(f)
            # printGrammar(grammar)
    except IOError:
        raise IOError("Error #4: Couldn’t open grammar file.")

    try: # check that SLR table can be read
        with open("slr_table.csv", "rt") as f:
            actions, gotos = loadTable(f)
            # printActions(actions)
    except IOError:
        raise IOError("Error #5: Couldn’t open SLR table file.")

    # in the beginning we will write the input...
    # as a sequence of terminal symbols, ending by $
    # the input will be the output of the lexical analyzer

    output = []

    while True:
        try:
            text, lexeme, token = lex.lex(text) # lex() returns (lexeme, token)
        except:
            raise Exception("Error #3: Lexical error")
        if not token:
            break
        token = token.name.lower()
        output.append(token)
    output.append('$')

    tree = parse(output, grammar, actions, gotos)

    if tree:
        print("Input is syntactically correct!")
        tree.print()
    else:
        print("Code has syntax errors!")
