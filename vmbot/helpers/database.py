# coding: utf-8

from __future__ import absolute_import, division, unicode_literals, print_function

from sqlalchemy import (create_engine, Column, Integer, BigInteger, Float, String,
                        Text, Enum, DateTime, LargeBinary, PickleType, ForeignKey)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

from .files import BOT_DB

engine = create_engine("sqlite:///{}".format(BOT_DB))
Session = sessionmaker(bind=engine)
Model = declarative_base()


def init_db():
    """Create all required database tables."""
    Model.metadata.create_all(engine)
