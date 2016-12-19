from flask.ext.jsontools import JsonSerializableBase
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(cls=(JsonSerializableBase,))
