# CS3210 - Principles of Programming Languages - Fall 2019
# A Syntax Analyzer for an expression

from tree import Tree


def loadGrammar(input):
    '''reads the given input and returns the grammar as a list of productions'''
    grammar = []
    for line in input:
        grammar.append(line.strip())
    return grammar


def getLHS(production):
    '''returns the LHS (left hand side) of a given production'''
    return production.split("->")[0].strip()


def getRHS(production):
    '''returns the RHS (right hand side) of a given production'''
    return production.split("->")[1].strip().split(" ")


def printGrammar(grammar):
    '''prints the productions of a given grammar, one per line'''
    i = 0
    for production in grammar:
        print(str(i) + ". " + getLHS(production), end=" -> ")
        print(getRHS(production))
        i += 1


def loadTable(input):
    """reads the given input containing an SLR parsing table
       and returns the "actions" and "gotos" as dictionaries"""

    actions = {}
    gotos = {}
    header = input.readline().strip().split(",")
    end = header.index("$")
    tokens = []
    for field in header[1:end + 1]:
        tokens.append(field)
        # tokens.append(int(field))
    variables = header[end + 1:]
    for line in input:
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


def parse(input, grammar, actions, gotos):
    """given an input (source program), grammar, actions, and gotos,
       returns true/false depending whether the input should be accepted or not"""

    # TODO #1: create a list of trees
    trees = []

    stack = []
    stack.append(0)
    while True:
        print("stack: ", end="")
        print(stack, end=" ")
        print("input: ", end="")
        print(input, end=" ")
        state = stack[-1]
        token = input[0]
        action = actions[(state, token)]
        print("action: ", end="")
        print(action)

        if action is None:
            return None  # tree building update

        # shift operation
        if action[0] == 's':
            input.pop(0)
            stack.append(token)
            state = int(action[1])
            stack.append(state)

            # TODO #2: create a new tree, set data to token, and append it to the list of trees
            newTree = Tree()
            newTree.data = token
            trees.append(newTree)

        # reduce operation
        elif action[0] == 'r':
            production = grammar[int(action[1])]
            lhs = getLHS(production)
            rhs = getRHS(production)
            for i in range(len(rhs) * 2):
                stack.pop()
            state = stack[-1]
            stack.append(lhs)
            stack.append(int(gotos[(state, lhs)]))

            # TODO #3: create a new tree and set data to lhs
            newerTree = Tree()
            newerTree.data = lhs

            # TODO #4: get "len(rhs)" trees from the right of the list of trees and add each of them as child of the new tree you created, preserving the left-right order
            for tree in trees[-len(rhs):]:
                newerTree.add(tree)

            # TODO #5: remove "len(rhs)" trees from the right of the list of trees
            trees = trees[:-len(rhs)]

            # TODO #6: append the new tree to the list of trees
            trees.append(newerTree)

        # not a shift or reduce operation, must be an "accept" operation
        else:
            production = grammar[0]
            lhs = getLHS(production)
            rhs = getRHS(production)

            # TODO #7: same as reduce but using the 1st rule of the grammar
            root = Tree()
            root.data = lhs
            for tree in trees:
                root.add(tree)

            # TODO #8: return the new tree
            return root


if __name__ == "__main__":

    input = open("grammar.txt", "rt")
    grammar = loadGrammar(input)
    # printGrammar(grammar)
    input.close()

    input = open("slr_table.csv", "rt")
    actions, gotos = loadTable(input)
    # printActions(actions)
    # printGotos(gotos)
    input.close()

    # in the beginning we will write the input...
    # as a sequence of terminal symbols, ending by $
    # later we will integrate this code with the lexical analyzer

    input = ['l', '+', 'i', '/', 'l', '*', 'l', '$']

    # tree building update
    tree = parse(input, grammar, actions, gotos)

    if tree:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        tree.print("")
    else:
        print("Code has syntax errors!")
