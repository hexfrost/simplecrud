from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import AsyncSession


class CRUDConfig:
    """Singleton class for CRUD settings"""
    _instance: CRUDConfig | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CRUDConfig, cls).__new__(cls)
        return cls._instance

    @property
    def sessionmaker(self) -> AsyncSession:
        if not self._sessionmaker:
            raise ValueError("Sessionmaker is not set. Use set_sessionmaker() method")
        return self._sessionmaker

    def set_sessionmaker(self, sessionmaker: AsyncSession) -> None:
        """Set sessionmaker"""
        self._sessionmaker = sessionmaker


def session() -> AsyncSession:
    """Get session"""
    config = CRUDConfig()
    return config.sessionmaker()
