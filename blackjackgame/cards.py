"""Cards module that is used to simulate a deck of cards."""


from random import shuffle, randrange
from collections import namedtuple
from math import floor


def stringify_card(card):
    """Returns string when Card object is returned."""
    # Value used to obtain correct unicode card emoji
    # 12th unicode value is Knight; skipped to obtain Queen and King
    if card.rank not in ["Jack", "Queen", "King"]:
        val = Deck.values_dict[card.rank]
    else:
        if card.rank == "Jack":
            val = 11
        elif card.rank == "Queen":
            val = 13
        elif card.rank == "King":
            val = 14

    if card.suit == "Spades":
        utf = ord("\U0001F0A1")  # Start of spades unicode
    elif card.suit == "Hearts":
        utf = ord("\U0001F0B1")  # Start of hearts unicode
    elif card.suit == "Diamonds":
        utf = ord("\U0001F0C1")  # Start of diamonds unicode
    elif card.suit == "Clubs":
        utf = ord("\U0001F0D1")  # Start of clubs unicode

    card = chr(utf + val - 1)
    return f"{card}"


def card_value(card):
    """Get Blackjack value for card."""
    return Deck.values_dict[card.rank]


Card = namedtuple('Card', ['rank', 'suit'])
Card.__str__ = stringify_card
Card.__int__ = card_value


class Deck:
    """Deck class that contains all deck functionality."""

    ranks = ['Ace'] + [str(x) for x in range(2, 11)] + 'Jack Queen King'.split()
    suits = 'Clubs Hearts Spades Diamonds'.split()
    values = list(range(1, 11)) + [10, 10, 10]
    values_dict = dict(zip(ranks, values))

    def __init__(self, cut_card_position_min=0, cut_card_position_max=0):
        """Class constructor that initializes deck components."""
        self._cards = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]
        if cut_card_position_min == 0 and cut_card_position_max == 0:
            self._cut_card_position = 10
        else:
            self._cut_card_position = randrange(
                cut_card_position_min, cut_card_position_max
            )

    def __getitem__(self, position):
        """Override getitem method to return card at specific position."""
        return self._cards[position]

    def __len__(self):
        """Override len method to return size of deck."""
        return len(self._cards)

    def __str__(self):
        """Override str method to display entire deck."""
        return '\n'.join(map(str, self._cards))

    @property
    def cards(self):
        """Getter for cards."""
        return self._cards

    def shuffle(self, num=1):
        """Shuffle deck."""
        for _ in range(num):
            shuffle(self._cards)

    def cut(self):
        """Cutting the deck."""
        pos = floor(len(self._cards) * 0.2)
        half = (len(self._cards) // 2) + randrange(-pos, pos)
        tophalf = self._cards[:half]
        bottomhalf = self._cards[half:]
        self._cards = bottomhalf + tophalf

    def shuffle_and_cut(self):
        """Shuffle and cut deck."""
        self.shuffle()
        self.cut()

    def deal(self, num=1):
        """Deal cards to player."""
        return [self._cards.pop(0) for _ in range(num)]

    def merge(self, other_deck):
        """Merge deck with another deck."""
        self._cards = self._cards + other_deck.cards

    def needs_shuffling(self):
        """Check if cut card has been reached and deck needs shuffling."""
        return len(self._cards) <= self._cut_card_position
