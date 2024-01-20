import unittest

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from simplecrud.crud import create_object
from simplecrud.tests.factories import AsyncConnFactory
from simplecrud.tests.utils import async_to_sync

database_url = "sqlite:///./test.db"
engine = create_engine(database_url)
session_maker = sessionmaker(bind=engine)


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
        params = dict(name="test")
        new_obj = ExampleModel(**params)
        with Session(engine) as conn:
            conn.add(new_obj)
            conn.commit()
            conn.refresh(new_obj)

        self.assertEqual(new_obj.name, "test")

    def test_create_obj_wrong_params(self):
        params = dict(name="test", wrong="wrong")
        with self.assertRaises(TypeError):
            new_obj = ExampleModel(**params)


class TestAsyncCRUDFunctions(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)
        self.session = AsyncConnFactory()

    def tearDown(self):
        Base.metadata.drop_all(engine)

    @async_to_sync
    async def test_async_create_obj(self):
        params_1 = dict(name="test1")
        new_obj_1 = await create_object(ExampleModel, **params_1)
        self.assertEqual(new_obj_1.name, "test1")

        params_2 = dict(name="test2")
        new_obj_2 = await create_object(ExampleModel, **params_2)
        self.assertEqual(new_obj_2.name, "test2")

    @async_to_sync
    async def test_async_create_obj_negative(self):
        params_1 = dict(name="test1")
        new_obj_1 = await create_object(ExampleModel, **params_1)
        self.assertNotEqual(new_obj_1.name, "test0")

    @async_to_sync
    async def test_async_create_obj_params_error(self):
        params_1 = dict(name="test1", wrong="wrong")
        with self.assertRaises(TypeError):
            new_obj_1 = await create_object(ExampleModel, **params_1)

    @async_to_sync
    async def test_get_object(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_object_negative(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_object_error(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_objects(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_objects_negative(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_objects_error(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_all(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_all_negative(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_all_error(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_all_with_filter(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_all_with_filter_negative(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_all_with_filter_error(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_object_by_filters(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_object_by_filters_negative(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_object_by_filters_error(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_or_create_object(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_or_create_object_negative(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_get_or_create_object_error(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_update_object(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_update_object_negative(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_update_object_error(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_update_or_create_object(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_update_or_create_object_negative(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_update_or_create_object_error(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_delete_object(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_delete_object_negative(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_delete_object_error(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_delete_objects(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_delete_objects_negative(self):
        raise Exception("Test not complete")

    @async_to_sync
    async def test_delete_objects_error(self):
        raise Exception("Test not complete")
