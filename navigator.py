"""
Mock up the navigation aspects of inhumanerror.


We'll use some a while loop that accepts stdin in real time.

Navigation modes: 
    (right arrow) = next passage
    (left arrow) = previous passage
    > = next index
    < = previous index
    i = insert mode
    q = quit and apply changes


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

key = ''
while key != 113:

    win.addstr(1,1,message1)

    prevKey = key
    event = win.getch()
    if event == -1:
        pass
    else:
        key = event
        win.addch(18,58,event)

curses.endwin()


def navigator():
    pass


if __name__ == "__main__":
    pass


