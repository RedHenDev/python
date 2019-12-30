

""" Generating random sentences from arrays of words. """
""" Monday 30th December 2019 """

from random import *

# In python, the compound data type of an array is called a list.

nouns = ["man", "goose", "banana", "plant", "egg", "dinosaur"]

verbs = ["sees", "finds", "likes", "chases", "eats", "talks with"]

determiners = ["my", "your", "his", "her", "our",
               "the", "a", "that", "this"]

message = ""

def newMessage():
    """ generate a new random sentence and print it """

    dR = choice(determiners) + " "
    d2R = choice(determiners) + " "
    nR = choice(nouns) + " "
    oR = choice(nouns) + "."
    vR = choice(verbs) + " "

    message =   dR + nR + vR + d2R + oR
    
    print(message)

newMessage()
