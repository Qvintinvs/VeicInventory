from sqlalchemy import Column, Integer, LargeBinary, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = Column(LargeBinary)  # blob aqui
