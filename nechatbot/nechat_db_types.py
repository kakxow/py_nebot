from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    ForeignKey,
    ForeignKeyConstraint,
    Identity,
)


Base = declarative_base()


tags_for_users = Table(
    "tags_for_users",
    Base.metadata,
    Column("user_id", Integer, primary_key=True),
    Column("user_chat_id", Integer, primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    ForeignKeyConstraint(
        ["user_chat_id", "user_id"],
        ["users.chat", "users.id"],
    ),
)

mentions_for_tags = Table(
    "mentions_for_tags",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    Column("mention_id", ForeignKey("mention_tags.id"), primary_key=True),
)


class MentionTag(Base):
    __tablename__ = "mention_tags"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    def __repr__(self) -> str:
        return "<MentionTag(name='%s')>" % (self.name,)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    mentions = relationship(
        MentionTag, secondary=mentions_for_tags, collection_class=list
    )

    def __repr__(self) -> str:
        return "<Tag(name='%s', mentions=[%s])>" % (
            self.name,
            self.mentions,
        )


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
    tags = relationship(Tag, secondary=tags_for_users, collection_class=list)

    def __repr__(self) -> str:
        return "<User(first_name='%s', last_name='%s', username='%s')>" % (
            self.first_name,
            self.last_name,
            self.username,
        )
