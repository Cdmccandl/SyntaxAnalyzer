# CS3210 - Principles of Programming Languages - Fall 2019
# A Syntax Analyzer for an expression

# reads the given input and returns the grammar as a list of productions
def loadGrammar(input):
    grammar = []
    for line in input:
        grammar.append(line.strip())
    return grammar

# returns the LHS (left hand side) of a given production
def getLHS(production):
    return production.split("->")[0].strip()

# returns the RHS (right hand side) of a given production
def getRHS(production):
    return production.split("->")[1].strip().split(" ")

# prints the productions of a given grammar, one per line
def printGrammar(grammar):
    for production in grammar:
        print(getLHS(production), end = " -> ")
        print(getRHS(production))

# reads the given input containing an SLR parsing table and returns the "actions" and "gotos" as dictionaries
def loadTable(input):
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

# prints the given actions, one per line
def printActions(actions):
    for key in actions:
        print(key, end = " -> ")
        print(actions[key])
        

# prints the given gotos, one per line
def printGotos(gotos):
    for key in gotos:
        print(key, end = " -> ")
        print(gotos[key])

# given an input (source program), grammar, actions, and gotos, returns true/false depending whether the input should be accepted or not
def parse(input, grammar, actions, gotos):
    stack = []
    stack.append(0)
    while True:
        print("stack: ", end = "")
        print(stack, end = " ")
        print("input: ", end = "")
        print(input, end = " ")
        state = stack[-1]
        token = input[0]
        action = actions[(state, token)]
        print("action: ", end = "")
        print(action)
        if action is None:
            return False
        
        # TODO: implement the shift operation (reads last value in imput and stores that as well as the state in the stack)
        
        if 's' in action:
            sNumber = int(action[1:])
            stack.append(input.pop(0))
            stack.append(sNumber)
        
            # TODO: implement the reduce operation(pops the value and state from the stack and reduces)
        if 'r' in action:
            sNumber = int(action[1:])
            reduction = getRHS(grammar[sNumber]) #gets the right hand side of the reduction from grammar
            del stack[-len(reduction) * 2:]      #removes 2 times the length of the reduction from the stack
            reduction = getLHS(grammar[sNumber]) # gets the left hand side of the reduction from grammar
            stack.append(reduction)             # appends the reduction change to the stack
            reduction = gotos[stack[-2],stack[-1]]  
            stack.append(int(reduction))        #appends the new goto number to the stack cast as an integer

        # TODO: not a shift or reduce operation, must be an "accept" operation
        if 'acc' in action:
            return True

# main
if __name__ == "__main__":
    
    input = open("grammar.txt", "rt")
    grammar = loadGrammar(input)
    printGrammar(grammar)
    input.close()
    
    input = open("slr_table.csv", "rt")
    actions, gotos = loadTable(input)
    printActions(actions)
    printGotos(gotos)
    input.close()
    
    # in the beginning we will write the input as a sequence of terminal symbols, ending by $
    # input will be the output of the lexical analyzer
    input = [ 'l', '+', 'i', '/', 'l', '*', 'l', '$' ]
    if parse(input, grammar, actions, gotos):
        print("Input is syntactically correct!")
    else:
        print("Code has syntax errors!")
