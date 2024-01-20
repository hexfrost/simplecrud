from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from simplecrud.settings import CRUDConfig


class AsyncConnFactory():

    def __init__(self):
        self.async_engine = create_async_engine("sqlite+aiosqlite:///./test.db")
        self.async_session_maker = async_sessionmaker(self.async_engine, expire_on_commit=False, class_=AsyncSession)
        self.config = CRUDConfig()
        self.config.set_sessionmaker(self.async_session_maker)

    def __call__(self, *args, **kwargs):
        return self.config.sessionmaker
