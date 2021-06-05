import unittest
from SamlClients import main


class TestSamlClients(unittest.TestCase):
    def test_main_1(self):
        self.assertEqual(main)