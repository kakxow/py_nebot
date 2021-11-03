from .predicates import is_date

__all__ = [
    "add_birthday",
    "choose_city"
]


async def add_birthday(inline_query) -> list:
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


async def choose_city(inline_query):
    text = inline_query["query"]
    if not text:
        text_message_content_msk = {
            "message_text": "I'm in Moscow now!"
        }
        text_message_content_spb = {
            "message_text": "I'm in St. Petersburg now!"
        }
        text_message_content_remove = {
            "message_text": "I'm in undefined now!"
        }
        inline_keyboard_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "Where are you?",
                        "switch_inline_query_current_chat": "",
                    }
                ]
            ]
        }
        inline_query_result_msk = {
            "type": "article",
            "id": "msk",
            "title": "msk",
            "input_message_content": text_message_content_msk,
            "reply_markup": inline_keyboard_markup,
        }
        inline_query_result_spb = {
            "type": "article",
            "id": "spb",
            "title": "spb",
            "input_message_content": text_message_content_spb,
            "reply_markup": inline_keyboard_markup,
        }
        inline_query_result_remove = {
            "type": "article",
            "id": "remove",
            "title": "remove",
            "input_message_content": text_message_content_remove,
            "reply_markup": inline_keyboard_markup,
        }
        return [inline_query_result_msk, inline_query_result_spb, inline_query_result_remove]
