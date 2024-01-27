import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from simplecrud import CRUDConfig
from simplecrud.tests.test_crud import engine, Base
from simplecrud.utils import inject_connection

database_url = "sqlite:///./test.db"
engine = create_engine(database_url)
session_maker = sessionmaker(bind=engine)


class TestAsyncCRUDFunctions(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)
        CRUDConfig().set_sessionmaker(session_maker)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_inject_connection(self):
        def example_func(conn=None):
            return conn

        conn = inject_connection(example_func)()
        self.assertIsInstance(conn, Session)
