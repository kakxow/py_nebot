import pytest

from nechatbot import birthdays


def test_convert_slash():
    assert birthdays.convert_date_for_trello("31/12") == "2090-12-31"


def test_convert_dot():
    assert birthdays.convert_date_for_trello("31.12") == "2090-12-31"


def test_convert_colon():
    assert birthdays.convert_date_for_trello("31:12") == "2090-12-31"


def test_convert_dash():
    assert birthdays.convert_date_for_trello("31-12") == "2090-12-31"
