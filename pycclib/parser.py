__author__ = "Grant Murphy, gcmurphy@protonmail.com"

from pycclib.ast import (
        ReturnStmt,
        String,
        Int,
        FunctionDecl,
        TypeDecl,
        Ident,
        UnaryOp,
        Operator,
        DataType

)
from pycclib.log import log

import re
from parsy import *

_whitespace = regex(r'\s*', re.MULTILINE)
_lit = lambda s: string(s) << _whitespace
_lbrace = _lit('{')
_rbrace = _lit('}')
_lparen = _lit('(')
_rparen = _lit(')')
_semi_colon = _lit(';')

_separator = (_semi_colon | _lbrace | _whitespace)
_keyword = lambda kw: _separator >> string(kw) << regex(r'\s+')
_negation = _lit('-').map(lambda op: Operator(op))
_bitwise_complement = _lit('~').map(lambda op : Operator(op))
_logical_negation = _lit('!').map(lambda op : Operator(op))
_return = _keyword('return')
_constant_int =  (regex(r'[0-9]+') << _whitespace).map(lambda x: Int(x))
_constant_str = string('"') >> regex(r'[^\0\n\"\\]').many().concat().map(lambda x: String(x)) << string('"')
_identifier = (regex(r'[a-zA-Z]\w*') << _whitespace).map(lambda x: Ident(x))
_constant = (_constant_int | _constant_str)
_operator = (_negation | _bitwise_complement | _logical_negation)
_void_type = _keyword('void').map(lambda t: DataType(t))
_int_type = _keyword('int').map(lambda t: DataType(t))
_type_decl = (_void_type | _int_type ).map(lambda x: TypeDecl(x))

@generate
def _unary_op():
    operator = yield _operator
    expr = yield _expr
    return UnaryOp(operator, expr)

_expr = _constant | _unary_op

@generate
def _return_stmt():
    yield _return
    rval = yield _expr
    return ReturnStmt(rval)

@generate
def _statement():
    val = yield _return_stmt
    yield _semi_colon
    return val

@generate
def _params():
    yield _lparen
    yield _rparen

@generate
def _block():
    yield _lbrace
    body = yield _statement.many()
    yield _rbrace
    return body

@generate
def _function_decl():
    return_type = yield _type_decl
    ident = yield _identifier
    yield _params
    body = yield _block
    return FunctionDecl(ident, return_type, [], body)

_cparser = _whitespace >> _function_decl

def parse(source):
    filecontent = source.read()
    log.debug("parsing..")
    log.debug(filecontent)
    return _cparser.parse(filecontent)

def parse_file(filename):
    with open (filename) as source_file:
        return parse_source(source_file)
