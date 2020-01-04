"""Text adventure game 0.1 4/1/20"""

""" 
I'm interested in working out
two things: (1) game architecture
                 (2) generalising functionality
"""

from random import *

userName = input("Hi there. You'll want to tell me your name, I guess?").strip()

if userName != " ":
        print("Hi, " + userName)

# Right -- we'll want a game loop, then.

health = 100
alive = True
level = 0

def printStatus():
        print("")
        print("***")
        print("")
        
        print("Health = " + str(health))
        print("Name = " + userName)
        print("Level = " + str(level))

        print("")
        print("***")
        print("")
        
def getQuestion():
        if level == 1:
                return "Nice name. Walk left or right?"
        elif level == 2:
                return "Wow -- you got to level 2! Eat or sleep now?"
        elif level == 3:
                return "This is the last level. Return to base, or fly to moon?"
        

def damage():
        global health
        health -= randint(1,15)

while alive:
        damage()
        level = randint(1,3)
        printStatus()
        a = input(getQuestion()).strip()
        if a == "x": alive = False

print("Well played! Seeeeeya!")
