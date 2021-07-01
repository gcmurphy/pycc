import sys
import unittest
from io import StringIO

from test.utils import compiles
from pycclib import compiler


class TestStage2(unittest.TestCase):

    def _check_invalid(self, name, code):
        source = StringIO(code)
        asm = StringIO()
        with self.assertRaises(Exception):
            compiler.compile(name, code, asm)

    def test_bitwise(self):
        self.assertTrue(compiles("bitwise.c",
                        "int main(){ return ~12;}"))


    def test_negation(self):
        self.assertTrue(compiles("negation.c",
                        "int main(){ return -5;}"))


    def test_logical_not(self):
        self.assertTrue(compiles("not.c",
                        "int main(){ return !0;}"))

    def test_nested(self):
        self.assertTrue(compiles("nested.c",
                        "int main(){ return !~0;}"))

    def test_missing_const(self):
        self._check_invalid("missing_const.c",
                            "int main(){ return !; }")
        self._check_invalid("missing_const_nested.c",
                            "int main(){ return !~;}")

    def test_missing_const(self):
        self._check_invalid("missing_const.c",
                            "int main(){ return !; }")
        self._check_invalid("missing_const_nested.c",
                            "int main(){ return !~;}")

    def test_wrong_order(self):
        self._check_invalid("wrong_order.c",
                            "int main(){ return 4-; }")

    def test_missing_semi(self):
        self._check_invalid("missing_semi.c",
                            "int main(){ return !5}")

    

if __name__ == "__main__":
    unittest.main()
