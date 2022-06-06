import random
import json
import curses
from curses import wrapper

def start_screen(screen):
    screen.clear()
    screen.addstr("Welcome to the WPM Test!")
    screen.addstr("\nPress any key to begin!")
    screen.refresh()
    screen.getkey()

def wpm_test(screen):
    with open("quotes.json") as q:
        author, quote = random.choice(json.load(open('quotes.json'))["quotes"]).values()


def main(screen):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(screen)
    wpm_test(screen)

wrapper(main)