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


def getChar(input_):  # TODO getChar update with new Grammar
    '''reads the next char from input_ and returns its class'''
    if len(input_) == 0:
        return (None, CharClass.EOF)
    c = input_[0].lower()
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


def getNonBlank(input_):
    '''calls getChar and getChar until it returns a non-blank'''
    ignore = ""
    while True:
        c, charClass = getChar(input_)
        if charClass == CharClass.BLANK:
            input_, ignore = addChar(input_, ignore)
        else:
            return input_


def addChar(input_, lexeme):
    '''adds the next char from input_ to lexeme, advancing the input_ by one char'''
    if len(input_) > 0:
        lexeme += input_[0]
        input_ = input_[1:]
    return (input_, lexeme)


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
    "boolean": Token.BOOLEAN_TYPE,
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


def lex(input_):
    '''returns the next (lexeme, token) pair or None if EOF is reached'''

    input_ = getNonBlank(input_)

    c, charClass = getChar(input_)
    lexeme = ""

    # check EOF first
    if charClass == CharClass.EOF:
        return (input_, None, None)

    # TODO: read letters
    if charClass == CharClass.LETTER:
        input_, lexeme = addChar(input_, lexeme)
        while getChar(input_)[1] in (charClass.LETTER,
                                    charClass.DIGIT):
            input_, lexeme = addChar(input_, lexeme)
        if lexeme in KEYWORDS:
            return(input_, lexeme, KEYWORDS[lexeme])
        if lexeme in LOOKUP:
            return(input_, lexeme, LOOKUP[lexeme])
        return(input_, lexeme, Token.IDENTIFIER)

    # TODO: return digit literal vs identifier
    if charClass == CharClass.DIGIT:
        while True:
            input_, lexeme = addChar(input_, lexeme)
            c, charClass = getChar(input_)
            if charClass != CharClass.DIGIT:
                break
        return (input_, lexeme, Token.INTEGER_LITERAL)

    # TODO: read an operator
    # TODO add conditional for :=
    if charClass == CharClass.OPERATOR:
        input_, lexeme = addChar(input_, lexeme)
        if c in ('<', '>') and getChar(input_)[0] == '=':
            input_, lexeme = addChar(input_, lexeme)
        if lexeme in LOOKUP:
            return (input_, lexeme, LOOKUP[lexeme])

    if charClass == CharClass.PUNCTUATOR:
        input_, lexeme = addChar(input_, lexeme)
        if c == ':' and getChar(input_)[0] == '=':
            input_, lexeme = addChar(input_, lexeme)
            return (input_, lexeme, Token.ASSIGNMENT)
        if lexeme in LOOKUP:
            return (input_, lexeme, LOOKUP[lexeme])

    # TODO: anything else, raise an exception (change with syntax analyzer)
    raise Exception("Lexical Analyzer Error: unrecognized symbol was found!")

if __name__ == "__main__":

    # check if source file was passed and exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file!")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Could not open source file.")
    input_ = source.read()
    source.close()
    output = []

    while True:  # main loop
        input_, lexeme, token = lex(input_)
        if lexeme == None:
            break
        output.append((lexeme, token))

    for (lexeme, token) in output:  # prints output
        print(lexeme, token)
