"""
Mock up the navigation aspects of inhumanerror.

Curses supports color, so consider that.

This needs a context manager! If curses breaks, it screws up the terminal.


TODO:

    Make a view method for viewing the current index.  The four navigation
    methods simply update the index by incrementing or decrementing by 1 or
    the amount to the next potential error, then they show this view method.
    The same view method should also be used when starting up (view the first
    potential error), and when leaving the help screen (view the current index).


Options
=======

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


def display_index_left():
    pass

def display_index_right():
    pass

def display_passage_left():
    pass

def display_passage_right():
    pass

def enter_insert_mode():
    pass

def display_help():
    """ the curses view for help 
    """
    m1 = "Navigation:"
    m2 = "'<' - Move left one index"
    m3 = "'>' - Move right one index"
    m4 = "left arrow - Move left one passage"
    m5 = "right arrow - Move right one passage"
    m6 = "'i' - insert mode, update the word at the current index"
    m7 = "'h' - This help menu"
    messages = [m1, m2, m3, m4, m5, m6, m7]

    return messages

def punctuation_stripper(word):
    """ Strip punctuation from before or after a word.

    This function is intended for use when identifying words.
    In this project, all text mutation should be done by the human reviewer.
    """
    word = word.strip('\,.!?;"')

    # strip enclosing single quotes if there is on on the left.
    if word[0] = "'":
        word = word.strip("'")     
    else:
        pass # don't strip a apostrophe representing plural ownership

    return word




def build_word_frequency_dict(source):
    """ Build a word frequency dict from a source list of words.

    Use a function that strips words of any leading or trailing punctuation.
    """
    word_frequency_dict = {}
    for word in source:
        word = punctuation_stripper(word)
        times = word_frequency_dict.get(word, 0)
        times += 1
        word_frequency_dict[word] = times

    return word_frequency_dict


if __name__ == "__main__":
    """
    The control loop must maintain what index the user is currently on.

    Index refers to what word in the passage the user is on.

    A separate list of errors is maintained.

    Each jump function can manipulate the index.

    > will increment the index by 1 and redraw
    < will decrement the index by 1 and redraw
    left arrow will find the next lowest potential error index and redraw
    right arrow will find the next highest potential error index and redraw

    The index can then be increased or decreased based on the input the user gives.

    When the user uses 'i' the screen must be redrawn and input must be taken on
    the current index.
    
    Currently the 'h' option draws help, but there's no option to redraw the current index.
    """

    my_input_file = "sample.txt"

    with open(my_input_file, 'r') as f:
        raw_text = f.read()

    whitespaced_text = raw_text.split()
    parsed_text_index, parsed_text = zip(*enumerate(whitespaced_text))

    print parsed_text_index, parsed_text
    print whitespaced_text

    word_frequency_dict = build_word_frequency_dict(whitespaced_text)
    # build_potential_errors(parsed_text_index, word_frequency_dict)

    print word_frequency_dict

    # an index tracks our place... it hasn't been implemented
    index = 0

    # Curses Setup
    curses.initscr()
    curses.noecho()
    win = curses.newwin(20,60,0,0)
    win.keypad(1)
    win.nodelay(1)
    win.border(0)
    # always display help at bottom.
    win.addstr(18,1,"Press 'h' for help.")

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

            # messages is used to provide actual input.
            messages = list()
            if event == 60:
                display_index_left()
            elif event == 62:
                display_index_right()
            elif event == KEY_LEFT:
                display_passage_left()
            elif event == KEY_RIGHT:
                display_passage_right()
            elif event == 104:
                messages = display_help()
            elif event == 105:
                enter_insert_mode()

            # Add up to 10 messages, truncating after 58 characters.
            for i, message in enumerate(messages):
                if i > 10:
                    break
                win.addnstr(i,1,message, 58)
                # win.addstr(i,1,message)

        ### THIS IS THE BOTTOM DISPLAY OF THE WINDOW
        # always display help at bottom.
        win.addstr(18,1,"Press 'h' for help.")
        # let the user know what they pressed.
        win.addch(18,56,event)
        #win.addstr(18,50,str(event)) # showes the integer for the event.
        win.refresh()


    curses.endwin()


