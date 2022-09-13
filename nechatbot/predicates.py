from datetime import datetime as dt
import re


WORDS_PATTERN = re.compile(r"\w+")
FIRST_WORD_PATTERN = re.compile(r"^\w+")
LAST_WORD_PATTERN = re.compile(r"\w+$")
WORDS_AND_EMOJIS_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    r"]|\w+"
)  # https://gist.github.com/Alex-Just/e86110836f3f93fe7932290526529cd1#gistcomment-3236190
TAGS_PATTERN = re.compile(r"@\w+")


def extract_words_and_emojis(message: str) -> set[str]:
    words_and_emojis = WORDS_AND_EMOJIS_PATTERN.findall(message.lower())
    return set(words_and_emojis)


def is_message_contains_words_and_emojis(message: str, *words_to_find: str) -> bool:
    message_words = extract_words_and_emojis(message)
    return any(word.lower() in message_words for word in words_to_find)


def extract_words(message: str) -> set[str]:
    words = WORDS_PATTERN.findall(message.lower())
    return set(words)


def is_message_contains_words(message: str, *words_to_find: str) -> bool:
    message_words = extract_words(message)
    return any(word.lower() in message_words for word in words_to_find)


def is_message_contains_phrases(message: str, *phrases: str) -> bool:
    return any(phrase.lower() in message.lower() for phrase in phrases)


def is_message_startswith(message: str, *prefixes: str) -> bool:
    return any(message.lower().startswith(prefix.lower()) for prefix in prefixes)


def is_message_starts_with_word(message: str, *word_prefixes: str) -> bool:
    match = FIRST_WORD_PATTERN.search(message.lower())
    if match is None:
        return False
    first_word = match.group()
    return any(first_word == word.lower() for word in word_prefixes)


def is_message_endswith(message: str, *postfixes: str) -> bool:
    return any(message.lower().endswith(postfix.lower()) for postfix in postfixes)


def is_message_ends_with_word(message: str, *word_postfixes: str) -> bool:
    match = LAST_WORD_PATTERN.search(message.lower())
    if match is None:
        return False
    last_word = match.group()
    return any(last_word == postfix.lower() for postfix in word_postfixes)


def is_date(text: str) -> bool:
    try:
        day, month = text.split(".")
        dt(2000, int(month), int(day))
    except ValueError:
        return False
    return True


def extract_tags(text: str) -> set[str]:
    tags = TAGS_PATTERN.findall(text.lower())
    return set(tags)
