import random
import json
import curses
import time
from math import ceil
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

def display_txt(screen, quote, author, current_txt, wpm=0):
    """
    Displays quote and typed text to the terminal screen
    """
    screen.addstr(quote)
    screen.addstr(f"\nWPM: {wpm}")
    screen.addstr(f"\nAuthor: {author}")

    for i,char in enumerate(current_txt):
        correct_char = quote[i]

        # Select text color based on correctness:
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
            if char == " ":
                color = curses.color_pair(3)
        try:
            screen.addstr(0, i, char, color)
        except:
            pass # attempt at fixing error after many keypresses

def wpm_test(screen):
    """
    The WPM test itself
    """
    with open("quotes.json") as q:
        author, quote = random.choice(json.load(q)["quotes"]).values()
    quote = quote.strip() # Remove whitespace at end of quotes
    current_txt = []
    wpm = 0
    start_time = time.time()
    screen.nodelay(True) # Makes it so program doesn't keep waiting for keypress

    while True:
        time_elapsed = max(time.time() - start_time, 1) # max() so we don't get zero division error
        wpm = round(len(current_txt) / (time_elapsed /60)) / 5

        screen.clear()
        display_txt(screen, quote, author, current_txt, wpm)
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
        
    return ceil(len(quote) / 79) + 3

def main(screen):
    """
    Main call of other functions
    """
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)

    start_screen(screen)
    byeLine = wpm_test(screen)

    screen.addstr(byeLine, 0, "You completed the text! Press any key to continue or ESC to end...")
    screen.getkey()

wrapper(main)