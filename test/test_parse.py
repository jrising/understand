import unittest
from parse import interpret

class TestInterpret(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(interpret.guess("1+1")[0], 'calc4')
        self.assertEqual(interpret.guess("sqrt(3)")[0], 'math')
        self.assertEqual(interpret.guess("ls *")[0], 'bash')
        self.assertEqual(interpret.guess("{'test': 3}")[0], 'python')
        self.assertEqual(interpret.guess('{"test": 3}')[0], 'json')
        self.assertEqual(interpret.guess('yes,no\n3,5')[0], 'csv')

if __name__ == '__main__':
    unittest.main()

