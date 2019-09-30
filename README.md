# CS3210 - Principles of Programming Languages
## Programming assignment 1: Syntax Analyzer
### Fall 2019, Metropolitan State University of Denver
#### Conor McCandless, Casey Jones

a syntax analyzer for the grammar given in grammar.txt

To parse your source code, run parse.py with your file's path as the only argument:
```
python parse.py [SOURCE_FILE]
```

You can also view the lexemes and tokens identified by the lexer by running lex.py in similar fashion:
```
python lex.py [SOURCE_FILE]
```

The syntax analyzer uses the lexical analyzer to scan a source file and generate tokens for each term.
It then parses these symbols using a bottom-up parsing method.
The source file is then determined to be syntactically correct or incorrect.
If there are syntax errors, the program will generate an error code depicting the cause.
If there are no syntax errors, a parse tree is generated and displayed on the console.
The parse tree will show the paths taken to verify that the given source file was syntactically correct.

## Requirements

The external modules tree-format and termcolor are used as dependencies.
These are bundled along with this distribution.

Alternatively, they may be installed with either `pip install -r requirements.txt` or `pip install tree-format termcolor`.
