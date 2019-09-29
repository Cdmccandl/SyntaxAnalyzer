# CS3210 - Principles of Programming Languages - Fall 2019
# A Lexical Analyzer for an expression
# Author: Thyago Mota
# Contributors:
#   Conor McCandless
#   Casey Jones

from enum import Enum
import sys


class CharClass(Enum):
    '''all char classes'''
    EOF = 1
    LETTER = 2
    DIGIT = 3
    OPERATOR = 4
    PUNCTUATOR = 5
    QUOTE = 6
    BLANK = 7
    OTHER = 8


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

class EOF():
    name = '$'

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


class Lexer:

    def __init__(self, input_):
        self.input = input_
        self.results = {}
        self.pos = 0
        self.line = 1
        self.column = 1

    @property
    def c(self):
        '''current character'''
        return self.input[self.pos].lower()

    @property
    def charClass(self):
        '''charClass of current character'''

        if self.pos == len(self.input):
            return CharClass.EOF
        if self.c.isalpha():
            return CharClass.LETTER
        if self.c.isdigit():
            return CharClass.DIGIT
        if self.c == '"':
            return CharClass.QUOTE
        if self.c in ['+', '-', '*', '/', '>', '=', '<']:
            return CharClass.OPERATOR
        if self.c in ['.', ':', ',', ';']:
            return CharClass.PUNCTUATOR
        if self.c in [' ', '\n', '\t']:
            return CharClass.BLANK
        return CharClass.OTHER


    def getNonBlank(self):
        '''seek to next non-blank character'''

        while True:
            if self.charClass == CharClass.BLANK:
                self.addChar("") # ignore
            else:
                break


    def addChar(self, lexeme):
        '''add next char from input to lexeme, advance input by one char'''

        if self.pos < len(self.input):
            lexeme += self.input[self.pos]
            if self.c == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1

        return lexeme


    def add_lexeme(self, line, column, lexeme, token):
        self.results[(line, column)] = (lexeme, token)
        return (lexeme, token)

    def lex(self):
        '''returns the next (lexeme, token) pair or None if EOF is reached'''

        self.getNonBlank()

        line = self.line
        column = self.column

        lexeme = ""

        # check EOF first
        if self.charClass == CharClass.EOF:
            return self.add_lexeme(line, column, None, EOF)

        # read letters
        if self.charClass == CharClass.LETTER:
            lexeme = self.addChar(lexeme)
            while self.charClass in (CharClass.LETTER,
                                     CharClass.DIGIT):
                lexeme = self.addChar(lexeme)
            if lexeme in KEYWORDS:
                return self.add_lexeme(line, column, lexeme, KEYWORDS[lexeme])
            if lexeme in LOOKUP:
                return self.add_lexeme(line, column, lexeme, LOOKUP[lexeme])
            return self.add_lexeme(line, column, lexeme, Token.IDENTIFIER)

        # return digit literal vs identifier
        if self.charClass == CharClass.DIGIT:
            while True:
                lexeme = self.addChar(lexeme)
                if self.charClass != CharClass.DIGIT:
                    break
            return self.add_lexeme(line, column, lexeme, Token.INTEGER_LITERAL)

        # read an operator
        if self.charClass == CharClass.OPERATOR:
            lexeme = self.addChar(lexeme)
            if lexeme in ('<', '>') and self.c == '=':
                lexeme = self.addChar(lexeme)
            if lexeme in LOOKUP:
                return self.add_lexeme(line, column, lexeme, LOOKUP[lexeme])

        # read an punctuator
        if self.charClass == CharClass.PUNCTUATOR:
            lexeme = self.addChar(lexeme)
            if lexeme == ':' and self.c == '=':
                lexeme = self.addChar(lexeme)
                return self.add_lexeme(line, column, lexeme, Token.ASSIGNMENT)
            if lexeme in LOOKUP:
                return self.add_lexeme(line, column, lexeme, LOOKUP[lexeme])

        # anything else, raise an exception
        raise Exception("Lexical Analyzer Error: unrecognized symbol!")

    @property
    def output(self):

        while True:
            lexeme, token = self.lex()
            if token == EOF:
                break

        return self.results

if __name__ == "__main__":

    if len(sys.argv) != 2:  # check that source path argument was passed
        raise ValueError("Missing source file!")

    try:  # check that source file can be read
        with open(sys.argv[1], "rt") as source:
            input_ = source.read()
    except IOError:
        raise IOError("Could not open source file.")

    lexer = Lexer(input_)

    for lexeme, token in lexer.output.values():
        print(lexeme, token)
