import time
import unittest

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from simplecrud.crud import *
from simplecrud.tests.factories import AsyncConnFactory
from simplecrud.utils import async_to_sync

database_url = "sqlite:///./test.db"
engine = create_engine(database_url)
session_maker = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class ExampleModel(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class TestAsyncCRUDFunctions(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)
        self.session = AsyncConnFactory()

    def tearDown(self):
        Base.metadata.drop_all(engine)

    @async_to_sync
    async def test_async_create_obj(self):
        params_1 = dict(name="test_async_create_obj1")
        new_obj_1 = await create_object(ExampleModel, params_1)
        self.assertEqual(new_obj_1.name, "test_async_create_obj1")

        params_2 = dict(name="test_async_create_obj2")
        new_obj_2 = await create_object(ExampleModel, params_2)
        self.assertEqual(new_obj_2.name, "test_async_create_obj2")

    @async_to_sync
    async def test_create_obj_params_error(self):
        params_1 = dict(name="test_create_obj_params_error", wrong="wrong")
        with self.assertRaises(TypeError):
            new_obj_1 = await create_object(ExampleModel, **params_1)

    @async_to_sync
    async def test_bulk_create(self):
        all_ = await get_all(ExampleModel)
        self.assertEqual(len(all_), 0)
        data = [dict(name=f"test_bulk_create{i}") for i in range(1, 11)]
        objects = await bulk_create(ExampleModel, data)
        all_ = await get_all(ExampleModel)
        self.assertEqual(len(all_), 10)
        for i in range(1, 11):
            self.assertEqual(all_[i - 1].name, f"test_bulk_create{i}")

    @async_to_sync
    async def test_get_object(self):
        params_1 = dict(name="test_get_object")
        await create_object(ExampleModel, params_1)
        obj = await get_object(ExampleModel, params_1)
        self.assertEqual(obj.name, "test_get_object")

    @async_to_sync
    async def test_get_object_not_exist(self):
        params_1 = dict(name="test_get_object_not_exist1")
        obj = await create_object(ExampleModel, params_1)
        none_expected = await get_object(ExampleModel, filters=dict(name="test_get_object_not_exist0"))
        self.assertEqual(none_expected, None)

    @async_to_sync
    async def test_get_object_error(self):
        params_1 = dict(name="test_get_object_error")
        obj = await create_object(ExampleModel, params_1)

        with self.assertRaises(InvalidRequestError):
            error_expected = await get_object(ExampleModel, filters=dict(wrong="wrong"))

    @async_to_sync
    async def test_get_all_objects(self):
        all_ = await get_all(ExampleModel)
        self.assertEqual(len(all_), 0)
        for i in range(5):
            params_1 = dict(name=f"test_get_all_objects{i}")
            await create_object(ExampleModel, params_1)
        all_ = await get_all(ExampleModel)
        self.assertEqual(5, len(all_))
        self.assertTrue(isinstance(all_, list))
        await delete_object(all_[0])

    @async_to_sync
    async def test_get_all_if_objects_not_exist(self):
        all_ = await get_all(ExampleModel)
        self.assertEqual(len(all_), 0)
        self.assertTrue(isinstance(all_, list))

    @async_to_sync
    async def test_get_all_with_filter(self):
        for i in range(1, 6):
            params_1 = dict(name=f"test_get_all_with_filter{i}")
            await create_object(ExampleModel, params_1)
        all_ = await get_all_with_filter(ExampleModel, dict(name="test_get_all_with_filter1"))
        self.assertEqual(len(all_), 1)

    # TODO: Add test for multiple filter parameters

    @async_to_sync
    async def test_get_all_with_filter_error(self):
        await create_object(ExampleModel, dict(name="test_get_all_with_filter_negative"))
        with self.assertRaises(InvalidRequestError):
            await get_all_with_filter(ExampleModel, dict(wrong="wrong"))

    @async_to_sync
    async def test_get_all_with_filter_negative(self):
        for i in range(1, 6):
            params_1 = dict(name=f"test_get_all_with_filter{i}")
            await create_object(ExampleModel, params_1)
        all_ = await get_all_with_filter(ExampleModel, dict(name="not_exist"))
        self.assertEqual(len(all_), 0)

    @async_to_sync
    async def test_get_objects_with_limit_and_per_page(self):
        for i in range(1, 30):
            params_1 = dict(name=f"test_get_objects_with_limit_and_ofset{i}")
            await create_object(ExampleModel, params_1)
        ten = await get_objects(ExampleModel, {}, limit=10, offset=10)
        self.assertEqual(len(ten), 10)
        one = await get_objects(ExampleModel, {}, limit=1, offset=1)
        self.assertEqual(len(one), 1)
        second = await get_objects(ExampleModel, {}, limit=1, offset=2)
        self.assertEqual(len(second), 1)
        self.assertEqual(second[0].id, 3)

    @async_to_sync
    async def test_get_object_by_filters(self):
        params_1 = dict(name="test_get_object_by_filters")
        new_ = await create_object(ExampleModel, params_1)
        obj = await get_object(ExampleModel, filters=dict(id=new_.id))
        self.assertEqual(obj.name, "test_get_object_by_filters")

    @async_to_sync
    async def test_get_object_by_filters_negative(self):
        params_1 = dict(name="test_get_object_by_filters_negative")
        new_ = await create_object(ExampleModel, params_1)
        with self.assertRaises(InvalidRequestError):
            obj = await get_object(ExampleModel, filters=dict(pk=new_.id))

    @async_to_sync
    async def test_get_or_create_object(self):
        self.assertEqual(len(await get_all(ExampleModel)), 0)
        params_1 = dict(name="test_get_or_create_object")
        new_1 = await get_or_create_object(ExampleModel, params_1)
        self.assertEqual(len(await get_all(ExampleModel)), 1)
        new_2 = await get_or_create_object(ExampleModel, params_1)
        self.assertEqual(len(await get_all(ExampleModel)), 1)
        self.assertEqual(new_1.id, new_2.id)

    @async_to_sync
    async def test_update_object(self):
        params_1 = dict(name="test_update_object")
        obj1 = await create_object(ExampleModel, params_1)
        params_2 = dict(name="test_update_object2")
        obj2 = await update_object(obj1, params_2)
        self.assertEqual(obj2.name, "test_update_object2")
        self.assertEqual(obj1.id, obj2.id)

    @async_to_sync
    async def test_update_or_error(self):
        obj = await create_object(ExampleModel, dict(name="test_update_or_error"))
        await update_or_error(obj, dict(name="test_update_or_error_updated"))
        upd_obj = await get_object(ExampleModel, dict(id=obj.id))
        self.assertEqual(upd_obj.id, obj.id)
        self.assertEqual(upd_obj.name, "test_update_or_error_updated")

    @async_to_sync
    async def test_update_or_error_error(self):
        obj = await create_object(ExampleModel, dict(name="test_update_or_error"))
        with self.assertRaises(AttributeError):
            await update_or_error(obj, dict(wrong="wrong"))

    @async_to_sync
    async def test_update_or_error_negative(self):
        params_1 = dict(name="test_update_object")
        obj1 = await create_object(ExampleModel, params_1)
        wrong_params = dict(wrong="test_update_object2")
        with self.assertRaises(AttributeError) as error:
            obj2 = await update_or_error(obj1, wrong_params)
        error_msg = "Attribute wrong not exists in ExampleModel"
        self.assertEqual(error.exception.args[0], error_msg)

    @async_to_sync
    async def test_soft_update_without_error(self):
        params_1 = dict(name="test_update_object_negative")
        obj1 = await create_object(ExampleModel, params_1)
        self.assertFalse(hasattr(obj1, "wrong"))
        wrong_params = dict(wrong="wrong")
        obj2 = await update_object(obj1, wrong_params)
        self.assertEqual(obj1.id, obj2.id)
        self.assertFalse(hasattr(obj2, "wrong"))

    @async_to_sync
    async def test_update_or_error(self):
        params_1 = dict(name="test1")
        obj1 = await create_object(ExampleModel, params_1)
        params_2 = dict(name="test2")
        obj2 = await update_or_error(obj1, params_2)
        self.assertEqual(obj2.name, "test2")

    @async_to_sync
    async def test_update_by_id(self):
        params_1 = dict(name="test1")
        obj1 = await create_object(ExampleModel, params_1)
        id_ = obj1.id
        params_2 = dict(name="test2")
        obj2 = await update_object_by_id(ExampleModel, id_, params_2)
        self.assertEqual(obj2.name, "test2")

    @async_to_sync
    async def test_update_or_create_object(self):
        self.assertEqual(len(await get_all(ExampleModel)), 0)
        params_1 = dict(name="test_update_or_create_object1")
        new_1 = await update_or_create_object(ExampleModel, params_1, params_1)
        self.assertEqual(len(await get_all(ExampleModel)), 1)
        params_2 = dict(name="test_update_or_create_object2")
        new_2 = await update_or_create_object(ExampleModel, params_1, params_2)
        self.assertEqual(new_2.name, "test_update_or_create_object2")
        self.assertEqual(new_1.id, new_2.id)

    # @async_to_sync
    # async def test_bulk_update(self):
    #     all_ = await get_all(ExampleModel)
    #     self.assertEqual(len(all_), 0)
    #     for i in range(1, 11):
    #         params_1 = dict(name=f"test_bulk_update{i}")
    #         await create_object(ExampleModel, params_1)
    #     all_ = await get_all(ExampleModel)
    #     self.assertEqual(len(all_), 10)
    #     new_data = dict(name="test_bulk_update_updated")
    #     objects = await bulk_update(all_, new_data)
    #     self.assertEqual(len(objects), 10)
    #     self.assertEqual(list, type(objects), "Result must be list")
    #     all_ = await get_all(ExampleModel)
    #     for obj in all_:
    #         self.assertEqual("test_bulk_update_updated", obj.name)

    @async_to_sync
    async def test_delete_object(self):
        all_ = await get_all(ExampleModel)
        self.assertEqual(len(all_), 0)
        params_1 = dict(name="test_delete_object")
        new_1 = await create_object(ExampleModel, params_1)
        all_ = await get_all(ExampleModel)
        self.assertEqual(len(all_), 1)
        result = await delete_object(new_1)
        self.assertEqual(result, True)
        all_ = await get_all(ExampleModel)
        get_ = await get_object(ExampleModel, filters=dict(id=new_1.id))
        self.assertEqual(len(all_), 0)

    @async_to_sync
    async def test_delete_objects(self):
        for i in range(1, 12):
            params_1 = dict(name=f"test_delete_objects{i}")
            await create_object(ExampleModel, params_1)
        all_ = await get_all(ExampleModel)
        result = await bulk_delete(all_[0:10])
        all_ = await get_all(ExampleModel)
        self.assertEqual(1, len(all_))
        self.assertEqual(all_[0].name, "test_delete_objects11")
        self.assertEqual(all_[0].id, 11)

    @async_to_sync
    async def test_bulk_delete(self):
        for i in range(1, 12):
            params_1 = dict(name=f"test_delete_objects{i}")
            await create_object(ExampleModel, params_1)
        objects = await get_all(ExampleModel)
        self.assertEqual(11, len(objects))
        await bulk_delete(objects)
        all_ = await get_all(ExampleModel)
        self.assertEqual(0, len(all_))

    @async_to_sync
    async def test_bulk_delete_by_id(self):
        for i in range(1, 12):
            params_1 = dict(name=f"test_delete_objects{i}")
            await create_object(ExampleModel, params_1)
        ids = [i.id for i in await get_all(ExampleModel)]
        self.assertEqual(11, len(ids))
        await bulk_delete_by_id(ExampleModel, ids)
        all_ = await get_all(ExampleModel)
        self.assertEqual(0, len(all_))
