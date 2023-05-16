"""Fake DB storage tests."""

import pytest

from bank_bot.db import DataBase


@pytest.fixture(name="db")
def fixture_db():
    """Create a DB fixture."""
    return DataBase()


def test_at_random_user(db):
    """Check the creation of a fake user."""
    user = db.get_user(1)

    assert user.user_id == 1
    assert user.balance > 0
    assert len(user.cards) > 0


def test_get_user(db):
    """Check the user data retrieval."""
    user1 = db.get_user(1)
    user1_cache = db.get_user(1)

    assert user1.user_id == user1_cache.user_id
    assert user1.balance == user1_cache.balance
    assert user1.cards == user1_cache.cards
