from .predicates import is_date

__all__ = [
    "add_birthday",
]


async def add_birthday(inline_query: dict) -> list:
    if inline_query["chat_type"] in ("group", "supergroup"):
        date = inline_query["query"]
        if is_date(date):
            user = inline_query["from"]
            text_message_content = {
                "message_text": f"Created {user['first_name']}'s card with birthday date {date}"
            }
            inline_keyboard_markup = {
                "inline_keyboard": [
                    [
                        {
                            "text": "Add your birthday too!",
                            "switch_inline_query_current_chat": "",
                        }
                    ]
                ]
            }
            inline_query_result = {
                "type": "article",
                "id": "1",
                "title": "Add birthday",
                "input_message_content": text_message_content,
                "reply_markup": inline_keyboard_markup,
            }
            return [inline_query_result]
    return []
