# SyntaxAnalyzer
#Programming assignment 1 for CS3210, Principles of Programming Languages. Metropolitan State University of Denver.
#Collaborators:
#Dr. Thyago Mota,
#Conor McCandless,
#Casey Jones

Syntax Analyzer for the grammar given in grammar.txt. Program uses a lexical analyzer to scan a source file and generate tokens for each
term. The syntax analyzer then takes this input and parses it using a bottom-up parsing method. The source file is then determined to be
syntactically correct or incorrect. If there are syntax errors the program will generate an error code depicting the cause of the syntax
error. If there are no syntax errors a parse tree is generated and displayed to the console. This parse tree shows paths taken to determine
that the given source file is syntactically correct.

#Requirements:
in order to generate the tree you must run:
pip install tree-format

In the directory where the program is located.
