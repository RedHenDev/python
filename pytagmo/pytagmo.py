

""" Generating random sentences from arrays of words. """
""" Monday 30th December 2019 """

from random import *

# In python, the compound data type of an array is called a list.

nouns = ["man", "goose", "banana", "plant", "egg", "dinosaur", "apple",
         "horse", "history", "opinion", "ant", "elephant", "elf", "onion",
         "otter", "insect", "igloo", "irritant", "island", "sentence", "Dot",
         "weekend", "bus", "time", "idea", "phrase", "clause", "day",
         "house", "England", "Brian"]

verbs = ["sees", "finds", "likes", "chases", "eats", "talks with",
         "understands", "brings", "watches", "denies", "delivers",
         "creates", "maintains", "praises", "saves", "teaches",
         "greets", "welcomes", "solves", "thanks", "breaks",
         "scratches", "rejects", "picks", "accepts", "fights",
         "licks", "paints", "tricks"]

determiners = ["my", "your", "his", "her", "our",
               "the", "a", "that", "this", "their", "Dot's", "the"]

# This is a tuple. My first :)
prepositions = (
    "in",
    "over",
    "next to",
    "within",
    "after",
    "inside",
    "around",
    "between",
    "from",
    "with",
    "by",
    "to",
    "in"
    )


adjectives = [
	'green',
	'pink',
	'crystalline',
	'ugly',
	'friendly',
	'spicy',
                "naughty",
	'unwelcome',
	'lovely',
	'delicious',
	'serpentine',
	'slimy']

message = ""



def capitalizeLetter(n, string):
    """ capitalize letter at n in string, return new string with this change """

    targetL = string[n]
    newL = targetL.upper()
    newString = string.replace(targetL, newL, 1)

    return newString

def anCheck(det, noun):
    """ If det is 'a' and noun begins with vowel, return 'an'.
         Else, just return the passed in determiner (det). """

    # Assume det is 'a'.
    returnValue = True

    # Is determiner only 1 letter long and start with 'a'?
    if len(det) > 1 or ord(det[0]) != 97:
        returnValue = False
    
    # First, makes sure string is lowercase. 
    lcNoun = noun
    lcNoun = lcNoun.lower()
    an = "an"

    # If we find a vowel return true.
    if lcNoun[0]=="a" and returnValue:
        return an
    elif lcNoun[0]=="e" and returnValue:
        return an
    elif lcNoun[0]=="i" and returnValue:
        return an
    elif lcNoun[0]=="o" and returnValue:
        return an
    elif lcNoun[0]=="u" and returnValue:
        return an
    else:
        return det


def randomSentence():
    """ Generate and return new random sentence """
    
    message = nounPhrase(0.3) + " " \
              + verbPhrase() + " " \
              + nounPhrase(0.7) + " " \
              + adverbialPhrase() + "."

    # NB python's own capitalize function. Nice.
    # Actually -- not nice! It lowers() the rest of the string!
    # message.capitalize()
    return (capitalizeLetter(0, message))

def verbPhrase():
    """ return a verb, basically """

    return choice(verbs)

def adverbialPhrase():
    """ concatenate a preposition and noun phrase """

    return choice(prepositions) + " " + nounPhrase(0.8)

def nounPhrase(adjBias):
    """ concatenate a determiner, optional adjective, and noun """

    # First, grab a random determiner from list.
    returnMessage = choice(determiners)

    # Second, decide whether to use adjective.
    # adjBias (0-1) is likelihood to use adjective.  
    if random() < adjBias: useAdj = True
    else: useAdj = False

    # Third, grab a random noun from list.
    newNoun = choice(nouns)

    # Concatenate elements, with or without adjective, and
    # check whether indefinite article 'an' must replace 'a'.
    if useAdj:
        newAdj = choice(adjectives)
        returnMessage = anCheck(returnMessage, newAdj) + \
                        " " + newAdj + " " + newNoun
    else:
        returnMessage = anCheck(returnMessage, newNoun) + \
                        " " + newNoun

    # Finally, return finished string.
    return returnMessage

##############################################
##############################################
##############################################
# Deprecated -->

def newMessage():
    """ generate a new random sentence and print it """

    dR = choice(determiners) + " "
    d2R = choice(determiners) + " "
    nR = choice(nouns) + " "
    oR = choice(nouns) + "."
    vR = choice(verbs) + " "

    message =   dR + nR + vR + d2R + oR
    
    print(capitalizeLetter(0,message))


