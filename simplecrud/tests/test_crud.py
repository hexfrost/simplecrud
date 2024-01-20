import unittest

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session


database_url = "sqlite:///./test.db"
engine = create_engine(database_url)


class Base(DeclarativeBase):
    pass

class ExampleModel(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class TestCRUDFunctions(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_create_obj(self):
        params = dict(
            name="test"
        )
        new_obj = ExampleModel(**params)
        with Session(engine) as conn:
            conn.add(new_obj)
            conn.commit()
            conn.refresh(new_obj)

        self.assertEqual(new_obj.name, "test")