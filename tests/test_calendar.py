import pytest

from nechatbot import calendar

def test_convert_slash():
    assert calendar.convert_date_for_trello("31/12") == "2090-12-31"

def test_convert_dot():
    assert calendar.convert_date_for_trello("31.12") == "2090-12-31"

def test_convert_colon():
    assert calendar.convert_date_for_trello("31:12") == "2090-12-31"

def test_convert_dash():
    assert calendar.convert_date_for_trello("31-12") == "2090-12-31"
