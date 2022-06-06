import random
import json
import curses
import time
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
    screen.addstr(f"\nWPM: {wpm}")

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
    wpm = 0
    start_time = time.time()
    screen.nodelay(True) # Makes it so program doesn't keep waiting for keypress

    while True:
        time_elapsed = max(time.time() - start_time, 1) # max() so we don't get zero division error
        wpm = round(len(current_txt) / (time_elapsed /60)) / 5

        screen.clear()
        display_txt(screen, quote, current_txt, wpm)
        screen.refresh()

        if "".join(current_txt) == quote: # join() transforms current_txt list into a string
            screen.nodelay(False)
            break

        # Try block handles exception generated if program keeps waiting for a keypress
        try:
            key = screen.getkey()
        except:
            continue

        # Break if ESC key was pressed:
        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"): # Handles backspace
            if len(current_txt) > 0:
                current_txt.pop()
        elif len(current_txt) < len(quote): # Handles current_txt exceeding quote
            current_txt.append(key)
    screen.addstr(1, len(quote)+5, f"Author: {author}")

def main(screen):
    """
    Main call of other functions
    """
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(screen)
    wpm_test(screen)

    screen.addstr(2, 0, "You completed the text! Press any key to continue...")
    screen.getkey()

wrapper(main)