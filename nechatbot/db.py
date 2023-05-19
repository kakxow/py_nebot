from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .nechat_db_types import User, user_from_dict


engine = create_engine("sqlite:///nechat.db")

Session = sessionmaker(bind=engine)


def update_user(chat_id: int, telegram_user: dict, updates: dict) -> tuple[str, User]:
    response = "User info updated."
    with Session() as session:
        session.expire_on_commit = False
        user = session.query(User).get((telegram_user["id"], chat_id))
        if not user:
            response = "User created."
            user = user_from_dict(telegram_user, chat_id)
            session.add(user)
        for name, value in updates.items():
            if isinstance(value, list):
                old_value = getattr(user, name)
                if isinstance(old_value, list):
                    setattr(user, name, old_value + value)
            setattr(user, name, value)
        session.commit()
        return response, user
