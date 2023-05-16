"""User credit card tests."""

import datetime
from datetime import datetime as dt

import pytest

from bank_bot.cc_payment import Card, User


def _to_date(date):
    return dt.strptime(date, "%Y-%m-%d")


FAKE_DATE_TIME = _to_date("2023-02-01")


@pytest.fixture
def fake_now(monkeypatch):
    class FakeDateTime:
        @classmethod
        def now(cls):
            return FAKE_DATE_TIME

    monkeypatch.setattr(datetime, "datetime", FakeDateTime)


@pytest.fixture(name="card")
def fixture_card():
    """Create a main credit card fixture."""
    return Card(number=5624, min_payment=50, due=_to_date("2023-06-15"))


@pytest.fixture(name="card2")
def fixture_card2():
    """Create a second credit card fixture."""
    return Card(number=1009, min_payment=70, due=_to_date("2023-07-25"))


@pytest.fixture(name="user")
def fixture_user(card, card2):
    """Create user fixture."""
    return User(user_id=1, cards={card.number: card, card2.number: card2}, balance=500)


def test_card_creation(card):
    """Check successful credit card creations."""
    assert card
    assert card.number == 5624
    assert card.min_payment == 50
    assert card.due == _to_date("2023-06-15")


def test_card_check_payment_amount(card):
    """Check if it is possible to make a payment of the specified amount."""
    assert not card.check_payment_amount(20)
    assert card.check_payment_amount(50)
    assert card.check_payment_amount(100)


def test_card_check_payment_date(card, fake_now):
    """Check if it is possible to make a payment on the specified date."""

    assert not card.check_payment_date(_to_date("2023-08-10"))
    assert not card.check_payment_date(_to_date("2023-01-30"))

    assert card.check_payment_date(_to_date("2023-06-15"))
    assert card.check_payment_date(_to_date("2023-03-10"))


def test_user(user):
    """Check successful user creations."""
    assert user
    assert user.user_id == 1
    assert user.balance == 500
    assert len(user.cards) == 2


def test_user_is_my_card(user):
    """Check that the user has this card."""
    assert not user.is_my_card(4500)
    assert user.is_my_card(5624)
    assert user.is_my_card(1009)


def test_user_check_payment_date(user, fake_now):
    """Check that the user can pay at the time."""

    assert not user.check_payment_date(1009, _to_date("2023-08-10"))

    assert not user.check_payment_date(5624, _to_date("2023-08-10"))
    assert not user.check_payment_date(5624, _to_date("2023-01-30"))

    assert user.check_payment_date(5624, _to_date("2023-06-15"))
    assert user.check_payment_date(5624, _to_date("2023-03-10"))


def test_user_make_payment(user, fake_now):
    """Check that the user can make payment."""
    assert not user.make_payment(4500, _to_date("2023-06-15"), 100)

    assert not user.make_payment(5624, _to_date("2023-08-15"), 100)
    assert not user.make_payment(5624, _to_date("2023-04-15"), 40)
    assert not user.make_payment(5624, _to_date("2023-04-15"), 700)

    assert user.make_payment(5624, _to_date("2023-04-15"), 100)
