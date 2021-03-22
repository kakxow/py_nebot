import threading

from notion.client import NotionClient  # type: ignore

from .constants import CREDIT_FIELD_NAME, NOTION_TOKEN, NOTION_DB_PAGE_URL


class NameNotFound(BaseException):
    pass


def get_table():
    # Connects and returns a table with scores.
    client = NotionClient(token_v2=NOTION_TOKEN)
    page = client.get_block(NOTION_DB_PAGE_URL)
    table = page.views[0].collection
    return table


def get_all_scores():
    table = get_table()
    all_records = table.get_rows()
    return [record.get_all_properties() for record in all_records]


def add_record(user: dict, score: int = 0):
    table = get_table()
    row = table.add_row()
    row.telegram_id = str(user["id"])
    row.first_name = user["first_name"]
    row.last_name = user.get("last_name", "")
    row.username = user.get("username", "")
    row.credit = score
    print(f"Created new record {row.first_name} with score {score}")


def add_credits(user: dict, credits: int):
    table = get_table()
    search_results = table.get_rows(search=str(user["id"]))
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
