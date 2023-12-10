import unittest

from simplecrud.settings import CRUDConfig


class TestCRUDConfig(unittest.TestCase):
    def test_singleton(self):
        config1 = CRUDConfig()
        config2 = CRUDConfig()
        self.assertEqual(config1, config2)

    def test_set_sessionmaker(self):
        config = CRUDConfig()
        config.set_sessionmaker("test")
        self.assertEqual(config.sessionmaker, "test")

    def test_get_sessionmaker(self):
        config = CRUDConfig()
        with self.assertRaises(ValueError):
            config.sessionmaker
