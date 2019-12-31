

""" Generating random sentences from arrays of words. """
""" Monday 30th December 2019 """

from random import *

# In python, the compound data type of an array is called a list.

nouns = ["man", "goose", "banana", "plant", "egg", "dinosaur", "apple",
         "horse", "history", "opinion", "ant", "elephant", "elf", "onion",
         "otter", "insect", "igloo", "irritant", "island", "sentence", "Dot"]

verbs = ["sees", "finds", "likes", "chases", "eats", "talks with",
         "understands", "brings", "watches", "denies", "delivers",
         "creates", "maintains", "praises", "saves", "teaches",
         "greets", "welcomes", "solves", "thanks", "breaks",
         "scratches", "rejects", "picks", "accepts", "fights",
         "licks", "paints", "tricks"]

determiners = ["my", "your", "his", "her", "our",
               "the", "a", "that", "this", "their", "Dot's", "the"]


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

def newMessage():
    """ generate a new random sentence and print it """

    dR = choice(determiners) + " "
    d2R = choice(determiners) + " "
    nR = choice(nouns) + " "
    oR = choice(nouns) + "."
    vR = choice(verbs) + " "

    message =   dR + nR + vR + d2R + oR
    
    print(capitalizeLetter(0,message))

def capitalizeLetter(n, string):
    """ capitalize letter at n in string, return new string with this change """

    targetL = string[n]
    newL = targetL.upper()
    newString = string.replace(targetL, newL, 1)

    return newString

def anCheck(det, noun):
    """ If det is 'a' and noun begins with vowel, return 'an' """

    # Assume det is 'a'.
    returnValue = True

# Why doesn't the below work?
##    if str(det) != str("a"):
##        returnValue = False

   # print("det =" + det + " ASCII = " + str(ord(det[0])))

    # Is determiner only 1 letter long and start with 'a'?
    if len(det) > 1 or ord(det[0]) != 97:
        returnValue = False

   # print(len(det)-1, ord(det[0]), returnValue)
    
    # First, makes sure string is lowercase. 
    lcNoun = noun
    #lcNoun.strip()
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
    """
    # Randomly choose words from lists.
    dR = choice(determiners) + " "
    d2R = choice(determiners) + " "
    a2R = choice(adjectives) + " "
    nR = choice(nouns) + " "
    oR = choice(nouns) + "."
    vR = choice(verbs) + " "

    # Randomize whether to apply adjective.
    # The aim should be to use this twice etc.
    useAdjective = False    # Game is to turn this true.
    if random() > 0.5:
        useAdjective = True

    # Concatenate our strings.
    if useAdjective:
        # Check whether determiners need to change from 'a' to 'an'.
        if anCheck(d2R, a2R) == True:
            d2R = "an" + " "
        if anCheck(dR, nR) == True:
            dR = "an" + " "
        message = dR + nR + vR + d2R + a2R + oR
    else:
        # Check whether determiners need to change from 'a' to 'an'.
        if anCheck(d2R, oR) == True:
            d2R = "an" + " "
        if anCheck(dR, nR) == True:
            dR = "an" + " "
        message = dR + nR + vR + d2R + oR
    """

    # Ugly, but the first pass through.
    # We need, I think, something like a
    # 'phrase builder'. E.g. NounPhrase, which could be
    # used for both the subject and object elements.
    
    message = nounPhrase() + " " \
              + verbPhrase() + " " \
              + nounPhrase() + "."

    # NB python's own capitalize function. Nice.
    # message.capitalize()
    return (capitalizeLetter(0, message))

def verbPhrase():
    """ return a verb, basically """

    return choice(verbs)

def nounPhrase():
    """ concatenate a determiner, optional adjective, and noun """

    returnMessage = choice(determiners)

    if random() > 0.3: useAdj = True
    else: useAdj = False

    newNoun = choice(nouns)

    if useAdj:
        newAdj = choice(adjectives)
        returnMessage = anCheck(returnMessage, newAdj) + \
                        " " + newAdj + " " + newNoun
    else:
        returnMessage = anCheck(returnMessage, newNoun) + \
                        " " + newNoun

    return returnMessage


