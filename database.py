from decouple import config
from sqlalchemy.orm.base import sa_exc
from sqlmodel import Session, create_engine



DATABASE_URL = config("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session

