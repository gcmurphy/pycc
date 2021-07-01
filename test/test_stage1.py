import sys
import unittest
from io import StringIO
from pycclib import compiler
from test.utils import compiles

stage1 = """
.globl _main
_main:
	movl	$0, %eax
	ret
""".strip()



class TestStage1(unittest.TestCase):


    def test_parser_newlines(self):
        code = "int main () { return 0 ; }".replace(" ", "\n")
        self.assertTrue(compiles("newlines.c", code, stage1))

    def test_parser_single_line(self):
        self.assertTrue(compiles("single_line.c",
            "int main(){ return 0; }", stage1))

    def test_parser_bad_return(self):
        source = StringIO("int main(){ return0 ;}")
        asm = StringIO()
        with self.assertRaises(Exception):
            compiler.compile("bad_return.c", source, asm)

    def test_parser_no_brace(self):
        source = StringIO("int main(){ return 0;")
        asm = StringIO()
        with self.assertRaises(Exception):
            compiler.compile("no_brace.c", source, asm)

    def test_parser_missing_paren(self):
        source = StringIO("int main( {return 0;}")
        asm = StringIO()
        with self.assertRaises(Exception):
            compiler.compile("missing_paren.c", source, asm)

    def test_parser_missing_semi(self):
        source = StringIO("int main(){ return 0 }")
        asm = StringIO()
        with self.assertRaises(Exception):
            compiler.compile("missing_semi.c", source, asm)

    def test_parser_wrong_case(self):
        source = StringIO("int main(){ RETURN 0; }")
        asm = StringIO()
        with self.assertRaises(Exception):
            compiler.compile("wrong_case.c", source, asm)


if __name__ == "__main__":
    unittest.main()
