import json

from .constants import CREDIT_FIELD_NAME
from .trello_main import (
    create_card,
    get_all_cards,
    get_card,
    update_card
)


def get_all_scores_pretty(chat_id: int) -> str:
    """
    Gets all social credit scores and prettifies the result to be sent by the bot. 
    """
    cards = get_all_cards(chat_id, "Credit")
    card_descriptions = [json.loads(card.desc) for card in cards]
    card_descriptions.sort(key=lambda c: c[CREDIT_FIELD_NAME], reverse=True)
    text_scores = [f"•{record['first_name']} {record['username']}: {record[CREDIT_FIELD_NAME]}" for record in card_descriptions]
    text = "<b>Nechat Social Credit System scores</b>\n"
    score_table = "\n".join(text_scores) or "Nothing to show yet!"
    return text + score_table


def update_or_add_social_credit(chat_id: int, user: dict, credits: int) -> str:
    """
    Updates or creates new user card in credits Trello list with chat_id in name,
    and returns a keyword for bot's reply.
    """
    card = get_card(chat_id, str(user["id"]), "Credit")
    if card:
        card_desc = json.loads(card.desc)
        credits = card_desc[CREDIT_FIELD_NAME] + credits
        update_card(card, {CREDIT_FIELD_NAME: credits}, {})
        action = "Updated"
    else:
        create_card(
            chat_id,
            user,
            "Credit",
            {CREDIT_FIELD_NAME: credits}
        )
        action = "Created"
    return action
