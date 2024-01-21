import logging
from typing import Dict

# from cachetools import LFUCache
from sqlalchemy import select

from .settings import session

logger = logging.getLogger(__name__)


async def create_obj(model, **params):
    """Create object in db"""
    logger.debug(f"{__name__}.create_obj: model = {model}, params = {params}")
    new_obj = model(**params)
    async with session() as conn:
        conn.add(new_obj)
        await conn.commit()
    return new_obj


async def get_object(model, **filters):
    """Get object from db"""
    key = f"{model.__name__}{filters}"
    query = select(model).filter_by(**filters)
    logger.debug(f"{__name__}.get_obj: query = {query}")
    async with session() as conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_obj: result = {result}")
    obj = result.scalars().first()
    logger.debug(f"{__name__}.get_obj: obj = {obj}")
    return obj


async def get_all(model):
    """Get objects from db"""
    query = select(model)
    async with session() as conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_all: result = {result}")
    objects = result.scalars().all()
    logger.debug(f"{__name__}.get_all: obj = {objects}")
    return objects


async def get_all_with_filter(model, filters: dict):
    """Get objects from db"""
    query = select(model).filter_by(**filters)
    async with session() as conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_all: result = {result}")
    objects = result.scalars().all()
    logger.debug(f"{__name__}.get_all: obj = {objects}")
    return objects


async def get_objects(model, filters: Dict, limit=10, per_page=10):
    """Get objects from db"""
    query = select(model).filter_by(**filters).limit(limit).offset(per_page)
    logger.debug(f"{__name__}.get_objects: query = {query}")
    async with session() as conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_objects: result = {result}")
    objects = result.scalars().all()
    logger.debug(f"{__name__}.get_objects: obj = {objects}")
    return objects


async def get_or_create_object(model, **params):
    """Get object from db or create new one"""
    key = f"{model.__name__}{params}"
    obj = await get_object(model, **params)
    if not obj:
        obj = await create_object(model, **params)
    return obj


async def create_object(model, **params):
    """Create object in db"""
    logger.debug(f"{__name__}.create_obj: model = {model}, params = {params}")
    new_obj = model(**params)
    async with session() as conn:
        conn.add(new_obj)
        await conn.commit()
    return new_obj


def create_objects():
    pass


async def update_object(obj, **params):
    async with session() as conn:
        for key, value in params.items():
            setattr(obj, key, value)
        conn.add(obj)
        await conn.commit()
    return obj


async def update_object_by_id(model, id: int, **params):
    obj = await get_object(model, id=id)
    updated_obj = await update_object(obj, **params)
    return updated_obj


def update_objects():
    pass


def update_or_create_object():
    pass


async def delete_object(model, id: int):
    pass


def delete_objects():
    pass
