# CS3210 - Principles of Programming Languages - Fall 2019
# A Lexical Analyzer for an expression

from enum import Enum
import sys

# all char classes
#TODO update CharClass with new Grammar
class CharClass(Enum):
    EOF        = 1
    LETTER     = 2
    DIGIT      = 3
    OPERATOR   = 4
    PUNCTUATOR = 5
    QUOTE      = 6
    BLANK      = 7
    OTHER      = 8

# reads the next char from input and returns its class
#TODO getChar update with new Grammar
def getChar(input):
    if len(input) == 0:
        return (None, CharClass.EOF)
    c = input[0].lower()
    if c.isalpha():
        return (c, CharClass.LETTER)
    if c.isdigit():
        return (c, CharClass.DIGIT)
    if c == '"':
        return (c, CharClass.QUOTE)
    if c in ['+', '-', '*', '/', '>', '=', '<']:
        return (c, CharClass.OPERATOR)
    if c in ['.', ':', ',', ';']:
        return (c, CharClass.PUNCTUATOR)
    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)
    return (c, CharClass.OTHER)

# calls getChar and getChar until it returns a non-blank
def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input

# adds the next char from input to lexeme, advancing the input by one char
def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)

# all tokens
class Token(Enum):
    ADD_OP          = 1
    ASSIGNMENT      = 2
    BEGIN           = 3
    BOOLEAN_TYPE    = 4
    COLON           = 5
    DO              = 6
    ELSE            = 7
    END             = 8
    EQUAL           = 9
    FALSE           = 10
    GREATER         = 11
    GREATER_EQUAL   = 12
    IDENTIFIER      = 13
    IF              = 14
    INTEGER_LITERAL = 15
    INTEGER_TYPE    = 16
    LESS            = 17
    LESS_EQUAL      = 18
    MUL_OP          = 19
    PERIOD          = 20
    PROGRAM         = 21
    READ            = 22
    SEMICOLON       = 23
    SUB_OP          = 24
    THEN            = 25
    TRUE            = 26
    VAR             = 27
    WHILE           = 28
    WRITE           = 29
    
    
# lexeme to token conversion
lookup = {
    #TODO how to represent integer literal and type
    "+"      : Token.ADD_OP,
    "-"      : Token.SUB_OP,
    "*"      : Token.MUL_OP,
    "begin"  : Token.BEGIN,
    ":"      : Token.COLON,
    ":="      : Token.ASSIGNMENT,
    "bool"   : Token.BOOLEAN_TYPE,
    "do"     : Token.DO,
    "else"   : Token.ELSE,
    "end"    : Token.END,
    "="     : Token.EQUAL,
    "false"  : Token.FALSE,
    ">"      : Token.GREATER,
    ">="     : Token.GREATER_EQUAL,
    "if"     : Token.IF,
    "<"      : Token.LESS,
    "<="     : Token.LESS_EQUAL,
    "."      : Token.PERIOD,
    "program": Token.PROGRAM,
    "read"   : Token.READ,
    ";"      : Token.SEMICOLON,
    "then"   : Token.THEN,
    "true"   : Token.TRUE,
    "while"  : Token.WHILE,
    "write"  : Token.WRITE,
    "integer": Token.INTEGER_TYPE,
    "var"    : Token.VAR
        
}

# returns the next (lexeme, token) pair or None if EOF is reached
def lex(input):
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # check EOF first
    if charClass == CharClass.EOF:
        return (input, None, None)

    # TODO: reading letters
    if charClass == CharClass.LETTER:
        input, lexeme = addChar(input, lexeme)
        #reads subsequent letters until blank
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass == CharClass.BLANK: #FIXME probably should be letter or number
                break
            if charClass == CharClass.OPERATOR:
                break
        if lexeme == "program":
            return(input, lexeme, Token.PROGRAM)
        elif lexeme == "begin":
            return(input, lexeme, Token.BEGIN)
        elif lexeme == "do":
            return(input, lexeme, Token.DO)
        elif lexeme == "else":
            return(input, lexeme, Token.ELSE)
        elif lexeme == "end":
            return(input, lexeme, Token.END)
        elif lexeme == "false":
            return(input, lexeme, Token.FALSE)
        elif lexeme == "true":
            return(input, lexeme, Token.TRUE)
        elif lexeme == "if":
            return(input, lexeme, Token.IF)
        elif lexeme == "read":
            return(input, lexeme, Token.READ)
        elif lexeme == "write":
            return(input, lexeme, Token.WRITE)
        elif lexeme == "while":
            return(input, lexeme, Token.WHILE)
        elif lexeme == "var":
            return(input, lexeme, Token.VAR)
        else:
            return(input, lexeme, Token.IDENTIFIER)

    # TODO: return digit literal vs identifier
    if charClass == CharClass.DIGIT:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass != CharClass.DIGIT:
                break
        return (input, lexeme, Token.INTEGER_LITERAL)

    # TODO: reading an operator
    #TODO add conditional for := 
    if charClass == CharClass.OPERATOR:
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookup:
            return (input, lexeme, lookup[lexeme])

    # TODO: anything else, raise an exception (change with syntax analyzer)
    raise Exception("Lexical Analyzer Error: unrecognized symbol was found!")

# main
if __name__ == "__main__":

    #checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Couldn't open source file")
    input = source.read()
    source.close()
    output = []

    # main loop
    while True:
        input, lexeme, token = lex(input)
        if lexeme == None:
            break
        output.append((lexeme, token))

    # prints the output
    for (lexeme, token) in output:
        print(lexeme, token)
