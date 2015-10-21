"""
Mock up the navigation aspects of inhumanerror.

Curses supports color, so consider that.

Navigation modes: 
    (right arrow) = next passage
    (left arrow) = previous passage
    > = next index
    < = previous index
    i = insert mode
    q = quit and apply changes


Characters:
    602 <
    622 >

This navigator is designed to allow the user easy access

"""
import curses

from curses import KEY_LEFT, KEY_RIGHT

curses.initscr()

win = curses.newwin(20,60,0,0)
win.keypad(1)
curses.noecho()
win.border(0)
win.nodelay(1)

message1 = "This is the top line."
message = "This is a message."

index = 0
mywords = list(range(100))

events = (602, 622, KEY_LEFT, KEY_RIGHT, 'i', 113)

event = ''
while event != 113:

    prev_event = event
    event = win.getch()

    if event == -1:
        continue # This handles no new input for the nodelay(1) setting.

    """
    if event in events:
        # win.clear()

        if event == 602:
            # display important stuff.
            win.addstr(1,1,message1)
            win.addstr(2,1,message)
            win.addstr(3,1,message)
            win.addstr(4,1,message)
            win.addstr(5,1,message)
    """


    win.addch(18,58,event)
    win.addstr(18,51,str(event))

curses.endwin()


def navigator():
    pass


if __name__ == "__main__":
    pass


