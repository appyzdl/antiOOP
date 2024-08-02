from src.lexer import TokenType
from src.ast import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.current_token = self.tokens[self.current] if self.tokens else None

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        program = ProgramNode(statements)
        print(f"Parsed program: {program}")  # Print the parsed program
        return program

    def statement(self):
        if self.match(TokenType.LET):
            return self.let_statement()
        return self.expression()

    def let_statement(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        self.consume(TokenType.EQUAL, "Expect '=' after variable name.")
        value = self.expression()
        return LetNode(name.value, value)

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.addition()
        while self.match(TokenType.EQUALEQUAL):
            operator = self.previous()
            right = self.addition()
            expr = BinaryOpNode(expr, operator.type, right)
        return expr

    def addition(self):
        expr = self.multiplication()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.multiplication()
            expr = BinaryOpNode(expr, operator.type, right)
        return expr

    def multiplication(self):
        expr = self.unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.previous()
            right = self.unary()
            expr = BinaryOpNode(expr, operator.type, right)
        return expr

    def unary(self):
        if self.match(TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return UnaryOpNode(operator.type, right)
        return self.primary()

    def primary(self):
        # Debug print
        print(f"Entering primary, current token: {self.current_token}")
        if self.match(TokenType.FALSE):
            return BooleanNode(False)
        if self.match(TokenType.TRUE):
            return BooleanNode(True)
        if self.match(TokenType.INTEGER, TokenType.FLOAT):
            return NumberNode(self.previous().value)
        if self.match(TokenType.STRING):
            return StringNode(self.previous().value)
        if self.match(TokenType.IDENTIFIER):
            name = self.previous()
            if self.match(TokenType.LPAREN):
                arguments = []
                if not self.check(TokenType.RPAREN):
                    arguments.append(self.expression())
                    while self.match(TokenType.COMMA):
                        arguments.append(self.expression())
                self.consume(TokenType.RPAREN, "Expect ')' after arguments.")
                return CallNode(IdentifierNode(name.value), arguments)
            return IdentifierNode(name.value)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
            return expr
        if self.match(TokenType.FN):
            return self.function()
        if self.check(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.LBRACKET):
            return self.list()

        raise Exception(f"Unexpected token: {self.peek()}")

    def function(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'fn'.")
        parameters = []
        if not self.check(TokenType.RPAREN):
            parameters.append(self.consume(
                TokenType.IDENTIFIER, "Expect parameter name.").value)
            while self.match(TokenType.COMMA):
                parameters.append(self.consume(
                    TokenType.IDENTIFIER, "Expect parameter name.").value)
        self.consume(TokenType.RPAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LBRACKET, "Expect '{' before function body.")
        body = self.block()
        return FunctionNode(parameters, body)

    def if_statement(self):
        # Debug print
        print(f"Entering if_statement, current token: {self.current_token}")
        self.consume(TokenType.IF, "Expect 'if' keyword.")
        condition = self.expression()
        self.consume(TokenType.LBRACKET, "Expect '{' before if branch.")
        then_branch = self.block()
        else_branch = None
        if self.match(TokenType.ELSE):
            self.consume(TokenType.LBRACKET, "Expect '{' before else branch.")
            else_branch = self.block()
        return IfNode(condition, then_branch, else_branch)

    def block(self):
        statements = []
        self.consume(TokenType.LBRACKET, "Expect '{' before block.")
        while not self.check(TokenType.RBRACKET) and not self.is_at_end():
            statements.append(self.statement())
        self.consume(TokenType.RBRACKET, "Expect '}' after block.")
        return BlockNode(statements)

    def list(self):
        elements = []
        if not self.check(TokenType.RBRACKET):
            elements.append(self.expression())
            while self.match(TokenType.COMMA):
                elements.append(self.expression())
        self.consume(TokenType.RBRACKET, "Expect ']' after list elements.")
        return ListNode(elements)

    def block(self):
        statements = []
        while not self.check(TokenType.RBRACKET) and not self.is_at_end():
            statements.append(self.statement())
        self.consume(TokenType.RBRACKET, "Expect '}' after block.")
        return statements

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.is_at_end():
            return False
        return self.current_token.type == type

    def advance(self):
        self.current += 1
        if not self.is_at_end():
            self.current_token = self.tokens[self.current]
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.current_token

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise Exception(f"{message}. Got {self.current_token} instead.")
