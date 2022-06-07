from . import storage
from .nechat_types import Chat


def get_all_scores_pretty(chat_id: str) -> str:
    """
    Gets all social credit scores and prettifies the result to be sent by the bot.
    """
    chats = storage.get_chats()
    chat = chats.get(chat_id, Chat(chat_id))
    users = list(chat.users.values())
    users.sort(key=lambda u: u.credit, reverse=True)
    text_scores = [
        f"•{user.first_name} {user.username}: {user.credit}"
        for user in users
        if user.credit
    ]
    text = "<b>Nechat Social Credit System scores</b>\n"
    score_table = "\n".join(text_scores) or "Nothing to show yet!"
    return text + score_table


def update_or_add_social_credit(chat_id: str, user: dict, credits: int) -> int:
    """
    Updates credits score, returns new score.
    """
    chats = storage.get_chats()
    chat = chats.get(chat_id, Chat(chat_id))
    credits_old = 0
    user_id = str(user["id"])
    if user_id in chat.users:
        credits_old = chat.users[user_id].credit
    updated_user = storage.update_user(chat_id, user, credit=(credits_old + credits))
    return updated_user.credit
