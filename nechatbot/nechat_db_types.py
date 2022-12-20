from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    chat = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64))
    username = Column(String(64))
    birthday = Column(String(64))
    credit = Column(Integer)
    location = Column(String(64))

    def __repr__(self) -> str:
        return "<User(first_name='%s', last_name='%s', username='%s')>" % (
            self.first_name,
            self.last_name,
            self.username,
        )
