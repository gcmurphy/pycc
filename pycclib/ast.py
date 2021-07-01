__author__ = "Grant Murphy, gcmurphy@protonmail.com"

import enum
from pycclib.log import log


class ASTNode(object):
    def __init__(self):
        self.tags = {}

    def name(self):
        return self.__class__.__name__

    def tag(self, tag):
        self.tags.add(tag)

    def __repr__(self):
        return self.name()

class Stmt(ASTNode):
    pass

class ReturnStmt(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return (self.name() + ": " + str(self.expr))

class Expr(Stmt):
    pass

class Constant(Expr):
    def __init__(self):
        self.value = None

    def __repr__(self):
        return (self.name() + ": " + str(self.value))


class Int(Constant):
    def __init__(self, integer):
        self.value = int(integer)

class String(Constant):
    def __init__(self, string):
        self.value = string


class Operator(enum.Enum):
    NEGATION = '-'
    LOGICAL_NEGATION = '!'
    BITWISE_COMPLIMENT = '~'

class UnaryOp(Expr):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Ident(ASTNode):
    def __init__(self, name):
        self.ident = name

    def __repr__(self):
        return (self.name() + ": " + str(self.ident))


class Decl(ASTNode):
    pass

class DataType(enum.Enum):
    VOID = 'void'
    INT = 'int'
    FLOAT = 'float'
    DOUBLE = 'double'
    CHAR = 'char'

class TypeDecl(Decl):
    def __init__(self, tval):
        self.declared_type = tval

    def __repr__(self):
        return (self.name() + ": " + str(self.declared_type))

class FunctionDecl(Decl):
    def __init__(self, ident, ret, params, statements):
        self.ident = ident
        self.ret = ret
        self.params = params
        self.statements = statements

    def __repr__(self):
        return (self.name() + ": " +
            ", ".join([str(self.ret),
                       str(self.ident),
                       str(self.params),
                       str(self.statements)]))


class ASTVisitor(object):
    def __init__(self):
        self.called = False

    def visit(self, node):
        if not self.called:
            log.debug("walking ast...")
            self.called = True

        name = "visit_{}".format(node.__class__.__name__)
        if hasattr(self, name):
            visitor = getattr(self, name)
            log.debug(name)
            visitor(node)
        else:
            this = self.__class__.__name__
            err = "{} missing {}() required for {}".format(this, name, node)
            raise NotImplementedError(err)
