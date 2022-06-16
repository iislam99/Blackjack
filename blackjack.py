#! /usr/bin/env python3

"""Play Blackjack by running ./blackjack.py in the terminal."""

from blackjackgame.game import BlackjackGame

def main():
    """Main function to initialize and run game."""
    game = BlackjackGame()
    game.run()

if __name__ == '__main__':
    main()
