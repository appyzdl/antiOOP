from src.lexer import Lexer, TokenType


def test_lexer_integers():
    lexer = Lexer("123 456")
    assert lexer.get_next_token().type == TokenType.INTEGER
    assert lexer.get_next_token().type == TokenType.INTEGER
    assert lexer.get_next_token().type == TokenType.EOF


def test_lexer_operators():
    lexer = Lexer("+ - * /")
    assert lexer.get_next_token().type == TokenType.PLUS
    assert lexer.get_next_token().type == TokenType.MINUS
    assert lexer.get_next_token().type == TokenType.MULTIPLY
    assert lexer.get_next_token().type == TokenType.DIVIDE
    assert lexer.get_next_token().type == TokenType.EOF


def test_lexer_parentheses():
    lexer = Lexer("()")
    assert lexer.get_next_token().type == TokenType.LPAREN
    assert lexer.get_next_token().type == TokenType.RPAREN
    assert lexer.get_next_token().type == TokenType.EOF


def test_lexer_complex_expression():
    lexer = Lexer("(1 + 2) * 3 - 4 / 25")
    tokens = [lexer.get_next_token().type for _ in range(11)
              ]  # 10 tokens + EOF
    assert tokens == [
        TokenType.LPAREN, TokenType.INTEGER, TokenType.PLUS, TokenType.INTEGER, TokenType.RPAREN,
        TokenType.MULTIPLY, TokenType.INTEGER, TokenType.MINUS, TokenType.INTEGER,
        TokenType.DIVIDE, TokenType.INTEGER
    ]
