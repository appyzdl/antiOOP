from src.lexer import Lexer, TokenType
from src.parser import Parser
from src.ast import *


def parse(text):
    lexer = Lexer(text)
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == TokenType.EOF:
            break
    parser = Parser(tokens)
    return parser.parse()


def test_number():
    ast = parse("42")
    assert isinstance(ast.statements[0], NumberNode)
    assert ast.statements[0].value == 42


def test_string():
    ast = parse('"Hello, World!"')
    assert isinstance(ast.statements[0], StringNode)
    assert ast.statements[0].value == "Hello, World!"


def test_boolean():
    ast = parse("True")
    assert isinstance(ast.statements[0], BooleanNode)
    assert ast.statements[0].value == True


def test_let_statement():
    ast = parse("let x = 5")
    assert isinstance(ast.statements[0], LetNode)
    assert ast.statements[0].name == "x"
    assert isinstance(ast.statements[0].value, NumberNode)
    assert ast.statements[0].value.value == 5


def test_binary_operation():
    ast = parse("1 + 2 * 3")
    assert isinstance(ast.statements[0], BinaryOpNode)
    assert ast.statements[0].op == TokenType.PLUS
    assert isinstance(ast.statements[0].left, NumberNode)
    assert ast.statements[0].left.value == 1
    assert isinstance(ast.statements[0].right, BinaryOpNode)
    assert ast.statements[0].right.op == TokenType.MULTIPLY


def test_function_definition():
    ast = parse("fn(x, y) { x + y }")
    assert isinstance(ast.statements[0], FunctionNode)
    assert ast.statements[0].params == ["x", "y"]
    assert len(ast.statements[0].body) == 1
    assert isinstance(ast.statements[0].body[0], BinaryOpNode)


def test_if_statement():
    ast = parse("if x == 5 { 1 } else { 2 }")
    assert isinstance(ast.statements[0], IfNode)
    assert isinstance(ast.statements[0].condition, BinaryOpNode)
    assert isinstance(ast.statements[0].then_branch[0], NumberNode)
    assert isinstance(ast.statements[0].else_branch[0], NumberNode)


def test_list():
    ast = parse("[1, 2, 3]")
    assert isinstance(ast.statements[0], ListNode)
    assert len(ast.statements[0].elements) == 3
    assert all(isinstance(el, NumberNode) for el in ast.statements[0].elements)
