import re
from typing import Set

WORDS_PATTERN = re.compile(r"\w+")
FIRST_WORD_PATTERN = re.compile(r"^\w+")
LAST_WORD_PATTERN = re.compile(r"\w+$")


def extract_words(message: str) -> Set[str]:
    words = WORDS_PATTERN.findall(message.lower())
    return set(words)


def is_message_contains_words(message: str, *words_to_find: str) -> bool:
    message_words = extract_words(message)
    return any(word.lower() in message_words for word in words_to_find)


def is_message_contains_phrases(message: str, *phrases: str) -> bool:
    return any(phrase.lower() in message.lower() for phrase in phrases)


def is_message_startswith(message: str, *prefixes: str) -> bool:
    match = FIRST_WORD_PATTERN.search(message.lower())
    if match is None:
        return False
    first_word = match.group()
    return any(first_word == prefix.lower() for prefix in prefixes)


def is_message_endswith(message: str, *postfixes: str) -> bool:
    match = LAST_WORD_PATTERN.search(message.lower())
    if match is None:
        return False
    last_word = match.group()
    return any(last_word == postfix.lower() for postfix in postfixes)
