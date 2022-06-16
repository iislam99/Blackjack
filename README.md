# Blackjack

Blackjack is a casino banking game where the player competes against the house or casino to have the best hand of cards. Unlike many other familiar card games, the players do not compete against each other or help one another. 

## Requirements
* Python3 must be installed.
* Game must be played in a terminal compatible with UTF-8 encoding. Otherwise, the cards will not be visible since they are emojis.
* Run the game with `./blackjack.py`.


## Rules

* There is at least one players playing the game and at most four.
* To start the game, a player can enter the number 1 through 4 to establish how many players there are.
* All players start with $10,000.00 in their bank balance.
* The dealer is always a computer AI and has unlimited funds.
* The game is turn based.
* All players have a name. Players' names may be used as unique identifiers or additional information can be gathered.
* Unique identifiers are used to serialize the game state to a file so that a player can have their bank balance upon return to the game.
* The game is played with 8 decks of cards. The cards are typical cards with the ranks Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King and the suits Clubs, Hearts, Spades, Diamonds. There are no jokers.
* The value of the cards is the rank of the card except for Ace, Jack, Queen, and King. An Ace's value is either 1 or 11 depending on what is most advantageous to the hand in question. Jacks, Queens, and Kings have a value of 10.
* Before playing, the cards must be shuffled and cut.
* A cut card is placed randomly between the 60th and 80th card from the bottom of the deck.
* The players play in the order their names are entered when the program starts. The dealer always goes last.
* Once each player has had a turn in ascending order, the turn returns to the first player. (The process is a circular queue.)
* The game is made up of many games. The players continue playing games of blackjack. At the end of every game, the game prompts the first player if they would like to play again. An answer of _yes_ means the dealer will deal cards out to the same players who played previously. With multiple players, should one choose to leave then the first player must answer _no_ to end the game and exit the program.
* At the start of every game, before cards are dealt, each player must place a wager. A wager can be at least $1 and at most their bank balance.
* A player may not wager more money than she has in her bank balance.
* The cards are dealt one by one, starting with the first player and ending on the dealer.
* The dealer's second card is kept hidden from the players all other cards are dealt face up.
* At the beginning of every turn, the game displays what cards the current player is holding and what face up card the dealer has showing.
* Whenever a card is dealt, it is printed or shown to the players before taking any other action.
* When it is the dealer's turn, the dealer must turn over (print or show) the face down card before taking any other action.
* All bets pay out 2 to 1.
* When a players turn begins, they have the option to buy _insurance_, _split_ (if possible), or _double down_.
* A player may not _surrender_.
* An _insurance_ best is a _side bet_ and is a separate wager. If a player chooses to buy _insurance_ then they may wager a minimum of $1 to a maximum of their bank balance minus what they have wagered on their hand.
* The player must decide to _split_ before deciding if she wants to buy _insurance_.
* A player may only _split_ once per game. This means a player's single hand can only double.
* _Insurance_ and _doubling down_ is per hand, not per player.
* The player may _split_ if and only if there is sufficient funds in her balance to double her wager.
* The player may _double down_ when her turn starts and never later.
* The player may _double down_ if and only if there is sufficient funds in her balance to double her wager.
* A player is prompted to _hit_ or _stand_ unless they are _busted_ or have _21_. If they have _busted_ or have _21_ then a message is shown stating that they have _busted_ or reached _21_.
* The dealer must _hit_ on a hand that is less than 17. The dealer must _stand_ on a hand that is 17 or greater.
* The dealer only _hits_ if there are players who are not _busted_.
* No one wins or loses when there is a _push_.
* A dealer does not place bets which means the dealer does not buy _insurance_ or _double down_.
* A dealer may not _split_ their hand.


To summarize the order of game play operations:
1. If needed, cards are shuffled, cut, and a cut card is placed in a position between the 60th and 80th card from the bottom.
1. For each player, a wager is entered before the cards are dealt.
1. Cards are dealt one at a time starting with the first player, continuing through to the last player, and ending on the dealer. This is done twice such that each player and the dealer has two cards. The dealer's last card is kept face down until it is the dealer's turn.
1. If the dealer has a card valued at 10 or greater showing, then for each player offer to purchase _insurance_ as a side bet.
1. For each player, begin their turn.
    1. If the player has two cards of identical rank, offer to _split_ the hand. If the hand is _split_, then convert the single hand to two hands dealing one additional card per hand. The player must double her wager.
    1. For each hand, offer to _double down_. For each _double down_ wager, the player's wager is doubled.
    1. While the player's hand is less than 21 or is not busted, offer the player to _hit_ or _stand_. When the player _hits_ deal an additional card. If the player _stands_, then the player's turn concludes.
1. The dealer plays last. If there exists a player who is not busted, then the dealer must play their hand according to the rules. Otherwise, the dealer stands.
1. For each player, determine if the player has won, lost, or _pushed_. Update all the players' balances to reflect the outcome of the game.
