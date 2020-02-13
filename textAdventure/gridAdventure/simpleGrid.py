"""
Example of a position tracker.
This can be thought of as
moving left, right, up, and down
on a grid of squares.

Thursday 13th February
2020
Mr New

Suggested developments:
1) Prevent user going off-grid
2) Keep track of how many squares
   user has travelled.
3) Draw a grid with player position
   marked as an 'X' -- in text.
4) Have different items, such as
   a key, hidden on different
   squares. Print if player finds.
5) Have a monster chase the player!
"""

# How many squares in our 
# territory, X and Y?
squaresX = 4
squaresY = 4

# We can calculate the total number
# of squares :)
totalS = squaresX * squaresY

# Print total number of squares.
print("Territory = " + str(totalS) + " squares")

# Position of user, X and Y.
# We'll start at square 1,1.
myX = 1
myY = 1

# Function to print position.
def printPos():
  global myX, myY
  print("PosX = " + str(myX))
  print("PosY = " + str(myY)) 

# Check input from user and
# carry out their instructions.
def checkAnswer(a):
  global myX, myY, alive
  
  if a == "x":
    alive = False
  elif a == "w":
    myY = myY - 1
  elif a == "s":
    myY = myY + 1
  elif a == "a":
    myX = myX - 1
  elif a == "d":
    myX = myX + 1
    
    
# Before we begin the game,
# print position, and set
# status to ALIVE.
printPos()
alive = True

# Main game loop.
# This WHILE loop will loop until
# alive variable is False.
while alive == True:
  ans = input("> ")
  checkAnswer(ans)
  printPos()

# If we are here, user must
# have exited, since we
# are outside WHILE loop.
print("You have ended the game. Thank you.")
