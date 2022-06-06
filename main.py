import curses
from curses import wrapper

def main(screen):
    screen.clear()
    screen.addstr("Hello world!")
    screen.refresh()
    screen.getkey()

wrapper(main)