"""
Searching for keywords via mic.
20 Dec 2022

Example adapted from here:
https://pypi.org/project/pocketsphinx/ 
"""

from pocketsphinx import LiveSpeech
import os

speech = LiveSpeech(keyphrase='robot', kws_threshold=1e-20)

for phrase in speech:
    print(phrase.segments(detailed=True))
    os.system(f"say 'Did you say, {str(phrase)}?'")