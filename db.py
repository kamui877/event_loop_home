import config
import atexit
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine(config.PG_DSN)
Base = declarative_base(engine)


class CharactersModel(Base):

    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    birth_year = Column(String)
    eye_color = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    films = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)


Base.metadata.create_all()
Session = sessionmaker(engine)
atexit.register(lambda: engine.dispose())
