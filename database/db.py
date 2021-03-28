from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Table, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .engine import engine

Base = declarative_base()


# =============== USER ================
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    username = Column(String(255))
    state = Column(String())

    def __repr__(self):
        return f'<User {self.id} {self.username}>'

    def get_username(self):
        return '@' + self.username if self.username else self.first_name

    def get_name(self):
        return (self.first_name + ' ' + self.last_name) if self.last_name else self.first_name


session = sessionmaker(bind=engine)()


class Program(Base):
    __tablename__ = 'command'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    creator_id = Column(Integer, ForeignKey('user.id'))
    commands = Column(String())
