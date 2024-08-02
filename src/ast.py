class ASTNode:
    def accept(self, visitor):
        method_name = f'visit_{type(self).__name__.lower()}'
        visit_method = getattr(visitor, method_name)
        return visit_method(self)


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

    def __str__(self):
        return f"LetNode(name={self.name}, value={self.value})"


class FunctionNode(ASTNode):
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def __str__(self):
        return f"FunctionNode(params={self.params}, body={self.body})"


class CallNode(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args


class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return f"BlockNode(statements={self.statements})"


class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __str__(self):
        return f"IfNode(condition={self.condition}, then={self.then_branch}, else={self.else_branch})"


class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements


class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements
 # type: ignore
