"""Text adventure game 0.3 4/1/20"""

""" 
I'm interested in working out
two things: (1) game architecture
                 (2) generalising functionality
"""

from random import *
from time import *

health = 100
alive = True
level = 0

userName = input("Hi there. You'll want to tell me your name, I guess? > ").strip()

if len(userName) > 0:
        print("Hi, " + userName)
else: alive = False




def printStatus():
        print("")
        print("***")
        print("")

        print("Name = " + userName)
        print("Level = " + str(level))
        print("Health = " + str(health))

        print("")
        print("(s for STATUS)")
        print("(x to EXIT)")
        print("***")
        #print("")
        
def getQuestion():
        if level == 1:
                return "Nice name. Walk left or right?"
        elif level == 2:
                return "Wow -- you got to level 2! Eat or sleep now?"
        elif level == 3:
                return "This is the last level. Return to base, or fly to moon?"
        

def assembleQuestion(question, ans1, ans2):
        """prints input question and returns which of the two answers user chose"""
        print("")
        ua = input(question + "\n" + ans1 + " or " + ans2 + "? > ").strip().lower()

        # Return user's choice as integer, 1 or 2.
        # If they enter incoherent input, prompt with alternative and call function recursively.
        if ua == ans1: return ans1
        elif ua == ans2: return ans2
        elif ua == "s": return "s"
        elif ua == "x": return "x"
        else:
                print("\n" + "Pardon? Choose either " + ans1 + " or " + ans2 + ". Thank you.\n" )
                return 3
                
def damage():
        global health
        health -= randint(1,15)

level = randint(1,3)
printStatus()

# Our game loop.
while alive:
        damage()
        if health <= 0:
                alive = False
                break
        a = assembleQuestion("The forest is dark and quiet. Move on, or retreat for supplies?",
                             "move", "retreat")
        # a = input(getQuestion()).strip()
        if a != "x" and a != 3 and a!= "s":
                print("You chose to", a)
                print("")
        if a == "x": alive = False
        elif a == "s":
                level = randint(1,3)
                printStatus()
        

print("You have exited the game.")
