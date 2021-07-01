__author__ = "Grant Murphy, gcmurphy@protonmail.com"

import os
from pycclib import parser, codegen
from pycclib.log import log

def assembly_file(filename):
    path, _ = os.path.splitext(filename)
    path += '.s'
    return path

def compile(filename, source, dest):
    log.debug("compiling %s..", filename)
    astnode = parser.parse(source)
    codegen.generate(dest, astnode)
