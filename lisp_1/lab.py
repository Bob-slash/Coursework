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


class Frame:
    def __init__(self, parent=None):
        # self.variables = {}
        # self.functions = {}
        self.functions_and_variables = {}
        self.parent = parent

    def find(self, var):
        if var in self.functions_and_variables:
            return self.functions_and_variables[var]
        if self.parent == None:
            return None
        return self.parent.find(var)

    def find_var(self, var):
        if var in self.variables:
            return self.variables[var]
        if self.parent == None:
            raise SchemeNameError("we can't find your var")
        return self.parent.find_var(var)

    def find_func(self, func):
        if func in self.functions:
            return self.functions[func]
        if self.parent == None:
            raise SchemeEvaluationError
        return self.parent.find_func(func)

    def set_functions(self, functions):
        self.functions_and_variables = functions.copy()

    def add_functions(self, name, func):
        self.functions_and_variables[name] = func

    def define(self, name, value):
        # if isinstance(value, (int, float)):
        #     self.variables[name] = value
        # elif callable(value):
        #     self.functions[name] = value
        self.functions_and_variables[name] = value
        return value


class userFunc:
    def __init__(self, parameters, body, frame):
        self.parameters = parameters
        self.body = body
        self.enclosing_frame = frame

    def __call__(self, parameters):
        if len(parameters) != len(self.parameters):
            print("pass")
            raise SchemeEvaluationError

        new_frame = Frame(self.enclosing_frame)
        for i in range(len(self.parameters)):
            new_frame.define(self.parameters[i], parameters[i])

        # all_funcs = self.enclosing_frame.functions.items()
        # name = None
        # for tup in all_funcs:
        #     if tup[1] == self:
        #         name = tup[0]
        # new_frame.add_functions(name, userFunc(
        #     evaled_params, self.body, self.enclosing_frame))

        return evaluate(self.body, new_frame)


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
        if "\n" in substr:
            e_index = substr.index("\n") + s_index + 1
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
                        tokens.append(chunk[i - length: i])
                        length = 0
                    tokens.append(chunk[i])
                else:
                    length += 1
        elif "(" in chunk:
            index = chunk.index("(")
            if index == 0:
                tokens.append("(")
                tokens.extend(parenthesis_check(chunk[1:]))
            elif index == len(chunk) - 1:
                tokens.extend(parenthesis_check(chunk[0:-1]))
                tokens.append("(")
            else:
                tokens.extend(parenthesis_check(chunk[0:index]))
                tokens.append("(")
                tokens.extend(parenthesis_check(chunk[index + 1:]))
        elif ")" in chunk:
            index = chunk.index(")")
            if index == 0:
                tokens.append(")")
                tokens.extend(parenthesis_check(chunk[1:]))
            elif index == len(chunk) - 1:
                tokens.extend(parenthesis_check(chunk[0:-1]))
                tokens.append(")")
            else:
                tokens.extend(parenthesis_check(chunk[0:index]))
                tokens.append(")")
                tokens.extend(parenthesis_check(chunk[index + 1:]))

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

        if tokens[index] == '(':
            res = []
            index += 1
            while tokens[index] != ')':
                next, index = parse_expression(index)
                res.append(next)
            return res, index + 1

    parsed_expression, next_index = parse_expression(0)
    return parsed_expression


######################
# Built-in Functions #
######################
def emptyFrame():
    parent = Frame()
    parent.set_functions(scheme_builtins)
    return Frame(parent)


def mult(args):
    """
    multiplies all values in list args
    """
    if len(args) == 1:
        return args[0]
    prod = 1
    for val in args:
        if callable(val):
            print("body ", val.body)
        prod *= val
    return prod


def div(args):
    """
    Divides first value in list args by the rest of the values
    """
    if len(args) == 1:
        return args[0]
    out = args[0]
    for i in range(1, len(args)):
        out /= args[i]
    return out


def define(frame, name, var):
    frame.define(name, var)


def lam(parameters, body, frame):
    return userFunc(parameters, body, frame)


scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mult,
    "/": div,
    "define": define,
    "lambda": lam,
}


##############
# Evaluation #
##############


def evaluate(tree, frame=None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if frame is None:
        frame = emptyFrame()
    if isinstance(tree, list):
        print("tree ", tree)
        vals = []
        if isinstance(tree[0], list):
            operation = evaluate(tree[0], frame)
        else:
            operation = frame.find(tree[0])

        if operation is None:
            raise SchemeEvaluationError

        if tree[0] == "define":
            if isinstance(tree[1], list) and isinstance(tree[2], list):
                redefine = ["define", tree[1][0], [
                    "lambda", tree[1][1:], tree[2]]]
                return evaluate(redefine, frame)
            return frame.define(tree[1], evaluate(tree[2], frame))

        elif tree[0] == "lambda":
            params = tree[1].copy()
            body = tree[2]
            return userFunc(params, body, frame)

        for val in tree[1:]:
            print("in", val)
            out = evaluate(val, frame)
            print("out ", out)
            vals.append(out)

        return operation(vals)

    elif isinstance(tree, str):
        found = frame.find(tree)
        if found is None:
            raise SchemeNameError
        return found

    elif isinstance(tree, (int, float)):
        return tree


def result_and_frame(tree, frame=None):
    if frame is None:
        frame = emptyFrame()
    return evaluate(tree, frame), frame


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
        "define",
        "lambda",
        "if",
        "equal?",
        "<",
        "<=",
        ">",
        ">=",
        "and",
        "or",
        "del",
        "let",
        "set!",
        "+",
        "-",
        "*",
        "/",
        "#t",
        "#f",
        "not",
        "nil",
        "cons",
        "list",
        "cat",
        "cdr",
        "list-ref",
        "length",
        "append",
        "begin",
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
                ("^C")


if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # print(evaluate(['dosomething', 2, 3, 4]))

    SchemeREPL(use_frames=True, verbose=True).cmdloop()
