DB_URL = 'sqlite:///congress.db'

from sqlalchemy import create_engine
engine = create_engine(DB_URL)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
Base.metadata.bind = engine

def create_session():
	from sqlalchemy.orm import sessionmaker
	DBSession = sessionmaker()
	DBSession.bind = engine
	return DBSession()
