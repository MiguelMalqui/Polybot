import unittest
from antlr4 import *
from polybot.cl import *


class TestEvalVisitor(unittest.TestCase):

    def test_eval_visitor(self):
        input_stream = FileStream('language_test_files/example_input.txt')
        lexer = LanguageLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = LanguageParser(token_stream)
        tree = parser.root()
        visitor = EvalVisitor()
        output, _ = visitor.visit(tree)
        file = open("language_test_files/example_output.txt")
        expected_output = file.read()
        file.close()
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
