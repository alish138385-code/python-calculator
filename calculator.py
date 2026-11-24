ALLOWED_CHARACTERS = "0123456789+-*/(). "


def calculate(expression):
    """Calculate the expression and return the result."""

    for character in expression:
        if character not in ALLOWED_CHARACTERS:
            raise ValueError("Only numbers and + - * / ( ) are allowed.")

    if "**" in expression:
        raise ValueError("Power (**) is not supported.")

    try:
        result = eval(expression)
        return round(result, 10)
    except ZeroDivisionError:
        raise ValueError("You can't divide by zero.")
    except (SyntaxError, TypeError):
        raise ValueError("Invalid expression. Example: (2 + 3) / 4")


def main():
    print("Calculator")
    print("Type any expression and press Enter, example: (2 + 3) / 4 * 10")
    print("Type q to quit.")

    while True:
        expression = input("\n> ").strip()

        if expression == "q":
            print("Goodbye!")
            break

        if expression == "":
            continue

        try:
            result = calculate(expression)
            print("=", result)
        except ValueError as error:
            print("Error:", error)


main()