from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


# load the database credentials.
PASSWORD = settings.DATABASE_PASSWORD
USER = settings.DATABASE_USER
HOST = settings.DATABASE_HOST
PORT = settings.DATABASE_PORT
DATABASE_NAME = settings.DATABASE_NAME

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
)

# create engine for connection to postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create a communication session for the postgres DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    """This creates an independent database session/connection (SessionLocal)
    per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
