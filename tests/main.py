import io
import sys

from language.compiler import main

class TestMain:
    def set_up(self):
        self.saved_argv = sys.argv
        self.saved_stdin = sys.stdin
        self.saved_stdout = sys.stdout
        sys.stdin = open('keywords.language')
        sys.stdout = io.StringIO()

    def tear_down(self):
        sys.stdout.close()
        sys.stdin.close()
        sys.stdout = self.saved_stdout
        sys.stdin = self.saved_stdin
        sys.argv = self.saved_argv

    def test_run_compiler(self):
        sys.argv = ['language', 'keywords.language']
        main()
        with open('demo.py') as file:
            assert file.read().startswith(
                'from language.semantics import *'
            )

    def test_main(self):
        sys.argv = ['language', '--help']
        main()
        assert sys.stdout.getvalue().startswith(
            'Type "language" to run the interpreter.\n'
            'Type "language <filename>" to compile <filename>.\n'
        )
