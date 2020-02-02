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

        # Return user's choice as string.
        # If they enter incoherent input, prompt with available answers.
        if ua == ans1: return ans1
        elif ua == ans2: return ans2
        elif ua == "s": return "s"
        elif ua == "x" or ua == "q" or ua == "exit": return "x"
        else:
                print("\n" + "Pardon? Choose either " + ans1 + " or " + ans2 + ". Thank you.\n" )
                return 3


# Assemble question, based on level.
# May need corresponding function that handles the answers given.
def findQuestion():
        global level
        if level == 1:
                return assembleQuestion("The forest is dark and quiet. Move on, or retreat for supplies?",
                             "move", "retreat")
        elif level == 2:
                return assembleQuestion("Quick feet! You've made it far already. Press on to the heart of the forest?",
                             "yes", "no")
        elif level == 3:
                return assembleQuestion("You have packed well. But there's space for one more item: torch or cloak?",
                             "torch", "cloak")
        elif level == 4:
                return assembleQuestion("The darkness grows. You slow down. You hear a scream. Run towards, or away?",
                             "towards", "away")
        elif level == 5:
                return assembleQuestion("You find a strange opening in the trees. Enter or walk on?",
                             "enter", "walk")

# Looks at answer given (_a) and returns new level.
def junctionBox(_a):
        global level
        if level == 1 and _a == "move": return 2
        elif level == 1 and _a == "retreat": return 3
        elif level == 2 and _a == "yes": return 4
        elif level == 2 and _a == "no": return 5
        elif level == 3: return 5
        elif level == 5 and _a == "walk": return 2
        elif level == 4 and _a == "away": return 5
        elif level == 4 and _a == "towards": return 3
        elif level == 5 and _a == "enter": return 1
        else: return level

def damage():
        global health
        health -= randint(1,15)

level = 1
printStatus()

# Our game loop.
while alive:
        damage()
        if health <= 0:
                alive = False
                break
        a = findQuestion()
        # a = input(getQuestion()).strip()
        if a != "x" and a != 3 and a!= "s":
                print("You chose to", a)
                print("")
        if a == "x" or a == "q" or a == "exit": alive = False
        elif a == "s":
                printStatus()
        # Determine new level based on answer.
        else: level = junctionBox(a)
        

printStatus()

print("You are dead, or have exited the game.")
