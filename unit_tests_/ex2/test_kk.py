import unittest
from kk import aa,bb,cc

class Test_kk(unittest.TestCase):

    def setUp(self):
        print('\nkk go!!')

    def test_aa(self):
        self.assertEqual(aa(5,6),11)

    def test_bb(self):
        self.assertEqual(bb(5,6),30)

    def test_cc(self):
        # self.assertEqual(cc(1,2),3)
        self.assertEqual(cc(1,'g'),0)

    def tearDown(self):
        print('\nkk end!!')

if __name__ == '__main__':
    unittest.main()