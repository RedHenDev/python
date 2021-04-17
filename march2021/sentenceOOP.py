"""Random sentence gen with classes"""
""" March 27th 2021 """

import random
from enum import Enum
from nltk.corpus import wordnet as wn

class Type(Enum):
    PREPOSITION = 1
    NOUN = 2
    VERB = 3

determiners = [
                "the",
                "this",
                "that",
                "her",
                "his",
                "our",
                "your",
                "a",
                "my"]

adjectives = [
                "big",
                "nice",
                "little",
                "enchanting",
                "discreet",
                "welcome",
                "affluent"
                        ]

nouns = [
                "Dad",
                "dog",
                "dinosaur",
                "nose",
                "antler",
                "frog",
                "gemstone"
                        ]

all_nouns = []
for synset in wn.all_synsets(wn.NOUN):
    all_nouns.extend(synset.lemma_names())

verbs = [
                "dodges",
                "digests",
                "remembers",
                "snatches",
                "acuses",
                "forgets",
                "squashes"
                        ]

"""Part of a clause"""
class Phrase:
    def __init__(this, whatType):
        this.type = whatType
        this.mess = this.generate()

    def render(this):
        print(this.mess)

    def generate(this):
        if this.type == Type.NOUN:
            return  (" " + random.choice(determiners) +
                        " " + random.choice(adjectives) +
                        " " + random.choice(all_nouns))
        elif this.type == Type.VERB:
            return " " + random.choice(verbs)

newPhrase = Phrase(Type.NOUN)
anotherPhrase = Phrase(Type.VERB)
finalPhrase = Phrase(Type.NOUN)

newPhrase.mess

newPhrase.mess += anotherPhrase.mess + finalPhrase.mess + "."

newPhrase.render()


