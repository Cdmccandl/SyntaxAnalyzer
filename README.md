# CS3210 - Principles of Programming Languages - Fall 2019
# Metropolitan State University of Denver
# Programming assignment 1: Syntax Analyzer
# Conor McCandless
# Casey Jones

Syntax Analyzer for the grammar given in grammar.txt.
The program uses a lexical analyzer to scan a source file and generate tokens for each term.
The syntax analyzer then takes this input and parses it using a bottom-up parsing method.
The source file is then determined to be syntactically correct or incorrect.
If there are syntax errors, the program will generate an error code depicting the cause.
If there are no syntax errors, a parse tree is generated and displayed on the console.
This parse tree shows paths taken to determine that the given source file is syntactically correct.

#Requirements:
The external modules tree-format and termcolor are used as dependencies.
These are bundled along with this distribution.
Alternatively, they may be installed with either the following command:
	pip install -r requirements.txt
Or:
	pip install tree-format termcolor
