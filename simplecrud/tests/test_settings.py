import unittest

from simplecrud.settings import CRUDConfig


class TestCRUDConfig(unittest.TestCase):

    def setUp(self):
        CRUDConfig._instance = None

    def test_singleton(self):
        config1 = CRUDConfig()
        config2 = CRUDConfig()
        self.assertEqual(config1, config2)

    def test_set_sessionmaker(self):
        config = CRUDConfig()
        config.set_sessionmaker("test")
        self.assertEqual(config.sessionmaker, "test")

    def test_sessionmaker_saved_between_creation(self):
        config = CRUDConfig()
        config.set_sessionmaker("test")
        self.assertEqual(config.sessionmaker, "test")
        config = CRUDConfig()
        self.assertEqual(config.sessionmaker, "test")

    def test_sessionmaker_value_error(self):
        config = CRUDConfig()
        config._sessionmaker = None
        with self.assertRaises(ValueError):
            config.sessionmaker

    def test_sessionmaker_not_set(self):
        config = CRUDConfig()
        with self.assertRaises(AttributeError):
            config.sessionmaker
