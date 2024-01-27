import logging
from typing import Dict

# from cachetools import LFUCache
from sqlalchemy import select

from .settings import session
from .utils import inject_connection

logger = logging.getLogger(__name__)


@inject_connection
async def create_obj(model, params, conn=None):
    """Create object in db"""
    logger.debug(f"{__name__}.create_obj: model = {model}, params = {params}")
    new_obj = model(**params)
    async with conn:
        conn.add(new_obj)
        await conn.commit()
    return new_obj


@inject_connection
async def get_object(model, filters, conn=None):
    """Get object from db"""
    key = f"{model.__name__}{filters}"
    query = select(model).filter_by(**filters)
    logger.debug(f"{__name__}.get_obj: query = {query}")
    async with conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_obj: result = {result}")
    obj = result.scalars().first()
    logger.debug(f"{__name__}.get_obj: obj = {obj}")
    return obj


@inject_connection
async def get_all(model, conn=None):
    """Get objects from db"""
    query = select(model)
    async with conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_all: result = {result}")
    objects = result.scalars().all()
    logger.debug(f"{__name__}.get_all: obj = {objects}")
    return objects


@inject_connection
async def get_all_with_filter(model, filters: dict, conn=None):
    """Get objects from db"""
    query = select(model).filter_by(**filters)
    async with conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_all: result = {result}")
    objects = result.scalars().all()
    logger.debug(f"{__name__}.get_all: obj = {objects}")
    return objects


@inject_connection
async def get_objects(model, filters: Dict, limit=10, per_page=10, conn=None):
    """Get objects from db"""
    query = select(model).filter_by(**filters).limit(limit).offset(per_page)
    logger.debug(f"{__name__}.get_objects: query = {query}")
    async with conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_objects: result = {result}")
    objects = result.scalars().all()
    logger.debug(f"{__name__}.get_objects: obj = {objects}")
    return objects


async def get_or_create_object(model, params, conn=None):
    """Get object from db or create new one"""
    key = f"{model.__name__}{params}"
    obj = await get_object(model, params)
    if not obj:
        obj = await create_object(model, params)
    return obj


@inject_connection
async def create_object(model, params, conn=None):
    """Create object in db"""
    logger.debug(f"{__name__}.create_obj: model = {model}, params = {params}")
    new_obj = model(**params)
    async with conn:
        conn.add(new_obj)
        await conn.commit()
    return new_obj


def create_objects():
    pass


@inject_connection
async def update_object(obj, params, conn=None):
    """
    Soft Update object in db.
    If attribute not exists in model`s fields, then skip field without error
    """
    avaliable_fields = obj.__class__.__table__.columns.keys()
    async with conn:
        for key, value in params.items():
            if key in avaliable_fields:
                setattr(obj, key, value)
        await conn.commit()
        conn.refresh(obj)
    return obj


@inject_connection
async def update_or_error(obj, params, conn=None):
    """
    Soft Update object in db.
    If attribute not exists in model`s fields, then skip field without error
    """
    avaliable_fields = obj.__class__.__table__.columns.keys()
    async with conn:
        for key, value in params.items():
            if key in avaliable_fields:
                setattr(obj, key, value)
            else:
                raise AttributeError(f"Attribute {key} not exists in {obj.__class__.__name__}")
        await conn.commit()
        conn.refresh(obj)
    return obj


async def update_object_by_id(model, id: int, params, conn=None):
    obj = await get_object(model, id=id)
    updated_obj = await update_object(obj, params)
    return updated_obj


def update_objects():
    pass


async def update_or_create_object(model, filters, params):
    obj = await get_or_create_object(model, filters)
    return await update_object(obj, params)


@inject_connection
async def delete_object(obj, conn=None):
    async with conn:
        conn.delete(obj)
        await conn.flush()
    logger.debug(f"{__name__}.delete_object: model = {obj.__class__}, id = {obj.id}")
    return True


@inject_connection
async def delete_object_by_id(model, id: int, conn=None):
    async with conn:
        conn.query(model).where(model.id == id)
        await conn.commit()
    return True


async def delete_objects(objects, conn=None):
    return False