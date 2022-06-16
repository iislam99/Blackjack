"""Game module. Contains all properties of main game like gameloop."""


from blackjackgame.player import Player, Dealer, to_file, from_file
from blackjackgame.cards import Deck
from blackjackgame.miscellaneous import type_effect, print_line
from blackjackgame.miscellaneous import prompt_str, prompt_int


def prompt_rules():
    """Ask players if they want to see the game rules."""
    qtn = (
        "\nPress r to display the rules or press p to play the game."
        "\nThen press enter."
    )
    if prompt_str(question=qtn, true='r', false='p'):
        type_effect(
            "\nHOW TO PLAY:\n"
            "\nThis game will be played with 8 decks of cards."
            "\nWhen the game begins, each player will wager an amount of money"
            "\nthey can afford. They will then be dealt 2 cards each face-up,"
            "\nexcept for the dealer, who is dealt one card face-up and one"
            "\nface-down. The objective of the game is to have all your cards"
            "\nadd up to 21 or as close as you can get without going over."
            #
            "\n\nTo calculate the sum of your hand, use the following rules:"
            "\n- Cards ranked between 2 and 10 have values equal to their"
            "\n  ranks."
            "\n- Aces are valued at 1 or 11. The value is 11 unless the hand's"
            "\n  sum is over 21, in which case it is 1."
            "\n- Jacks, Queens, and Kings are all valued at 10."
            "\n- Add up all the values in your hand to find the hand's sum."
            #
            "\n\nThe following are the winning/losing conditions:"
            "\n- If you go over 21, you \"bust\" and lose your wagered money."
            "\n- If you are at 21 or under and the dealer is also at the same"
            "\n  value, you \"push\", or tie, and you do not lose or gain any"
            "\n  money."
            "\n- If the dealer is under 21 and you are higher than the dealer"
            "\n  and at or lower than 21, you win money equal to your wager."
            #
            "\n\nIf you believe you can win by adding only one more card to"
            "\nyour hand, you can double down. In doing so, your wager will be"
            "\ndoubled and another card will be added to your hand. You will"
            "\nnot be able to add any more cards to your hand for the rest of"
            "\nthe current round."
            #
            "\n\nIf the dealer's face-up card is valued at 10 or higher, you"
            "\nhave the option to buy insurance. This means if the dealer's"
            "\nface-down card results in a total of 21, you will be awarded"
            "\nmoney equal to your insurance."
            #
            "\n\nIf the two cards you are initially dealt have the same rank,"
            "\nyou have the option to split that hand into two hands. In doing"
            "\nso, you will be allowed to play the round on both hands."
            #
            "\n\nAfter splitting, doubling down, and insurance bets are"
            "\ncompleted, players have the option to add more cards to their"
            "\nhands. If a player \"hits\", they will be dealt a single card."
            "\nIf a player stands, it will be the next player's turn."
            #
            "\n\nYou will be required to press enter after all your future"
            "\ninputs."
            "\n\nYou are now ready to play!"
        )
    print_line(before=True)


class BlackjackGame:
    """Contains all methods related to game functionality."""

    def __init__(self):
        """Constructor. Initializes game variables and player count."""
        self.player_list = []
        self.gameover = False
        self.full_player_list = from_file("players.db")
        self.deck = Deck(60, 80)
        for _ in range(7):
            self.deck.merge(Deck())
        self.deck.shuffle_and_cut()

        # Welcoming players
        type_effect("Welcome to Blackjack!")
        prompt_rules()

    def set_players(self):
        """Creates all players and sets turn order based on player rolls."""

        # Getting player count
        qtn = "\nPlease enter the total number of players (1-4): "
        num_players = prompt_int(
            question=qtn, less_than=1, greater_than=4, newline=False
        )

        # Creating and naming all players.
        type_effect(
            "\nAll player names must be unique. When prompted, please"
            "\nenter a unique name/username that can be used to"
            "\nidentify you in future games."
        )

        for i in range(num_players):
            type_effect(f"\nPlease enter Player {i + 1}'s name: ", False)
            name = input()

            # If player in database, retrieve player stats
            if len(self.full_player_list) != 0:
                for plr in self.full_player_list:
                    if plr.name == name:
                        type_effect(
                            f"\nWelcome back, {plr.name}!"
                            f"\nYou have ${plr.balance} in your account."
                        )
                        temp = plr
                        break

                    # Player does not exist, create new player
                    if plr == self.full_player_list[-1]:
                        type_effect(
                            "\nNew player created."
                            "\n$10000 has been added to your account."
                        )
                        temp = Player(name)
            else:
                type_effect(
                    "\nNew player created."
                    "\n$10000 have been added to your account."
                )
                temp = Player(name)
            self.player_list.append(temp)
        self.player_list.append(Dealer())
        print_line(before=True)

    def place_bets(self):
        """Ask players for their wagers."""
        for plr in self.player_list:
            if not plr.is_dealer:
                qtn = (
                    f"\n{plr.name}, you have ${plr.balance} in your account."
                    "\nHow much would you like to wager?"
                )
                bet = prompt_int(
                    question=qtn, less_than=1, greater_than=plr.balance
                )
                plr.bet.append(bet)
                print_line(before=True)

        # Display all players and their wagers
        type_effect("\nPlayers and Wagers")
        print_line(19)
        for plr in self.player_list:
            if not plr.is_dealer:
                type_effect(f"{plr.name} bet ${plr.bet[0]}.")
        print_line(before=True)

    def deal_all(self):
        """Deal all players their hands."""
        type_effect("\nDealing cards...")
        for _ in range(2):
            for plr in self.player_list:
                card = self.deck.deal()
                plr.add_to_hand(card[0])
        for plr in self.player_list:
            type_effect(f"\n{plr.name}:")
            type_effect("Hand: ", newline=False)
            plr.display_hand()
        print_line(before=True)

    def prompt_insurance(self):
        """Determines if player will buy insurance."""
        for plr in self.player_list:
            if not plr.is_dealer:
                dealer_card = self.player_list[-1].hand[0][0]
                if int(dealer_card) >= 10 or dealer_card.rank == 'Ace':
                    qtn = f"\n{plr.name}, do you want to buy insurance? (y/n)"
                    if prompt_str(question=qtn, true='y', false='n'):
                        qtn = "\nHow much do you want to buy?"
                        plr.insurance = prompt_int(
                            question=qtn,
                            less_than=1,
                            greater_than=plr.balance - plr.bet[0],
                        )
                    print_line(before=True)

    def prompt_split(self, player):
        """Determines if player will split based on player's input."""

        qtn = f"\nDo you want to split your hand? (y/n)"
        if prompt_str(question=qtn, true='y', false='n'):
            card = player.hand[0].pop()
            player.add_to_hand(card, index=1)
            for i in range(2):
                card = self.deck.deal()
                player.add_to_hand(card[0], index=i)
            player.bet.append(player.bet[0])

            type_effect("\nHand 1: ", newline=False)
            player.display_hand(index=0)
            type_effect("\nHand 2: ", newline=False)
            player.display_hand(index=1)

    def prompt_double_down(self, player, index):
        """Determines if player will double down based on player's input."""

        if player.has_split():
            qtn = f"\nDo you want to double down on hand {index + 1}? (y/n)"
        else:
            qtn = "\nDo you want to double down on your hand? (y/n)"

        if prompt_str(question=qtn, true='y', false='n'):
            player.bet[index] *= 2
            card = self.deck.deal()
            player.add_to_hand(card[0], index=index)

            type_effect("\nNew Hand: ", newline=False)
            player.display_hand(index=index)

            total = player.hand_sum(index)
            if total > 21:
                type_effect("\nYou BUSTED!")
            elif total == 21:
                type_effect("\nYou reached 21!")
            return True
        return False

    def hit_or_stand(self, player, i):
        """Hitting and standing logic."""
        while True:
            if player.is_dealer:
                player.player_list = self.player_list
            if not player.does_hit(index=i):
                break
            card = self.deck.deal()
            player.hand[i].append(card[0])
            if player.has_split():
                type_effect(f"\nHand {i + 1}: ", newline=False)
            else:
                type_effect("\nHand: ", newline=False)
            player.display_hand(index=i)
            total = player.hand_sum(i)

            # Bust
            if total > 21:
                type_effect("\nYou BUSTED!")
                break

            # Win
            if total == 21:
                type_effect("\nYou reached 21!")
                break

    def check_insurance_bets(self, player):
        """Update player balances based on insurance bets."""
        if int(player.hand[0][0]) >= 10:
            dealer_total = player.hand_sum(0)
            if dealer_total == 21:
                type_effect(
                    f"\n{player.name} has 21!"
                    "\nPlayers win their insurance bets!"
                )
                for plr in self.player_list:
                    if not plr.is_dealer:
                        if plr.insurance:
                            type_effect(
                                f"\n{plr.name} wins ${plr.insurance}!"
                                f"\nOld balance: ${plr.balance}"
                            )
                            plr.balance += plr.insurance
                            type_effect(f"New balance: ${plr.balance}")
            else:
                type_effect(
                    f"\n{player.name} does not have 21!"
                    "\nPlayers lose their insurance bets."
                )
                for plr in self.player_list:
                    if not plr.is_dealer:
                        if plr.insurance:
                            type_effect(
                                f"\n{plr.name} loses ${plr.insurance}."
                                f"\nOld balance: ${plr.balance}"
                            )
                            plr.balance -= plr.insurance
                            type_effect(f"New balance: ${plr.balance}")

    def take_turn(self, player):
        """Contains logic regarding what happens during a player's turn."""
        type_effect(f"\nIt is {player.name}'s turn!")

        # Player
        if not player.is_dealer:
            dealer = self.player_list[-1]
            type_effect(f"\n{dealer.name}'s Hand: ", newline=False)
            dealer.display_hand()

            type_effect(f"\n{player.name}'s Hand: ", newline=False)
            player.display_hand()

            # Splitting hand
            if player.can_split():
                self.prompt_split(player)

            # Double down
            can_hit_1 = True
            can_hit_2 = True
            if player.can_double_down(0):
                if self.prompt_double_down(player, 0):
                    can_hit_1 = False
            if player.has_split():
                if player.can_double_down(1):
                    if self.prompt_double_down(player, 1):
                        can_hit_2 = False

            # Hit or stand
            if can_hit_1:
                self.hit_or_stand(player, 0)
            if player.has_split():
                if can_hit_2:
                    self.hit_or_stand(player, 1)
        # Dealer
        else:
            player.hidden = False
            type_effect(f"\n{player.name}'s Hand: ", newline=False)
            player.display_hand()
            self.check_insurance_bets(player)
            self.hit_or_stand(player, 0)

        print_line(before=True)

    def check_win(self):
        """Check whether the players won."""

        type_effect("\nTime to see who won!")

        dealer = self.player_list[-1]
        dealer_total = dealer.hand_sum(0)
        type_effect(f"\n{dealer.name}'s Hand: ", newline=False)
        dealer.display_hand()
        if dealer_total > 21:
            type_effect(f"\n{dealer.name} busted!")

        for plr in self.player_list:
            if not plr.is_dealer:
                for i, _ in enumerate(plr.hand):
                    if i == 0 or plr.has_split():
                        print_line(length=20, before=True)
                        if plr.has_split():
                            type_effect(
                                f"\n{plr.name}'s Hand {i + 1}: ", newline=False
                            )
                        else:
                            type_effect(f"\n{plr.name}'s Hand: ", newline=False)
                        plr.display_hand(index=i)
                        p_total = plr.hand_sum(i)

                        # Won
                        win1 = p_total <= 21 < dealer_total
                        win2 = dealer_total < p_total <= 21
                        if win1 or win2:
                            type_effect(
                                f"\n{plr.name} won!"
                                f"\nOld balance: ${plr.balance}"
                            )
                            plr.balance += plr.bet[i]
                            type_effect(
                                f"New balance: ${plr.balance}"
                                f"\nProfit: +${plr.bet[i]}"
                            )
                        # Push
                        elif p_total == dealer_total and p_total <= 21:
                            type_effect(
                                f"\n{plr.name} pushed."
                                "\nYour balance stays the same: "
                                f"${plr.balance}"
                            )
                        # Lost
                        else:
                            type_effect(
                                f"\n{plr.name} lost!"
                                f"\nOld balance: ${plr.balance}"
                            )
                            plr.balance -= plr.bet[i]
                            type_effect(
                                f"New balance: ${plr.balance}"
                                f"\nProfit: -${plr.bet[i]}"
                            )
        print_line(before=True)

    def endgame(self):
        """Ask players if they want to play again."""

        qtn = "\nDo you all want to play again? (y/n)"
        if prompt_str(question=qtn, true='y', false='n'):
            for plr in self.player_list:
                plr.reset()
            type_effect("\nResetting game...")
            print_line(before=True)
        else:
            for plr in self.player_list:
                plr.reset()
            self.update_db()
            self.gameover = True
            print_line(length=13, before=True)
            print("End of game.")

    def reset_values(self):
        """Reset values if game will be played again."""
        for plr in self.player_list:
            plr.reset()

        # Reset deck if cut card has been reached
        if self.deck.needs_shuffling():
            self.deck = Deck(52 * 8 - 80, 52 * 8 - 60)
            for _ in range(7):
                self.deck.merge(Deck())
            self.deck.shuffle_and_cut()

    def update_db(self):
        """Updating database player list with new balances and players."""
        if len(self.full_player_list) == 0:
            self.full_player_list = self.player_list[
                0 : len(self.full_player_list) - 1
            ]
        else:
            for i in self.player_list:
                for j in self.full_player_list:
                    if not i.is_dealer:
                        if i.name == j.name:
                            j = i
                            break
                        if j == self.full_player_list[-1]:
                            self.full_player_list.append(i)
        to_file("players.db", self.full_player_list)

    def run(self):
        """Contains gameloop. Creates players and begins game."""
        self.set_players()
        while not self.gameover:
            self.place_bets()
            type_effect("\nThe game will now begin!")
            self.deal_all()
            self.prompt_insurance()

            for plr in self.player_list:
                self.take_turn(plr)

            self.check_win()
            self.endgame()
