import sys

import oracledb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .constants import (
    ORACLE_DSN,
    ORACLE_USER_PW,
    ORACLE_WALLET_PW,
    ORACLE_USER_LOGIN,
    ORACLE_WALLET_PATH,
)
from .nechat_db_types import User, user_from_dict


oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb


engine = create_engine(
    f"oracle://{ORACLE_USER_LOGIN}:{ORACLE_USER_PW}@",
    connect_args={
        "dsn": ORACLE_DSN,
        "config_dir": ORACLE_WALLET_PATH,
        "wallet_location": ORACLE_WALLET_PATH,
        "wallet_password": ORACLE_WALLET_PW,
    },
)

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
