from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from trading_system.settings import DATABASE

engine = create_engine(DATABASE, pool_recycle=3600)
Session = sessionmaker(bind=engine)
session = Session()
