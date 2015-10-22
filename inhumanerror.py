"""

Input format
============
It looks like the input format might be hocr, which means we'll need
to devise some sort of manual parser to generate a temporary plaintext
file to work with in Python. That temporary file will need to be mapped
back onto the hocr format.  This will play heavily into how mapping
results back onto the input format is managed.

Mapping changes back onto the original file
===========================================

We work with a few indexes. The document_index will let us map changes
back onto the base document without losing meaningful whitespace.

This relies on the document being mappable to characters, e.g. a text file.
Furthermore we may need to depart from the whitespace delimited tokens
if the OCR software doesn't provide an amenable format.

document_index = index of the document being worked on. When we tokenize
                    the document by using the whitespace splitter, we want
                    to keep the document_index of the start of that word.
                    This allows us to map the changes back onto the 
                    document_index of that word.  
                    
                    1st tricky piece: 
                    how do we get the document index of the start of each word 
                    when we are doing the splitting?
                    i could write a manual split function, tracking the whitespace.
                    I could split one at a time from back to front, recording the 
                    index of each split.
                    1. reverse the string
                    2. split the string with maxsplit=1
                    3. (if you think on this it might work)

                    2nd Tricky piece:
                    This will be a little tricky because
                    we are NOT guaranteed that the new word
                    will be the same length as the old string.
                    It is easy enough to apply the changes last to first
                    (highest to lowest index) in order to preserve the index
                    for unchanged words as changes are made.




Steps
=====
1. Create a word frequency dictionary of the document.
        This word frequency dictionary should follow
        the same grammar subtracting rules as the
        dictionary search used to identify spelling errors.
2. Separate the document on whitespace and enumerate each word.
        Punctuation is left in the word, it affects the
        dictionary search and will be truncated inside that
        module as needed
        Enumeration gives an index for each word in the document.
        An enumeration can be easily unzipped and zipped to get
        an independent index if neceessary.
3. Use the dictionary against the whitespace separated document
        Add each error index to the potential errors list.
        The POTENTIAL ERRORS LIST is a list of indexes that
        may have errors.
4. Do a context check on short words.
        Rules:
            1. A short word is less than X characters (choose X)
            2. The word immediately before OR after the short
                word must exist somewhere else in the document.
                See the elephant example in this document.
        Q: What data source do we use for this?
        A: Use the document on itself, this may work because
                author style may create a sufficient overlap. 
        If a word fails a context check, add its index to the
        POTENTIAL ERRORS LIST.


Problems
========
If we let an author fix an entire passage, then we would
have to deal with merge conflicts. Instead we can create
a MANUAL ADD MODE, where an author can add an index to the
POTENTIAL ERRORS LIST, allowing the author to then edit
that index.
It may be worth it to allow an author to remove an index
from the potential errors list as well. May not be necessary
though.

Goals
=====
This is a short module designed to use human intelligence
to fix errors introduced by OCR.

In particular this script is designed to allow humans to
quickly proofread questionable words in the output
of Tesseract PDFs.

Usability
=========

We want to keep each word in its own context in the 
document. For example, humans will want to see the 15
words before a word and the 15 words after a word (maybe
less or more, but this is my initial guideline).

Navigation should always be free of data entry. I do
not know the best way to do this at a python raw input
console. I guess we could enter insert mode with 'i',
then exit insert mode with 'return'.  Users will want
to be able to backspace, I think this is on raw_input
by default.
Navigation modes: 
    n = next passage
    p = previous passage
    > = next index
    < = previous index
    i = insert mode
    q = quit and apply changes

When loading a file, the user must provide through argparse:
    1. input file
    2. output file
The user should be asked to verify each filename (y/n/q)
    y = continue
    n, q = quit with message "Aborted by user (n or q)."

Navigation between questionable passages is critical.
Even after a passage has been fixed, the reviewer should
still be able to navigate backwards and forwards one
passage at a time, back to that fixed passage.

On viewing a passage a reviewer should see:
    1. Passage Number out of / Passages to check
    2. original passage
    3. a summary of the computer error
    4. reviewer fixed passage (if available)
    
    "Passage 34 out of 89 passages with potential errors.
    ((
    exception for free index view (<, >):
    if passage not in POTENTIAL ERRORS LIST then:
    "Word 190 out of 10920 total words." 
    ))
    Raw: "Original Passage with errqrs, 30 words long"
    Current Word: errqr
    Fix (if provided): error
    Fix View: "Original Passage with errors, 30 words long"
    PLEASE WRITE YOUR FIX WITH NO QUOTES
    ALL PUNCTUATION WILL BE INCLUDED IN YOUR FIX
    LEADING AND TRAILING WHITESPACE ARE TRUNCATED
    >>>

It would be nice to tap the right arrow or left arrow to 
see the next or previous passage.
It would also be nice to have a manual mode where the 
reviewer can traverse the index of the document and view 
each word similarly to the error review mode. In this case, 
the language would need changed.

Ideas
=====

The list of letters allowed in english words is as follows:
    A-Za-z'-    (The apostrophe and hyphen are treated as letters)

NGSL is used for the dictionary: http://www.newgeneralservicelist.org/

Two Tests:
    a. A test for all Words == Dictionary Search (2 classes
            of errors)
        1. not elsewhere in document
        2. elsewhere in document
    b. A test for common words == Questionable Context
        words is whether they exist in a database
        of common words in the same local context.
        Ex.
            "I am an elephant"
            "I an am elephant"
        The phrase "I an " will not be found.
        The phrase "an am" will not be found.
        A human can easily find these.


Transcription error types:
    Lose a letter
    Garble a letter (lose+add indistinguishable but rarer)
    Add a letter
    (Any combination)

What about grammar errors?
    1. Exceptionally long sentences (over 15 words?)
    2. Short sentences that lose commas or spaces.
            This represents a much harder problem to discover.
    3. Missing apostrophes and double quotes that don't close.
            A whole pass could be dedicated to this.
            This grammar error can be considered a spelling error.

Preliminary Considerations:
    We want to know a few things about our data:
        1. Frequency of each word.
        2. Context (given by the text).  It will be necessary
            for us to look at 
    Holding it all in memory? Yes, for now.
        It's reasonable to keep the word frequency dictionary
        in memory, but it's less reasonable to keep a whole
        document of text in memory.  However, with modern
        systems, a huge book is only a few megabytes, so we
        can safely ignore this for now.
"""
import pickle
import os


def unpickle_dictionary(dict_filename):
    """ Simple utility to unpickle the NGSL dictionary.
    """
    with open(dict_filename, 'r') as f:
        dictionary = pickle.load(f)

    return dictionary


def automated_review_word(word, dictionary, errorlog_filename):
    """ Check if a word is in a list of words

    This module needs to be able to accept words with
    affixed punctuation and to remove that punctuation.

    For this, we will give the reviewing human three things:
    1. Original Context
    2. Raw Word
    3. Cleaned word, use a whitelist of characters: A-Za-z'-
    This should allow the reader to make choices about the
    passage.
    """
    if word in dictionary:
        return word
    else:
        with open(errorlog_filename, 'a') as f:
            f.write(word) + os.linesep


def review_word(word):
    """ Display a word and ask a human to fix it.

    Also, we want to see the word in the context of the 15 words 
    before it and the 15 words after it.
    """

    print "===== NEXT WORD ======"
    print "Is this word "

if __name__ == "__main__":

    # boilerplate argparse code is broken out of main
    import lib.inargs
    input_filename, output_filename = lib.inargs.args.i, lib.inargs.args.o

    # import the document in question in order. This will
    # need space separated so the reader can parse it.
    # see the spec, don't use this next line
    every_word_in_the_document = list()

    # The dictionary should be small and fast, use the
    # conversational english dictionary from class.
    data_folder = "data"
    dict_filename = "ngsl.pickle"
    dict_path_and_file = os.path.join(data_folder, dict_filename)

    # open up the New General Service List common english
    # words. Represents 95% of common english.
    dictionary = unpickle_dictionary(dict_path_and_file)

