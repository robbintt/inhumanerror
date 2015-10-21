"""
This is a short module designed to use human intelligence
to fix error introduced by OCR.

In particular this script is designed to allow humans to
quickly proofread questionable words in the output
of Tesseract PDFs.

We want to keep each word in its own context in the 
document. For example, humans will want to see the 15
words before a word and the 15 words after a word.

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


def unpickle_dictionary(dict_filename):
    """ Simple utility to unpickle the NGSL dictionary.
    """
    with open(dict_filename, 'r') as f:
        dictionary = pickle.load(f)

    return dictionary


def automated_review_word(word, dictionary, errorlog_filename):
    """ Check if a word is in a list of words
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

    # current spec is a newline separated list of words.
    # all errors are feeding through review word right now.
    errorlog_filename = "errors.log"

    # The dictionary should be small and fast, use the
    # conversational english dictionary from class.
    dict_filename = "ngsl.pickle"

    every_word_in_the_document = list()


    dictionary = unpickle_dictionary(dict_filename)

    print dictionary

