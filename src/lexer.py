from enum import Enum, auto


class TokenType(Enum):
    # Existing token types (from chapter 2)
    INTEGER = auto()
    FLOAT = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    LPAREN = auto()
    RPAREN = auto()

    # New token types (from chapter 4)
    IDENTIFIER = auto()
    LET = auto()
    FN = auto()
    IF = auto()
    ELSE = auto()
    TRUE = auto()
    FALSE = auto()
    STRING = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    EQUAL = auto()
    EQUALEQUAL = auto()
    ARROW = auto()
    PIPE = auto()
    EOF = auto()


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(
            self.text) else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(
            self.text) else None

    def peek(self):
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        dot_count = 0
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                result += '.'
            else:
                result += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TokenType.INTEGER, int(result))
        else:
            return Token(TokenType.FLOAT, float(result))

    def identifier(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token_type = {
            'let': TokenType.LET,
            'fn': TokenType.FN,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'True': TokenType.TRUE,
            'False': TokenType.FALSE,
        }.get(result, TokenType.IDENTIFIER)

        return Token(token_type, result)

    def string(self):
        result = ''
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return Token(TokenType.STRING, result)

    def let_statement(self):
        self.consume(TokenType.LET, "Expect 'let' keyword.")
        name = self.consume(TokenType.IDENTIFIER,
                            "Expect variable name.").value
        self.consume(TokenType.EQUAL, "Expect '=' after variable name.")
        value = self.expression()
        return LetNode(name, value)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                token = self.identifier()
                print(f"Generated token: {token}")  # Debug print
                return token

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '"':
                return self.string()

            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.EQUALEQUAL, '==')
                self.advance()
                return Token(TokenType.EQUAL, '=')

            if self.current_char == '-' and self.peek() == '>':
                self.advance()
                self.advance()
                return Token(TokenType.ARROW, '->')

            if self.current_char == '|':
                self.advance()
                return Token(TokenType.PIPE, '|')

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET, '[')

            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET, ']')

            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACKET, '{')

            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACKET, '}')

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',')

            raise Exception(f"Invalid character: {self.current_char}")

        token = Token(TokenType.EOF, None)
        print(f"Generated token: {token}")  # Debug print
        return token
