from .constants import CREDIT_FIELD_NAME

from . import storage_utils


def get_all_scores_pretty(chat_id: int) -> str:
    """
    Gets all social credit scores and prettifies the result to be sent by the bot.
    """
    storage = storage_utils.Storage()
    users = storage.get_users_for_chat(chat_id)
    users.sort(key=lambda user: user["credit"], reverse=True)
    text_scores = [
        f"•{user['first_name']} {user['username']}: {user['credit']}" for user in users
    ]
    text = "<b>Nechat Social Credit System scores</b>\n"
    score_table = "\n".join(text_scores) or "Nothing to show yet!"
    return text + score_table


def update_or_add_social_credit(chat_id: int, user: dict, credits: int) -> str:
    """
    Updates or creates new user card in credits Trello list with chat_id in name,
    and returns a keyword for bot's reply.
    """
    storage = storage_utils.Storage()
    user_id = user["id"]
    new_user = storage.get_user(user_id)
    if new_user:
        new_user["credit"] += credits
        storage.update_user(user_id, new_user)
        action = "Updated"
    else:
        new_user = storage_utils.create_user_from_tg_user(**user, credit=credits)
        storage.update_user(user_id, new_user)
        action = "Created"
    return action
