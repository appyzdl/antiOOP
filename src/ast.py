class ASTNode:
    pass


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value


class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value


class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value


class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name


class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryOpNode(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class LetNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class FunctionNode(ASTNode):
    def __init__(self, params, body):
        self.params = params
        self.body = body


class CallNode(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args


class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements


class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements
