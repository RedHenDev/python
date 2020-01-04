"""Text adventure game 0.2 4/1/20"""

""" 
I'm interested in working out
two things: (1) game architecture
                 (2) generalising functionality
"""

from random import *

health = 100
alive = True
level = 0

userName = input("Hi there. You'll want to tell me your name, I guess?").strip()

if len(userName) > 0:
        print("Hi, " + userName)
else: alive = False




def printStatus():
        print("")
        print("***")
        print("")
        
        print("Health = " + str(health))
        print("Name = " + userName)
        print("Level = " + str(level))

        print("")
        print("(x to EXIT)")
        print("***")
        print("")
        
def getQuestion():
        if level == 1:
                return "Nice name. Walk left or right?"
        elif level == 2:
                return "Wow -- you got to level 2! Eat or sleep now?"
        elif level == 3:
                return "This is the last level. Return to base, or fly to moon?"
        

def assembleQuestion(question, ans1, ans2):
        """prints input question and returns which of the two answers user chose"""
        print("\n")
        ua = input(question + "\n" + ans1 + " or " + ans2 + "?").strip().lower()

        # Return user's choice as integer, 1 or 2.
        # If they enter incoherent input, prompt with alternative and call function recursively.
        if ua == ans1: return 1
        elif ua == ans2: return 2
        elif ua == "x": return 0
        else:
                print("\n" + "Pardon? Choose either " + ans1 + " or " + ans2 + ". Thank you.")
                assembleQuestion(ans1, ans2, question)
        

def damage():
        global health
        health -= randint(1,15)

while alive:
        damage()
        level = randint(1,3)
        printStatus()
        a = assembleQuestion("The forest is dark and quiet. Move on, or return for supplies?",
                             "move", "return")
        # a = input(getQuestion()).strip()
        if a == 0: alive = False

print("You have exited the game.")
