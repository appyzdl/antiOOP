from src.lexer import Lexer, TokenType
from src.parser import Parser
from src.interpreter import Interpreter

interpreter = Interpreter()


def run(code):
    lexer = Lexer(code)
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.EOF:
            break
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"AST: {ast}")
    result = interpreter.interpret(ast)
    print(f"Result: {result}")
    return result


def test_arithmetic():
    assert run("1 + 2 * 3") == 7
    assert run("(1 + 2) * 3") == 9


def test_variables():
    interpreter = Interpreter()
    assert run("let x = 5") == 5
    assert run("x") == 5



def test_functions():
    interpreter = Interpreter()
    run("let add = fn(a, b) { a + b }")
    assert run("add(3, 4)") == 7


def test_if_statement():
    assert run("if True { 1 } else { 2 }") == 1
    assert run("if False { 1 } else { 2 }") == 2


def test_lists():
    assert run("[1, 2, 3]") == [1, 2, 3]


def test_complex_program():
    program = """
    let fibonacci = fn(n) {
        if n == 0 { 0 }
        else {
            if n == 1 { 1 }
            else { fibonacci(n - 1) + fibonacci(n - 2) }
        }
    }
    fibonacci(10)
    """
    assert run(program) == 55
