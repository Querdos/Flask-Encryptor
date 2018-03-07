# coding=utf-8
from sqlalchemy                 import Column, String, Integer, LargeBinary

class BaseFile:
    __tablename__   = 'uploaded_files'
    id              = Column(Integer, primary_key=True)
    filename        = Column(String, nullable=False, unique=True)
    realname        = Column(LargeBinary, nullable=False)
    path            = Column(String, nullable=False)

class BaseToken:
    __tablename__   = 'tokens'
    id              = Column(Integer, primary_key=True)
    value           = Column(String, nullable=False)
