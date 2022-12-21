"""
PocketSphinx
20th Dec 2022
Hello Parrot
"""

from pocketsphinx import LiveSpeech
import os

for phrase in LiveSpeech():
    os.system("say " + str(phrase))
    print(phrase)