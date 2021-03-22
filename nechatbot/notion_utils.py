import threading

from notion.client import NotionClient  # type: ignore

from .constants import CREDIT_FIELD_NAME, NOTION_TOKEN, NOTION_DB_PAGE_URL


class NameNotFound(BaseException):
    pass


def get_page():
    # Connects and returns a table with scores.
    client = NotionClient(token_v2=NOTION_TOKEN)
    page = client.get_collection_view(NOTION_DB_PAGE_URL)
    return page


def get_all_scores():
    page = get_page()
    filter_params = {
        "filters": [{
            "filter": {"operator": "is_not_empty"},
            "property": "title"
        }],
        "operator": "and"
    }
    sort_params = [{
        "direction": "descending",
        "property": CREDIT_FIELD_NAME,  # Don't ask me, ask Notion. Nl?g
    }]
    all_records = page.build_query(filter=filter_params, sort=sort_params).execute()
    return [record.get_all_properties() for record in all_records]


def get_all_scores_pretty():
    scores = get_all_scores()
    text_scores = [f"{record['first_name']} {record['username']} - {getattr(record, CREDIT_FIELD_NAME)}" for record in scores]
    return "\n".join(text_scores)


def add_record(user: dict, score: int = 0):
    page = get_page()
    page.collection.add_row(
        telegram_id=str(user["id"]),
        first_name=user["first_name"],
        last_name=user.get("last_name", ""),
        username=user.get("username", ""),
        credit=score
    )
    print(f"Created new record {user['first_name']} with score {score}")


def add_credits(user: dict, credits: int):
    page = get_page()
    filter_params = {
        "filters": [{
            "filter": {
                "value": {
                    "type": "exact",
                    "value": str(user["id"]),
                },
                "operator": "string_is"
            },
            "property": "title"
        }],
        "operator": "and"
    }
    search_results = page.build_query(filter=filter_params).execute()
    if not search_results:
        raise NameNotFound
    target_record = search_results[0]
    current_credits = getattr(target_record, CREDIT_FIELD_NAME)
    new_credits = current_credits + credits
    setattr(target_record, CREDIT_FIELD_NAME, new_credits)
    print(f"Record {target_record.first_name} has score of {new_credits} now")


def _add_credits_or_record(user: dict, credits: int):
    try:
        add_credits(user, credits)
    except NameNotFound:
        add_record(user, credits)


def add_credits_or_record(user: dict, credits: int):
    t = threading.Thread(target=_add_credits_or_record, args=(user, credits))
    t.start()
    print("Thread started")
