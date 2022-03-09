from .predicates import is_date

__all__ = ["add_birthday", "choose_city"]


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
        text_message_content_msk = {"message_text": "I'm in Moscow now!"}
        text_message_content_spb = {"message_text": "I'm in St. Petersburg now!"}
        text_message_content_baku = {"message_text": "I'm in Baku now!"}
        text_message_content_ist = {"message_text": "I'm in Istanbul now!"}
        text_message_content_tbl = {"message_text": "I'm in Tbilisi now!"}
        text_message_content_yer = {"message_text": "I'm in Yereven now!"}
        text_message_content_remove = {"message_text": "I'm in undefined now!"}
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
        inline_query_result = {
            "type": "article",
            "reply_markup": inline_keyboard_markup,
        }
        inline_query_result_msk = {
            **inline_query_result,
            "id": "msk",
            "title": "msk",
            "input_message_content": text_message_content_msk,
        }
        inline_query_result_spb = {
            **inline_query_result,
            "id": "spb",
            "title": "spb",
            "input_message_content": text_message_content_spb,
        }
        inline_query_result_baku = {
            **inline_query_result,
            "id": "baku",
            "title": "baku",
            "input_message_content": text_message_content_baku,
        }
        inline_query_result_ist = {
            **inline_query_result,
            "id": "ist",
            "title": "ist",
            "input_message_content": text_message_content_ist,
        }
        inline_query_result_tbl = {
            **inline_query_result,
            "id": "tbl",
            "title": "tbl",
            "input_message_content": text_message_content_tbl,
        }
        inline_query_result_yer = {
            **inline_query_result,
            "id": "yer",
            "title": "yer",
            "input_message_content": text_message_content_yer,
        }
        inline_query_result_remove = {
            **inline_query_result,
            "id": "remove",
            "title": "remove",
            "input_message_content": text_message_content_remove,
        }
        return [
            inline_query_result_msk,
            inline_query_result_spb,
            inline_query_result_baku,
            inline_query_result_ist,
            inline_query_result_tbl,
            inline_query_result_yer,
            inline_query_result_remove,
        ]
