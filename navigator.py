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
    60 <
    62 >
    104 h
    105 i
    113 q  # currently handled by external loop
    RIGHT_ARROW is a const in curses
    LEFT_ARROW is a const in curses

This navigator is designed to allow the user easy access

"""
import curses

from curses import KEY_LEFT, KEY_RIGHT

curses.initscr()
curses.noecho()

win = curses.newwin(20,60,0,0)
win.keypad(1)
win.nodelay(1)
win.border(0)

message1 = "This is the top line."
message = "This is a message."

index = 0
mywords = list(range(100))

events = (60, 62, 104, 105, KEY_LEFT, KEY_RIGHT)

event = -1
while event != 113:

    prev_event = event
    event = win.getch()

    if event == -1:
        continue # This handles no new input for the nodelay(1) setting.

    # redraw for ANY user input right now
    win.clear()
    win.border(0)

    if event in events:

        # In this design, each function could return a list of strings.
        # Those strings could be assigned to m1, m2, m3, m4, m5 (five messages)
        if event == 60:
            display_index_left()
        elif event == 62:
            display_index_right()
        elif event == 104:
            display_passage_left()
        elif event == 105:
            display_passage_right()

        # This could be done for a list of strings over the index up to a max height.
        # consider a message truncator for messages that are too long.
        # you can easily truncate messages to length(=50) with win.addnstr(1,1,message,50)
        win.addstr(1,1,m1)
        win.addstr(2,1,m2)
        win.addstr(3,1,m3)
        win.addstr(4,1,m4)
        win.addstr(5,1,m5)
        win.refresh()

    # let the user know what they pressed.
    win.addch(18,56,event)
    #win.addstr(18,50,str(event)) # showes the integer for the event.

curses.endwin()


def display_index_left():
    pass

def display_index_right():
    pass

def display_passage_left():
    pass

def display_passage_right():
    pass


if __name__ == "__main__":
    pass


