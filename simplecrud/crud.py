import logging
from typing import Dict, List

from sqlalchemy import select, delete
from .utils import inject_connection


# READ / GET
@inject_connection
async def get_object(model, filters, conn=None) -> object:
    """Get object from db"""
    query = select(model).filter_by(**filters)
    async with conn:
        result = await conn.execute(query)
    obj = result.scalars().first()
    return obj


@inject_connection
async def get_all(model, conn=None) -> List[object]:
    """Get objects from db"""
    query = select(model)
    async with conn:
        result = await conn.execute(query)
    objects = result.scalars().all()
    return objects


@inject_connection
async def get_all_with_filter(model, filters: dict, conn=None) -> List[object]:
    """Get objects from db"""
    query = select(model).filter_by(**filters)
    async with conn:
        result = await conn.execute(query)
    objects = result.scalars().all()
    return objects


@inject_connection
async def get_objects(model, filters: Dict, limit=10, offset=10, conn=None) -> List[object]:
    """Get objects from db"""
    query = select(model).filter_by(**filters).limit(limit).offset(offset)
    async with conn:
        result = await conn.execute(query)
    objects = result.scalars().all()
    return objects


@inject_connection
async def get_or_create_object(model, params, conn=None) -> object:
    """Get object from db or create new one"""
    obj = await get_object(model, params, conn=conn)
    if not obj:
        obj = await create_object(model, params, conn=conn)
    return obj


# CREATE
@inject_connection
async def create_object(model, params, conn=None) -> object:
    """Create object in db"""
    new_obj = model(**params)
    async with conn:
        conn.add(new_obj)
        await conn.commit()
    return new_obj


@inject_connection
async def bulk_create(model, data: List[Dict], conn=None) -> List[object]:
    """Bulk create objects in db"""
    return [await create_object(model, params, conn=conn) for params in data]


# UPDATE
@inject_connection
async def update_object(obj, params, conn=None) -> object:
    """
    Soft Update object in db.
    If attribute not exists in model`s fields, then skip field without error
    """
    avaliable_fields = obj.__class__.__table__.columns.keys()
    for key, value in params.items():
        if key in avaliable_fields:
            setattr(obj, key, value)
    async with conn:
        await conn.commit()
        conn.refresh(obj)
    return obj


@inject_connection
async def update_or_error(obj, params, conn=None) -> object:
    """
    Soft Update object in db.
    If attribute not exists in model`s fields, then skip field without error
    """
    avaliable_fields = obj.__class__.__table__.columns.keys()
    for key, value in params.items():
        if key not in avaliable_fields:
            raise AttributeError(f"Attribute {key} not exists in {obj.__class__.__name__}")
    obj = await update_object(obj, params, conn=conn)
    return obj


@inject_connection
async def update_object_by_id(model, id: int, params, conn=None) -> object:
    """Update object in db by id"""
    obj = await get_object(model, dict(id=id))
    updated_obj = await update_object(obj, params, conn=conn)
    return updated_obj


# @inject_connection
# async def bulk_update(objects, params, conn=None) -> List[object]:
#     """Bulk update objects in db"""
#     updated_objects = []
#     for obj in objects:
#         updated_obj = await update_object(obj, params, conn=conn)
#         updated_objects.append(updated_obj)
#     return updated_objects


@inject_connection
async def update_or_create_object(model, filters, params, conn=None) -> object:
    obj = await get_or_create_object(model, filters, conn=conn)
    return await update_object(obj, params, conn=conn)


# DELETE
@inject_connection
async def delete_object(obj, conn=None) -> bool:
    model = obj.__class__
    id_ = obj.id
    return await delete_object_by_id(model, id_, conn=conn)


@inject_connection
async def delete_object_by_id(model, id_: int, conn=None) -> bool:
    query = delete(model).where(model.id == id_)
    async with conn:
        await conn.execute(query)
        await conn.commit()
    return True


@inject_connection
async def bulk_delete(objects, conn=None) -> bool:
    for obj in objects:
        await delete_object(obj, conn=conn)
    return True


@inject_connection
async def bulk_delete_by_id(model, ids, conn=None) -> bool:
    for id_ in ids:
        await delete_object_by_id(model, id_, conn=conn)
    return True
