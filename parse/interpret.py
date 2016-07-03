import sys, re
import Equation, parser, json
from arpeggio.cleanpeg import ParserPEG

def math_parser(command, verbose=True):
    fn = Equation.Expression(command)
    if repr(fn) == '':
        raise RuntimeError("Failed to parse.")
    if verbose:
        print "Parsed by Equation."

    return fn

def python_parser(command, verbose=True):
    st = parser.expr(command)
    if verbose:
        print "Parsed by Python 2.7."

    return st

def json_parser(command, verbose=True):
    tree = json.loads(command)
    if verbose:
        print "Parsed as JSON."

    return tree

def peg_parser(language, grammar, root):
    with open(grammar, 'r') as fp:
        parser = ParserPEG(fp.read(), root)
        def parse(command, verbose=True):
            parse_tree = parser.parse(command)
            print "Parsed by", language, "PEG."
            return parse_tree

        return parse

# In priority order
interpreters = [{'calc4': peg_parser("4-Operator Calc.", "grammars/calc4.peg", 'calc')},
                {'json': json_parser},
                {'math': math_parser,
                 'bash': peg_parser("Bash", "grammars/bash.peg", 'command'),
                 'python': python_parser},
                {'csv': peg_parser("CSV", "grammars/csv.peg", 'csvfile')}]

recognizeds = {'math': [r'sqrt\(', r'\^'],
               'python': [r'^def ', ':'],
               'bash': [r'^cd ', '^ls ', '/']}

def by_priority(command, verbose=True):
    for priority in interpreters:
        matches = {}
        for language in priority:
            try:
                result = priority[language](command, verbose)
                matches[language] = result
            except:
                pass
        if matches:
            return matches

    if verbose:
        print "Unknown language."
    return {}

def compare_recognizeds(command, languages, verbose=True):
    best_count = 0
    best_language = None
    for language in languages:
        count = count_recognizeds(command, recognizeds[language])
        if count > 0:
            print "Recognized", count, "from", language
            if count > best_count:
                best_language = language
                best_count = count

    return best_language

def count_recognizeds(command, patterns):
    count = 0
    for pattern in patterns:
        if re.search(pattern, command):
            count += 1

    return count

def guess(command, verbose=True):
    matches = by_priority(command, verbose)
    if len(matches) == 1:
        key = matches.keys()[0]
        return key, matches[key]

    if not matches:
        language = compare_recognizeds(command, recognizeds.keys(), verbose)
        return language, None
    else:
        language = compare_recognizeds(command, matches.keys(), verbose)
        return language, matches[language]

if __name__ == '__main__':
    language, parsed = guess(sys.argv[1], verbose=True)
    print language
    print parsed
