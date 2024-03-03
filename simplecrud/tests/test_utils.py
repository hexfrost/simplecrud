import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from simplecrud.tests.test_crud import engine, Base

database_url = "sqlite:///./test.db"
engine = create_engine(database_url)
session_maker = sessionmaker(bind=engine)
