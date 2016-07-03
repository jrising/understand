from arpeggio.cleanpeg import ParserPEG

with open("grammars/calc4.peg", 'r') as fp:
    parser = ParserPEG(fp.read(), "calc")
    input_expr = "-(4-1)*5+(2+4.67)+5.89/(.2+7)"
    parse_tree = parser.parse(input_expr)

    print parse_tree

with open("grammars/bash.peg", 'r') as fp:
    parser = ParserPEG(fp.read(), "command")
    input_expr = "ls *"
    parse_tree = parser.parse(input_expr)

    print parse_tree

with open("grammars/python27.peg", 'r') as fp:
    parser = ParserPEG(fp.read(), "single_input")
    input_expr = "print -(4-1)*5+(2+4.67)+5.89/(.2+7)"
    parse_tree = parser.parse(input_expr)

    print parse_tree
