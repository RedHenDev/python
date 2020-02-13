"""
Example of a position tracker.
This can be thought of as
moving left, right, up, and down
on a grid of squares.

Thursday 13th February 2020
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

# Variables for holding
# previous X and previous Y.
# Used to calculate distance.
pX = myX
pY = myY

# Distance travelled so far.
d = 0

# Function to print position.
def printPos():
  global myX, myY
  print("PosX = " + str(myX))
  print("PosY = " + str(myY))

# Function to print distance.
def printDis():
  global d

  if d == 1 or d == -1:
    unit = "mile"
  else:
    unit = "miles"

  print("Distance = " + str(d) + " " + unit)

def drawGrid():
  global myX, myY
  global squaresX, squaresY

  counterX = 1
  counterY = 1

  while counterY <= squaresY:
    while counterX <= squaresX:
      if myX == counterX and \
      myY == counterY:
        print("[X]", end = "")
      else:
        print("[ ]", end = "") 
      counterX+=1
    counterX = 1
    counterY+=1
    print("")  

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
    
# Add up how far we have travelled.
def measureDistance():
  global d, myX, myY, pX, pY

  d = d + (abs(myX - pX)) + abs((myY - pY))

  # Record current position in 
  # 'previous' position variables.
  pX = myX
  pY = myY

# Check whether we have hit edge of
# territory. If so, do not move.
def boarderCheck():
  global squaresX, squaresY
  global myX, myY

  if myX < 1:
    myX = 1
  elif myX > squaresX:
    myX = squaresX
  
  if myY < 1:
    myY = 1
  elif myY > squaresY:
    myY = squaresY

# Before we begin the game,
# print position, and set
# status to ALIVE.
printPos()
alive = True

# Main game loop.
# This WHILE loop will loop until
# alive variable is False.
while alive == True:
  drawGrid()
  ans = input("> ")
  checkAnswer(ans)
  boarderCheck()
  measureDistance()
  printDis()
  printPos()

# If we are here, user must
# have exited, since we
# are outside WHILE loop.
print("You have ended the game. Thank you.")
