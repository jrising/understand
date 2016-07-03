import unittest
import logic, simple, oeis

class TestLogic(unittest.TestCase):
    def test_simple(self):
        env = logic.understand("logic.py")
        self.assertTrue(env.frame[simple.types.IsLocalFilePath])
        env = logic.understand("3.14159")
        self.assertEqual(env.frame['numeric'], 3.14159)
        env = logic.understand("1,2,3,6,11,23,47,106,235")
        seqid = '%I A000055 M0791 N0299'
        self.assertEqual(env.frame[oeis.IntegerSequenceEncyclopedia][0][0:len(seqid)], seqid)

if __name__ == '__main__':
    unittest.main()

