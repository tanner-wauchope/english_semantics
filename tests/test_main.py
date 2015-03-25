import io
import sys
from unittest import TestCase

from __main__ import package_name, main

class TestMain(TestCase):
    def setUp(self):
        self.saved_stdin = sys.stdin
        self.saved_stdout = sys.stdout
        sys.stdin = open('keywords.english')
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdin.close()
        sys.stdout.close()
        sys.stdin = self.saved_stdin
        sys.stdout = self.saved_stdout

    def test_run_interpreter(self):
        main()
        self.assertEqual(
            sys.stdout.getvalue(),
            package_name + '\n'
            '>>> \n'
            '... \n'
        )

    def test_run_compiler(self):
        main('keywords.english')
        self.assertEqual(
            sys.stdout.getvalue(),
            'Compilation succeeded.\n'
        )
        with open('demo.py') as file:
            self.assert_equal(
                file.read(),
                '# ' + package_name + '\n'
                'from plain_english.semantics import *\n'
                'exit()'
            )

    def test_main(self):
        main('keywords.english', 'keywords.english')
        self.assertEqual(
            sys.stdout.getvalue(),
            'Provide no arguments to run the interpreter.\n'
            'Provide a file path to run the compiler.\n'
        )
