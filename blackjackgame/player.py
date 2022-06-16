"""Player module consists of all human player and AI player properties."""


import pickle
from blackjackgame.miscellaneous import type_effect, prompt_str


def to_file(pickle_file, players):
    """Write players to database."""
    with open(pickle_file, 'wb') as file_handle:
        pickle.dump(players, file_handle, pickle.HIGHEST_PROTOCOL)


def from_file(pickle_file):
    """Read player from database."""
    try:
        with open(pickle_file, 'rb') as file_handle:
            players = pickle.load(file_handle)
    except Exception:
        players = []
        to_file(pickle_file, players)
    return players


class Player:
    """Holds all player properties necessary for game, like name and hand."""

    def __init__(self, name, bankroll=10000):
        """Player constructor. Initializes Player attributes."""
        self._name = name
        self._balance = bankroll
        self._bet = []
        self._insurance = 0
        self._hand = [[], []]
        self._is_dealer = False
        self._hidden = False

    def __str__(self):
        """Override Player str method."""
        return (
            f"\n{self._name}:"
            f"\nBalance: ${self._balance}"
            f"\nBets: {self._bet}"
            f"\nHands: {self._hand}"
        )

    def __repr__(self):
        """Override Player repr method."""
        return f"Player({self._name}, {self._balance})"

    @property
    def name(self):
        """Getter for player name."""
        return self._name

    @property
    def hand(self):
        """Getter for player hand."""
        return self._hand

    @hand.setter
    def hand(self, hand):
        """Setter for player hand."""
        self._hand = hand

    @property
    def balance(self):
        """Getter for player balance."""
        return self._balance

    @balance.setter
    def balance(self, balance):
        """Setter for player balance."""
        self._balance = balance

    @property
    def bet(self):
        """Getter for player bet."""
        return self._bet

    @bet.setter
    def bet(self, bet):
        """Setter for player bet."""
        self._bet = bet

    @property
    def insurance(self):
        """Getter for player insurance."""
        return self._insurance

    @insurance.setter
    def insurance(self, insurance):
        """Setter for player insurance."""
        self._insurance = insurance

    @property
    def is_dealer(self):
        """Checks if player is dealer."""
        return self._is_dealer

    def can_split(self):
        """Determine if player can split hand."""
        # If two initial cards are the same
        if self._hand[0][0].rank == self._hand[0][1].rank:
            # If player can afford to double wager
            if 2 * self.bet[0] <= self.balance:
                return True
        return False

    def has_split(self):
        """Determine if the player has split their hand."""
        return len(self._hand[1]) > 0

    def can_double_down(self, index):
        """Determine if the player can double down."""
        return 2 * self.bet[index] <= self.balance

    def does_hit(self, index=0):
        """Determines if player will hit based on player's input."""

        total = self.hand_sum(index)
        # Bust
        if total > 21:
            type_effect("\nYou BUSTED!")
            return False
        # Win
        if total == 21:
            type_effect("\nYou reached 21!")
            return False

        qtn = f"\n{self.name}, do you want to hit or stand on "
        if self.has_split():
            qtn += f"Hand {index + 1}? (h/s)"
        else:
            qtn += "your hand? (h/s)"

        if prompt_str(question=qtn, true='h', false='s'):
            return True
        return False

    def add_to_hand(self, card, index=0):
        """Add card to player's hand."""
        self._hand[index].append(card)

    def hand_sum(self, index=0):
        """Finding sum of cards in hand."""
        total = sum(map(int, self._hand[index]))
        if (
            sum(map(lambda c: c.rank == 'Ace', self._hand[index]))
            and total + 10 <= 21
        ):
            total += 10
        return total

    def display_hand(self, index=0):
        """Display player hand."""
        # Print hand 1
        for i in range(2):
            if i == index:
                for card in self._hand[i]:
                    type_effect(str(card) + ' ', newline=False)
                type_effect(f"\nTotal: {self.hand_sum(i)}")

    def reset(self):
        """Reset player values for new game."""
        self._hand = [[], []]
        self._bet = []
        self._insurance = 0


class Dealer(Player):
    """Inherits Player class properties. Represents AI player."""

    def __init__(self):
        """Constructor for AI player."""
        super().__init__("JARVIS")
        self._is_dealer = True
        self._player_list = []
        self._hidden = True

    @property
    def is_dealer(self):
        """Checks if player is dealer."""
        return self._is_dealer

    @property
    def player_list(self):
        """Getter for player list."""
        return self._player_list

    @player_list.setter
    def player_list(self, plr_list):
        """Setter for player list."""
        self._player_list = plr_list

    @property
    def hidden(self):
        """Getter for hidden."""
        return self._hidden

    @hidden.setter
    def hidden(self, hidden):
        """Setter for hidden attribute."""
        self._hidden = hidden

    def does_hit(self, index=0):
        """Dealer must hit on hands less than 17."""
        all_bust = True
        for plr in self._player_list:
            if plr.hand_sum(0) <= 21:
                all_bust = False
                break
            if plr.has_split():
                if plr.hand_sum(1) <= 21:
                    all_bust = False
                    break
        if all_bust:
            type_effect("\nAll players have busted. Must stand.")
            return False

        total = self.hand_sum(index)
        if total < 17:
            type_effect(f"\nHand total is less than 17. Must hit.")
            return True
        type_effect(f"\nHand is greater than or equal to 17. Must stand.")
        return False

    def can_split(self):
        """Dealer can never split hand."""
        return False

    def display_hand(self, index=0):
        """Display Dealer hand."""
        if not self._hidden:
            for card in self._hand[index]:
                type_effect(str(card) + ' ', newline=False)
            type_effect(f"\nTotal: {self.hand_sum(index)}")
        else:
            type_effect(str(self._hand[0][0]) + ' ', newline=False)
            type_effect(f"?\nTotal: ?")

    def reset(self):
        """Reset Dealer values for new game."""
        self._hand = [[], []]
        self._player_list = []
        self._hidden = True
