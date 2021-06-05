import unittest
from mysum import sumFunc


class TestSamlClients(unittest.TestCase):
    def test_main_1(self):
        self.assertEqual(5,sumFunc(2,3))
    # def test_main_2(self):
    #     self.assertEqual(sumFunc(3,4),7)
    # def test_main_3(self):
    #     self.assertEqual(sumFunc(4,6),10)

if __name__ == '__main__':
    unittest.main()