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
        await conn.refresh(new_obj)
    return new_obj


async def get_obj(model, **filters):
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


async def get_objects(model, filters: Dict, limit=10, offset=10):
    """Get objects from db"""
    query = select(model).filter_by(**filters).limit(limit).offset(offset)
    logger.debug(f"{__name__}.get_objects: query = {query}")
    async with session() as conn:
        result = await conn.execute(query)
    logger.debug(f"{__name__}.get_objects: result = {result}")
    objects = result.scalars().all()
    logger.debug(f"{__name__}.get_objects: obj = {objects}")
    return objects


async def get_or_create(model, **params):
    """Get object from db or create new one"""
    key = f"{model.__name__}{params}"
    obj = await get_obj(model, **params)
    if not obj:
        obj = await create_obj(model, **params)
    return obj


async def update_obj(model, id: int, **params):
    async with session() as conn:
        obj = await get_obj(model, id=id)
        for key, value in params.items():
            setattr(obj, key, value)
        conn.add(obj)
        await conn.commit()
        await conn.refresh(obj)
    return obj
