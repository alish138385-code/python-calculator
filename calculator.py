"""A simple command-line calculator.

Supports + - * / // % ** , parentheses, a few math functions (sqrt, sin, ...),
the constants pi and e, and `ans` (the previous result).

Expressions are parsed with the `ast` module instead of `eval()`, so
arbitrary Python code can never be executed through the input.
"""

import ast
import math
import operator

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}

MAX_EXPONENT = 1000  # prevents things like 9**9**9 from freezing the program


class CalculatorError(Exception):
    """Raised when an expression is invalid or cannot be calculated."""


def _eval_node(node, variables):
    """Recursively evaluate a node of the parsed expression tree."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, variables)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise CalculatorError(f"Unsupported value: {node.value!r}")

    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise CalculatorError(f"Unknown name: {node.id}")

    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPERATORS:
        operand = _eval_node(node.operand, variables)
        return UNARY_OPERATORS[type(node.op)](operand)

    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPERATORS:
        left = _eval_node(node.left, variables)
        right = _eval_node(node.right, variables)
        if isinstance(node.op, ast.Pow) and abs(right) > MAX_EXPONENT:
            raise CalculatorError("Exponent is too large")
        return BINARY_OPERATORS[type(node.op)](left, right)

    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in FUNCTIONS
        and not node.keywords
    ):
        args = [_eval_node(arg, variables) for arg in node.args]
        return FUNCTIONS[node.func.id](*args)

    raise CalculatorError("Unsupported expression")


def evaluate(expression, ans=0):
    """Evaluate a math expression string and return the result.

    >>> evaluate("2 + 3 * 4")
    14
    >>> evaluate("sqrt(16) + 1")
    5.0
    """
    variables = {**CONSTANTS, "ans": ans}
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        return _eval_node(tree, variables)
    except SyntaxError:
        raise CalculatorError("Invalid syntax") from None
    except ZeroDivisionError:
        raise CalculatorError("Division by zero") from None
    except OverflowError:
        raise CalculatorError("Result is too large") from None
    except (ValueError, TypeError) as error:
        raise CalculatorError(f"Math error: {error}") from None


def format_result(value):
    """Show 2.0 as 2 and trim floating point noise (0.1 + 0.2 -> 0.3)."""
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def main():
    print("Python Calculator")
    print("Examples: 2 + 3 * 4, (1 + 2) ** 3, sqrt(16), ans * 2")
    print("Type 'q' to quit.\n")

    ans = 0
    while True:
        try:
            expression = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if expression.lower() in {"q", "quit", "exit"}:
            break
        if not expression:
            continue

        try:
            ans = evaluate(expression, ans)
        except CalculatorError as error:
            print(f"Error: {error}")
        else:
            print(format_result(ans))


if __name__ == "__main__":
    main()
