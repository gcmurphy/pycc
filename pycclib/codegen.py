__author__ = "Grant Murphy, gcmurphy@protonmail.com"

from pycclib.ast import ASTVisitor, Int, String, Operator
from pycclib.log import log


class CodeGenerator(ASTVisitor):

    def __init__(self, target):
        super().__init__()
        self.target = target

    def emit(self, asm):
        self.target.write(asm)
        self.target.write('\n')

    def emit_code(self, opcode, value=None):
        self.target.write('\t')
        self.target.write(opcode)
        if value:
            self.target.write('\t')
            self.target.write(value)
        self.target.write('\n')

    def visit_Int(self, node):
        self.emit_code('movl', '${}, %eax'.format(node.value))

    def visit_UnaryOp(self, node):
        self.visit(node.expr)
        if node.op == Operator.NEGATION:
            self.emit_code("neg", "%eax")
        elif node.op == Operator.BITWISE_COMPLIMENT:
            self.emit_code("not", "%eax")
        elif node.op == Operator.LOGICAL_NEGATION:
            self.emit_code("cmpl", "$0, %eax")
            self.emit_code("movl", "$0, %eax")
            self.emit_code("sete", "%al")
        else:
            raise NotImplementedError("Unsupported unary operator: " + node.op)

    def visit_FunctionDecl(self, node):
        self.emit('.globl _' + node.ident.ident)
        self.emit('_' + node.ident.ident + ':')
        for statement in node.statements:
            self.visit(statement)

    def visit_ReturnStmt(self, node):
        if node.expr:
            self.visit(node.expr)
        self.emit_code('ret')


def generate(fileobj, root):
    cgen = CodeGenerator(fileobj)
    cgen.visit(root)
