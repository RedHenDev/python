""" Random critical statement maker """

import random

# First, we need to create a list of features and other elements.

features = [
    'tone',
    'phrase',
    'clause',
    'adjective',
    'verb',
    'adverb',
    'connective',
    'imagery',
    'symbol',
    'idea',
    'sentence',
    'notion'
    ]

adjectives = [
    'sombre',
    'poignant',
    'abrupt',
    'elegaic',
    'sympathetic',
    'aggressive',
    'bright',
    'dull',
    'lurid',
    'prosaic',
    'vibrant',
    'energetic',
    'lethargic',
    'elusive',
    'naive'
    ]

determiners = [
    'this',
    'the'
    ]

connectives = [
    'though',
    'whereas',
    'but',
    'so',
    'since',
    'due to the fact that',
    'for',
    'and',
    ';'
    ]

def genStatement():
    # First, grab random determiner.
    # And we make sure the first letter is capitalized.
    det = random.choice(determiners).capitalize()

    adj = " "
    if random.randint(0,100) > 75: adj = " " + random.choice(adjectives) + " "

    adj2 = random.choice(adjectives)
    
    # Now, a random feature.
    feat = random.choice(features)

    # Connective - correcting for semicolon.
    con = ""
    conTemp = random.choice(connectives) 
    if conTemp != ";":
        con = ", " + conTemp + "..."
    else: con = "; " + random.choice(connectives) + ', ...'

    # Return the concatenized string.
    return det + adj + feat + " is more " + adj2 + con + "\n"

snibbly = ""

while snibbly != "x":
    snibbly = input("Press RETURN for new critical statement (or x to exit).")
    # As long as 'x' is not inputted, print a new random critical statement.
    if snibbly != "x": print(genStatement())

print("You have exited. Thanks, buddy.")
    

