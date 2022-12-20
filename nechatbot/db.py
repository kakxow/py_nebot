import sys

import oracledb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .constants import ORACLE_DSN, ORACLE_USER_PW, ORACLE_WALLET_PW, ORACLE_USER_LOGIN
from .nechat_db_types import User


oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb


engine = create_engine(
    f"oracle://{ORACLE_USER_LOGIN}:{ORACLE_USER_PW}@",
    connect_args={
        "dsn": ORACLE_DSN,
        "config_dir": "/home/kakxow/Documents/nebot-oracle/Wallet_nebotbd",
        "wallet_location": "/home/kakxow/Documents/nebot-oracle/Wallet_nebotbd",
        "wallet_password": ORACLE_WALLET_PW,
    },
)

Session = sessionmaker(bind=engine)


def update_user(chat_id: int, user: dict, updates: dict) -> None:
    with Session() as session:
        old_user = (
            session.query(User)
            .filter(User.id == user["id"], User.chat == chat_id)
            .first()
        )
        if old_user:
            for name, value in updates.items():
                setattr(old_user, name, value)
        else:
            new_user = User(
                id=user["id"],
                chat=chat_id,
                first_name=user["first_name"],
                last_name=user.get("last_name", ""),
                username=user.get("username", ""),
                **updates,
            )
            session.add(new_user)
        session.commit()
