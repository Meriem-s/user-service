from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLACLCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db/perseus_db"

# create SQL engine

# Sqlite allows only one thread
engine = create_engine(SQLACLCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
