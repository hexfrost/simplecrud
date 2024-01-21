[![Maintainability](https://api.codeclimate.com/v1/badges/d33ecb2661fb7aedf516/maintainability)](https://codeclimate.com/github/hexfrost/sqlalchemy-models-commands/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d33ecb2661fb7aedf516/test_coverage)](https://codeclimate.com/github/hexfrost/sqlalchemy-models-commands/test_coverage)

# SimpleCRUD
SimpleCRUD is a library that provides a simple way to create CRUD commands for SQLAlchemy models.

## Installation

```bash
pip install simplecrud
```
```
poetry add simplecrud
```

## Usage


### Example usage
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from simplecrud import CRUDConfig, BaseModelWithCRUD, get_all, create_obj, update_obj

engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=True)
async_sessionmaker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# Create a model
class ExampleModel(DeclarativeBase):
    __tablename__ = "example_model"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)


# Create CRUD config
CRUDConfig.sessionmaker(async_sessionmaker)

async def example_func():

    # Create a model
    new_model = await create_obj(model, name="test", description="test")

    # Get all models
    all_objs = await get_all(model)

    # Update a model
    updated_obj = await update_obj(model, name="test2", description="test2")

    # Delete a model
    await delete_obj(model, name="test2", description="test2")

```







