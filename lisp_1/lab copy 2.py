"""
6.101 Lab 12:
LISP Interpreter Part 1
"""

#!/usr/bin/env python3

from cmd import Cmd
import traceback
import re
import os
import sys
import doctest

sys.setrecursionlimit(20_000)

# NO ADDITIONAL IMPORTS!

#############################
# Scheme-related Exceptions #
#############################


class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    cl_source = source
    loop = cl_source.count(";")
    for i in range(loop):
        s_index = cl_source.find(";")
        substr = cl_source[s_index:]
        e_index = len(cl_source) - 1
        if '\n' in substr:
            e_index = substr.index('\n') + s_index + 1
        if e_index != len(cl_source) - 1:
            cl_source = cl_source[0:s_index] + cl_source[e_index:]
        else:
            cl_source = cl_source[0:s_index]

    if "\n" in cl_source:
        cl_source.replace("\n", "")

    chunks = cl_source.split()
    all_tokens = []

    def parenthesis_check(chunk):
        if len(chunk) == 1:
            return chunk
        tokens = []
        if "(" in chunk and ")" in chunk:
            length = 0
            for i in range(len(chunk)):
                if chunk[i] == "(" or chunk[i] == ")":
                    if length != 0:
                        tokens.append(chunk[i-length: i])
                        length = 0
                    tokens.append(chunk[i])
                else:
                    length += 1
        elif "(" in chunk:
            index = chunk.index("(")
            if index == 0:
                "pass"
                tokens.append("(")
                tokens.extend(parenthesis_check(chunk[1:]))
            elif index == len(chunk) - 1:
                tokens.extend(parenthesis_check(chunk[0:-1]))
                tokens.append("(")
            else:
                tokens.extend(parenthesis_check(chunk[0:index]))
                tokens.append("(")
                tokens.extend(parenthesis_check(chunk[index+1:]))
        elif ")" in chunk:
            index = chunk.index(")")
            print(chunk)
            if index == 0:
                tokens.append(")")
                tokens.extend(parenthesis_check(chunk[1:]))
            elif index == len(chunk) - 1:
                tokens.extend(parenthesis_check(chunk[0:-1]))
                tokens.append(")")
            else:
                tokens.extend(parenthesis_check(chunk[0:index]))
                tokens.append(")")
                print(chunk[index + 1:])
                tokens.extend(parenthesis_check(chunk[index+1:]))

        else:
            tokens.append(chunk)

        return tokens

    for chunk in chunks:
        all_tokens.extend(parenthesis_check(chunk))
    return all_tokens


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    if tokens[-1] != ')' and len(tokens) > 1:
        raise SchemeSyntaxError
    if tokens.count("(") != tokens.count(")"):
        raise SchemeSyntaxError

    def parse_expression(index):
        try:
            if "." in tokens[index]:
                return float(tokens[index]), index + 1
            return int(tokens[index]), index + 1
        except:
            if tokens[index] != '(' and tokens[index] != ')':
                return tokens[index], index + 1

        res = []
        if tokens[index] == '(':
            index += 1
            if tokens[index] == ')':
                return res, index + 1
            elif tokens[index] == '(':
                first, index = parse_expression(index)
                return [first], index
            operator = [tokens[index]]
            res += operator
            index += 1
            try:
                next, index = parse_expression(index)
                res += [next]
            except:
                index += 1
                return operator, index

            if tokens[index] == ')':
                return operator + [next], index + 1
            while tokens[index] != ')':
                second, index = parse_expression(index)
                res += [second]

            return res, index + 1

    parsed_expression, next_index = parse_expression(0)
    return parsed_expression
    raise NotImplementedError


######################
# Built-in Functions #
######################
def mult(args):
    if len(args) == 1:
        return args[0]
    prod = 1
    for val in args:
        prod *= val
    return prod


def div(args):
    if len(args) == 1:
        return args[0]
    out = args[0]
    for i in range(1, len(args)):
        out /= args[i]
    return out


scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mult,
    "/": div,
}


##############
# Evaluation #
##############


def evaluate(tree):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if isinstance(tree, list):
        vals = []
        if not callable(evaluate(tree[0])):
            raise SchemeEvaluationError
        for val in tree:
            out = evaluate(val)
            if callable(out):
                func = out
            else:
                vals.append(out)
        return func(vals)

    elif isinstance(tree, str):
        if tree not in scheme_builtins:
            raise SchemeNameError
        else:
            return scheme_builtins[tree]
    elif isinstance(tree, (int, float)):
        return tree


########
# REPL #
########


try:
    import readline
except:
    readline = None


def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.  Not guaranteed to work in all cases, but maybe in most?
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (
        plat != "win32" or "ANSICON" in os.environ
    )
    # IDLE does not support colors
    if "idlelib" in sys.modules:
        return False
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True


class SchemeREPL(Cmd):
    """
    Class that implements a Read-Evaluate-Print Loop for our Scheme
    interpreter.
    """

    history_file = os.path.join(
        os.path.expanduser("~"), ".6101_scheme_history")

    if supports_color():
        prompt = "\033[96min>\033[0m "
        value_msg = "  out> \033[92m\033[1m%r\033[0m"
        error_msg = "  \033[91mEXCEPTION!! %s\033[0m"
    else:
        prompt = "in> "
        value_msg = "  out> %r"
        error_msg = "  EXCEPTION!! %s"

    keywords = {
        "define", "lambda", "if", "equal?", "<", "<=", ">", ">=", "and", "or",
        "del", "let", "set!", "+", "-", "*", "/", "#t", "#f", "not", "nil",
        "cons", "list", "cat", "cdr", "list-ref", "length", "append", "begin",
    }

    def __init__(self, use_frames=False, verbose=False):
        self.verbose = verbose
        self.use_frames = use_frames
        self.global_frame = None
        Cmd.__init__(self)

    def preloop(self):
        if readline and os.path.isfile(self.history_file):
            readline.read_history_file(self.history_file)

    def postloop(self):
        if readline:
            readline.set_history_length(10_000)
            readline.write_history_file(self.history_file)

    def completedefault(self, text, line, begidx, endidx):
        try:
            bound_vars = set(self.global_frame)
        except:
            bound_vars = set()
        return sorted(i for i in (self.keywords | bound_vars) if i.startswith(text))

    def onecmd(self, line):
        if line in {"EOF", "quit", "QUIT"}:
            print()
            print("bye bye!")
            return True

        elif not line.strip():
            return False

        try:
            token_list = tokenize(line)
            if self.verbose:
                print("tokens>", token_list)
            expression = parse(token_list)
            if self.verbose:
                print("expression>", expression)
            if self.use_frames:
                output, self.global_frame = result_and_frame(
                    *(
                        (expression, self.global_frame)
                        if self.global_frame is not None
                        else (expression,)
                    )
                )
            else:
                output = evaluate(expression)
            print(self.value_msg % output)
        except SchemeError as e:
            if self.verbose:
                traceback.print_tb(e.__traceback__)
                print(self.error_msg.replace("%s", "%r") % e)
            else:
                print(self.error_msg % e)

        return False

    completenames = completedefault

    def cmdloop(self, intro=None):
        while True:
            try:
                Cmd.cmdloop(self, intro=None)
                break
            except KeyboardInterrupt:
                print("^C")


if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)
    print(evaluate(['+', 3, ['-', 7, 5]]))

    SchemeREPL(use_frames=False, verbose=True).cmdloop()
