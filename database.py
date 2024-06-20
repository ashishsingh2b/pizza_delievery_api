from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

engine = create_engine("postgresql://postgres:password123#@localhost:5432/pizza_delievery",
                       echo=True
                       )

Base = declarative_base()

Session = sessionmaker()