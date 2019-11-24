class ExprNode(object):

    def evaluate(self):
        pass

    def accept(self, node):
        pass


class BinaryOperationNode(ExprNode):

    def __init__(self, op):
        super().__init__()
        self.operator   = op     # the lexeme of the operator
        self.left_expr  = None   # the left-hand-side expression
        self.right_expr = None   # the right-hand-side expression

    def evaluate(self):
        return eval(self.left_expr + self.operator + self.right_expr)


class IntLiteralNode(ExprNode):

    def __init__(self, num):
        super().__init__()
        self.int_val = num

    def evaluate(self):
        return int(self.int_val)


class FloatLiteralNode(ExprNode):

    def __init__(self, num):
        super().__init__()
        self.float_val = num

    def evaluate(self):
        return float(self.float_val)


class IdLiteralNode(ExprNode):

    def __init__(self, id):
        super().__init__()
        self.id_val = id

    def evaluate(self):
        return str(self.id_val)