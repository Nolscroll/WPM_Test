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

def wpm_test(screen):
    """
    The WPM test itself
    """
    with open("quotes.json") as q:
        author, quote = random.choice(json.load(q)["quotes"]).values()
    current_txt = []

    while True:
        screen.clear()
        screen.addstr(quote)

        for char in current_txt:
            screen.addstr(char, curses.color_pair(1))

        screen.refresh()

        key = screen.getkey()

        # Break if ESC key was pressed:
        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"): # Handles backspace
            if len(current_txt) > 0:
                current_txt.pop()
        else:
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