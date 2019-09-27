# CS3210 - Principles of Programming Languages - Fall 2019
# A Lexical Analyzer for an expression

from enum import Enum
import sys

# all char classes
# TODO update CharClass with new Grammar


class CharClass(Enum):
    EOF = 1
    LETTER = 2
    DIGIT = 3
    OPERATOR = 4
    PUNCTUATOR = 5
    QUOTE = 6
    BLANK = 7
    OTHER = 8


def getChar(input):  # TODO getChar update with new Grammar
    '''reads the next char from input and returns its class'''
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


def getNonBlank(input):
    '''calls getChar and getChar until it returns a non-blank'''
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input


def addChar(input, lexeme):
    '''adds the next char from input to lexeme, advancing the input by one char'''
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)


class Token(Enum):
    '''all tokens'''
    ADDITION = 1
    ASSIGNMENT = 2
    BEGIN = 3
    BOOLEAN_TYPE = 4
    COLON = 5
    DO = 6
    ELSE = 7
    END = 8
    EQUAL = 9
    FALSE = 10
    GREATER = 11
    GREATER_EQUAL = 12
    IDENTIFIER = 13
    IF = 14
    INTEGER_LITERAL = 15
    INTEGER_TYPE = 16
    LESS = 17
    LESS_EQUAL = 18
    MULTIPLICATION = 19
    PERIOD = 20
    PROGRAM = 21
    READ = 22
    SEMICOLON = 23
    SUBTRACTION = 24
    THEN = 25
    TRUE = 26
    VAR = 27
    WHILE = 28
    WRITE = 29


LOOKUP = {  # lexeme to token conversion
    # TODO how to represent integer literal and type
    "+": Token.ADDITION,
    "-": Token.SUBTRACTION,
    "*": Token.MULTIPLICATION,
    "begin": Token.BEGIN,
    ":": Token.COLON,
    ":=": Token.ASSIGNMENT,
    "bool": Token.BOOLEAN_TYPE,
    "do": Token.DO,
    "else": Token.ELSE,
    "end": Token.END,
    "=": Token.EQUAL,
    "false": Token.FALSE,
    ">": Token.GREATER,
    ">=": Token.GREATER_EQUAL,
    "if": Token.IF,
    "<": Token.LESS,
    "<=": Token.LESS_EQUAL,
    ".": Token.PERIOD,
    "program": Token.PROGRAM,
    "read": Token.READ,
    ";": Token.SEMICOLON,
    "then": Token.THEN,
    "true": Token.TRUE,
    "while": Token.WHILE,
    "write": Token.WRITE,
    "integer": Token.INTEGER_TYPE,
    "var": Token.VAR
    }

KEYWORDS = {
    "program": Token.PROGRAM,
    "begin": Token.BEGIN,
    "do": Token.DO,
    "else": Token.ELSE,
    "end": Token.END,
    "false": Token.FALSE,
    "true": Token.TRUE,
    "if": Token.IF,
    "read": Token.READ,
    "write": Token.WRITE,
    "while": Token.WHILE,
    "var": Token.VAR
    }


def lex(input):
    '''returns the next (lexeme, token) pair or None if EOF is reached'''

    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # check EOF first
    if charClass == CharClass.EOF:
        return (input, None, None)

    # TODO: read letters
    if charClass == CharClass.LETTER:
        input, lexeme = addChar(input, lexeme)
        while getChar(input)[1] in (charClass.LETTER,
                                    charClass.DIGIT):
            input, lexeme = addChar(input, lexeme)
        if lexeme in KEYWORDS:
            return(input, lexeme, KEYWORDS[lexeme])
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

    # TODO: read an operator
    # TODO add conditional for :=
    if charClass == CharClass.OPERATOR:
        input, lexeme = addChar(input, lexeme)
        if c in ('<', '>') and getChar(input)[0] == '=':
            input, lexeme = addChar(input, lexeme)
        if lexeme in LOOKUP:
            return (input, lexeme, LOOKUP[lexeme])

    if charClass == CharClass.PUNCTUATOR:
        input, lexeme = addChar(input, lexeme)
        if c == ':' and getChar(input)[0] == '=':
            input, lexeme = addChar(input, lexeme)
            return (input, lexeme, Token.ASSIGNMENT)
        if lexeme in LOOKUP:
            return (input, lexeme, LOOKUP[lexeme])

    # TODO: anything else, raise an exception (change with syntax analyzer)
    raise Exception("Lexical Analyzer Error: unrecognized symbol was found!")

if __name__ == "__main__":

    # check if source file was passed and exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Couldn't open source file")
    input = source.read()
    source.close()
    output = []

    while True:  # main loop
        input, lexeme, token = lex(input)
        if lexeme == None:
            break
        output.append((lexeme, token))

    for (lexeme, token) in output:  # prints output
        print(lexeme, token)
