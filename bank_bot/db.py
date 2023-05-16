"""Fake database."""

from bank_bot.cc_payment import User


class DataBase:
    """Fake database storage."""

    def __init__(self):
        """Create new class instance."""
        self._storage = {}

    def get_user(self, user_id):
        """Get user profile from storage by id. Or create it at random."""
        user = self._storage.get(user_id)
        if not user:
            user = User.at_random(user_id)
            self._storage[user_id] = user

        return user
