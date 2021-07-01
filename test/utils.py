
from pycclib import compiler
from io import StringIO

def compiles(filename, code, expected=None):
    asm = StringIO()
    compiler.compile(filename, StringIO(code), asm)
    asm.seek(0)
    if not expected:
        return asm.read().strip() != None
    return asm.read().strip() == expected


