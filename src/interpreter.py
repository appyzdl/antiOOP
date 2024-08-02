from .lexer import TokenType
from src.ast import *
from src.environment import Environment


class Interpreter:
    def __init__(self):
        self.global_env = Environment()

    def interpret(self, program):
        result = None
        for statement in program.statements:
            print(f"Executing statement: {statement}")  # Print each statement
            result = self.execute(statement)
        print(f"Final result: {result}")  # Print the final result
        return result

    def execute(self, stmt):
        if isinstance(stmt, list):
            result = None
            for s in stmt:
                result = self.execute(s)
            return result
        else:
            print(f"Executing: {stmt}")  # Print the statement being executed
            return stmt.accept(self)

    def evaluate(self, expr):
        print(f"Evaluating: {expr}")  # Print the expression being evaluated
        return expr.accept(self)

    def visit_programnode(self, node):
        value = self.evaluate(node.value)
        self.global_env.define(node.name, value)
        return value  # Return the value of the variable

    def visit_numbernode(self, node):
        return node.value

    def visit_stringnode(self, node):
        return node.value

    def visit_booleannode(self, node):
        return node.value

    def visit_identifiernode(self, node):
        return self.global_env.get(node.name)

    def visit_binaryopnode(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.op == TokenType.PLUS:
            return left + right
        elif node.op == TokenType.MINUS:
            return left - right
        elif node.op == TokenType.MULTIPLY:
            return left * right
        elif node.op == TokenType.DIVIDE:
            return left / right
        elif node.op == TokenType.EQUALEQUAL:
            return left == right

    def visit_unaryopnode(self, node):
        right = self.evaluate(node.expr)

        if node.op == TokenType.MINUS:
            return -right

    def visit_letnode(self, node):
        print(f"Visiting LetNode: {node}")  # Print the LetNode
        value = self.evaluate(node.value)
        self.global_env.define(node.name, value)
        return value

    def visit_functionnode(self, node):
        return Function(node, self.global_env)

    def visit_callnode(self, node):
        callee = self.evaluate(node.func)
        arguments = [self.evaluate(arg) for arg in node.args]

        if not isinstance(callee, Function):
            raise Exception("Can only call functions.")

        if len(arguments) != len(callee.declaration.params):
            raise Exception(
                f"Expected {len(callee.declaration.params)} arguments but got {len(arguments)}.")

        return callee.call(self, arguments)

    def visit_blocknode(self, node):
        result = None
        for statement in node.statements:
            result = self.execute(statement)
        return result

    def visit_ifnode(self, node):
        if self.evaluate(node.condition):
            return self.execute(node.then_branch)
        elif node.else_branch:
            return self.execute(node.else_branch)
        return None

    def visit_listnode(self, node):
        return [self.evaluate(element) for element in node.elements]


class Function:
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for param, arg in zip(self.declaration.params, arguments):
            environment.define(param, arg)

        previous_env = interpreter.global_env
        interpreter.global_env = environment

        result = None
        for statement in self.declaration.body:
            result = interpreter.execute(statement)

        interpreter.global_env = previous_env
        return result


class Return(Exception):
    def __init__(self, value):
        self.value = value
