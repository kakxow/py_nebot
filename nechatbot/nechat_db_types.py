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


class MentionTag(Base):
    __tablename__ = "mention_tags"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False)
    tag = relationship("Tag", back_populates="mentions")

    def __repr__(self) -> str:
        return "<MentionTag(name='%s')>" % (self.name,)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    group = Column(String(64))
    users = relationship(
        "User", secondary=tags_for_users, back_populates="tags", collection_class=list
    )
    mentions = relationship(
        "MentionTag",
        back_populates="tag",
        cascade="save-update, merge, delete, delete-orphan",
        collection_class=list,
        passive_deletes=True,
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
    tags = relationship(
        Tag, secondary=tags_for_users, collection_class=list, back_populates="users"
    )

    def __repr__(self) -> str:
        return "<User(first_name='%s', last_name='%s', username='%s')>" % (
            self.first_name,
            self.last_name,
            self.username,
        )


def user_from_dict(telegram_user: dict, chat_id: int) -> User:
    return User(
        id=telegram_user["id"],
        chat=chat_id,
        first_name=telegram_user["first_name"],
        last_name=telegram_user.get("last_name", ""),
        username=telegram_user.get("username", ""),
    )
