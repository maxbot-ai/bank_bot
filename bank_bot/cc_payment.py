"""User profile and credit card payments."""

import datetime
from dataclasses import dataclass
from random import randint


@dataclass(frozen=True)
class Card:
    """Credit card class."""

    number: int
    min_payment: int
    due: datetime

    def check_payment_date(self, date):
        """Check if it is possible to make a payment on the specified date."""
        if date.date() > self.due.date() or date.date() < datetime.datetime.now().date():
            return False

        return True

    def check_payment_amount(self, amount):
        """Check if it is possible to make a payment of the specified amount."""
        if amount < self.min_payment:
            return False

        return True


class User:
    """User profile class."""

    def __init__(self, user_id, cards, balance):
        """Create new class instance."""
        self._user_id = user_id
        self._cards = cards
        self._balance = balance

    @property
    def user_id(self):
        """Access to the profile id field."""
        return self._user_id

    @property
    def cards(self):
        """Return a dictionary of all user cards."""
        return self._cards

    @property
    def balance(self):
        """Return user balance."""
        return self._balance

    def is_my_card(self, card_number):
        """Check that the user has this card."""
        return card_number in self.cards

    def check_payment_date(self, card_number, date):
        """Check if it is possible to make a payment for this card on the date specified."""
        if not self.is_my_card(card_number):
            return False

        return self.cards[card_number].check_payment_date(date)

    def check_payment_amount(self, card_number, amount):
        """Check if it is possible to make a payment of the specified amount for this card."""
        if amount > self.balance:
            return False
        return self.cards[card_number].check_payment_amount(amount)

    def make_payment(self, card_number, date, amount):
        """Make a payment."""
        if self.check_payment_date(card_number, date) and self.check_payment_amount(
            card_number, amount
        ):
            self._balance = self._balance - amount
            return True

        return False

    @classmethod
    def at_random(cls, user_id):
        """Create a random user profile."""
        balance = randint(1000, 9999)  # nosec B311
        cards = {}
        for _ in range(randint(1, 4)):  # nosec B311
            due = datetime.datetime.now() + datetime.timedelta(randint(1, 365))  # nosec B311
            card = Card(
                number=randint(1000, 9999), min_payment=randint(20, 100), due=due  # nosec B311
            )
            cards[card.number] = card

        return cls(user_id, cards, balance)
