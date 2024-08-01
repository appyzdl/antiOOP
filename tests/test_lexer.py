from src.lexer import Lexer, TokenType


def test_lexer_keywords():
    lexer = Lexer("let fn if else True False")
    assert lexer.get_next_token().type == TokenType.LET
    assert lexer.get_next_token().type == TokenType.FN
    assert lexer.get_next_token().type == TokenType.IF
    assert lexer.get_next_token().type == TokenType.ELSE
    assert lexer.get_next_token().type == TokenType.TRUE
    assert lexer.get_next_token().type == TokenType.FALSE
    assert lexer.get_next_token().type == TokenType.EOF


def test_lexer_identifiers():
    lexer = Lexer("x y123 abc")
    assert lexer.get_next_token().type == TokenType.IDENTIFIER
    assert lexer.get_next_token().type == TokenType.IDENTIFIER
    assert lexer.get_next_token().type == TokenType.IDENTIFIER
    assert lexer.get_next_token().type == TokenType.EOF


def test_lexer_strings():
    lexer = Lexer('"Hello, World!" "Test"')
    token1 = lexer.get_next_token()
    token2 = lexer.get_next_token()
    assert token1.type == TokenType.STRING
    assert token1.value == "Hello, World!"
    assert token2.type == TokenType.STRING
    assert token2.value == "Test"
    assert lexer.get_next_token().type == TokenType.EOF


def test_lexer_operators():
    lexer = Lexer("= == -> |")
    assert lexer.get_next_token().type == TokenType.EQUAL
    assert lexer.get_next_token().type == TokenType.EQUALEQUAL
    assert lexer.get_next_token().type == TokenType.ARROW
    assert lexer.get_next_token().type == TokenType.PIPE
    assert lexer.get_next_token().type == TokenType.EOF


def test_lexer_complex_expression():
    lexer = Lexer("(1 + 2) * 3 - 4 / 5")
    tokens = [lexer.get_next_token().type for _ in range(11)
              ]  # 10 tokens + EOF
    assert tokens == [
        TokenType.LPAREN, TokenType.INTEGER, TokenType.PLUS, TokenType.INTEGER, TokenType.RPAREN,
        TokenType.MULTIPLY, TokenType.INTEGER, TokenType.MINUS, TokenType.INTEGER,
        TokenType.DIVIDE, TokenType.INTEGER
    ]

    # Add a new test for square brackets
    lexer = Lexer("[1, 2, 3]")
    tokens = [lexer.get_next_token().type for _ in range(8)]  # 7 tokens + EOF
    assert tokens == [
        TokenType.LBRACKET, TokenType.INTEGER, TokenType.COMMA, TokenType.INTEGER,
        TokenType.COMMA, TokenType.INTEGER, TokenType.RBRACKET, TokenType.EOF
    ]


def test_lexer_function_definition():
    lexer = Lexer('let add = fn(a, b) { a + b }')
    expected_tokens = [
        (TokenType.LET, 'let'),
        (TokenType.IDENTIFIER, 'add'),
        (TokenType.EQUAL, '='),
        (TokenType.FN, 'fn'),
        (TokenType.LPAREN, '('),
        (TokenType.IDENTIFIER, 'a'),
        (TokenType.COMMA, ','),
        (TokenType.IDENTIFIER, 'b'),
        (TokenType.RPAREN, ')'),
        (TokenType.LBRACKET, '{'),
        (TokenType.IDENTIFIER, 'a'),
        (TokenType.PLUS, '+'),
        (TokenType.IDENTIFIER, 'b'),
        (TokenType.RBRACKET, '}'),
        (TokenType.EOF, None)
    ]

    for expected_type, expected_value in expected_tokens:
        token = lexer.get_next_token()
        assert token.type == expected_type, f"Expected {expected_type}, but got {token.type}"
        assert token.value == expected_value, f"Expected value '{expected_value}', but got '{token.value}'"

    # Ensure we've reached the end of the input
    assert lexer.get_next_token().type == TokenType.EOF
