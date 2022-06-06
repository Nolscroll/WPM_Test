import random
import json
import curses
from curses import wrapper

def start_screen(screen):
    """
    Initialize the terminal screen with a welcoming message
    """
    screen.clear()
    screen.addstr("Welcome to the WPM Test!")
    screen.addstr("\nPress any key to begin!")
    screen.refresh()
    screen.getkey()

def display_txt(screen, quote, current_txt, wpm=0):
    """
    Displays quote and typed text to the terminal screen
    """
    screen.addstr(quote)

    for i,char in enumerate(current_txt):
        correct_char = quote[i]

        # Select text color based on correctness:
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        screen.addstr(0, i, char, color)

def wpm_test(screen):
    """
    The WPM test itself
    """
    with open("quotes.json") as q:
        author, quote = random.choice(json.load(q)["quotes"]).values()
    current_txt = []

    while True:
        screen.clear()
        display_txt(screen, quote, current_txt)
        screen.refresh()

        key = screen.getkey()

        # Break if ESC key was pressed:
        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"): # Handles backspace
            if len(current_txt) > 0:
                current_txt.pop()
        elif len(current_txt) < len(quote): # Handles current_txt exceeding quote
            current_txt.append(key)

def main(screen):
    """
    Main call of other functions
    """
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(screen)
    wpm_test(screen)

wrapper(main)