"""This module contains random functions used by the other modules."""


from sys import stdout
from time import sleep


def type_effect(text, newline=True, speed=0.05):
    """Prints strings one character at a time for a typing effect."""
    for char in text:
        stdout.write(char)
        stdout.flush()
        sleep(speed)
    if newline:
        print()


def print_line(length=50, before=False, after=False):
    """Print line of specified size using type effect."""
    if before:
        print()
    type_effect("-" * length, speed=0.02)
    if after:
        print()


def prompt_str(question, true, false, newline=True):
    """Ask user to input string. Check input validity."""
    while True:
        type_effect(question, newline=newline)
        resp = input()

        # Checks if input has non-letter characters
        if resp == '' or any(not c.isalpha() for c in resp):
            type_effect("Invalid response.")
        else:
            if resp.lower() == true:
                return True
            if resp.lower() == false:
                return False
            type_effect("Invalid response.")


def prompt_int(question, less_than, greater_than, newline=True):
    """Ask user to input integer value. Check input validity."""
    while True:
        type_effect(question, newline=newline)
        val = input()

        # Check if input has any non-digit characters
        if val == '' or any(not c.isdigit() for c in val):
            type_effect("\nInvalid value entered.")
        else:
            val = int(val)

            # Check if inputted numbers are outside of range
            if val < less_than or val > greater_than:
                type_effect("\nThis value is out of range.")

            # Input is valid
            else:
                return val
