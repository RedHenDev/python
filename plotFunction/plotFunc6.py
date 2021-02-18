

# So, the aim here is to
# define a mathematical function
# and then, to begin with, output
# return values as each new input
# is given by the user.

""" plotFunc 6 """

""" Here, we aim to try different function equations. """

# Math module used for floor() in version 1.0.
from math import *
import time
from graphics import *

# Our input value. I believe this will be set to -350 at start of loop (edge of canvas).
x = float(0)
# Our current value for x.
newX = float(0)
# Our current increment value.
iX = float(0.01)
# Exponential degree, when using this function.
n = 0

# Rendering scalar.
scalar = 100


# Set previous point location to above left of draw window.
prevPXY = Point(-350,-350)

# Our integer-cum-bool for while looping indefinitely.
looping = 1

# Create our graphics window. Thanks graphics.py :)
win = GraphWin("",700,700)
win.setBackground(color_rgb(0,101,101))
yLine = Line(Point(350,0), Point(350,700))
xLine = Line(Point(0,350), Point(700,350))
yLine.setOutline("gray")
xLine.setOutline("yellow")
yLine.draw(win)
xLine.draw(win)
cir = Circle(Point(350,350), 42)
cir.setOutline("black")
cir.draw(win)

def func(_x):
    #if _x==0: return float(0)
    """ Exponential """
    #global: n
    #return float(_x**n)
    """ Hyperbola. """
    return float(1/_x)
    #return float(_x**3)
    #return float(_x**2)
    #return float(_x * sin(_x/70 + _x/10))
    #return float(_x**2 + 2)
    #return float(tan(_x))
    #return 6*(_x**2) + (11*_x) - 35;
    #return 1/(_x**2)
    #return 5
    #return -1/_x**2
    """ Oblique asymptote. """
    #x2 = (_x * _x) - _x - 2
    #return x2/_x
def checkInput():
    whatKey = win.checkKey()
    if whatKey.lower() == "q" or whatKey.lower() == "x":
        win.close()
        return True
    else: return False

# Loop continues indefinitely.
while looping != 0:
    
    if looping == 1:
        startX = x = -1

        newX = float(x)
        # OK, we have now taken initial X value.

    # Have we looped through at least once?
    if looping == 2:
        # Increment current X value by increment value.
        newX += float(iX)
    else:
        newX = float(x) # Don't increment first time through :)

    # Print output Y to screen; function is called in print's string concatenation.
    #print("Thanks. When x = " + str(float(newX)) + " y = " + \
    #     str(func(float(newX))) + " ")
    prevY = func(float(newX - float(iX)))
    
    y = func(float(newX))
  
    print("x: " + str(float(newX)) + " y: " + str(y))
    
    pxy = Point(350+float(newX)*scalar, 350-(func(float(newX))))
        
    # Draw line from previous to new points. For smoothness.
    if looping == 1:
        newLine = Line(pxy, pxy)
    else: newLine = Line(pxy, prevPXY)
    newLine.setOutline("white")
    newLine.setWidth(3) # Stroke weight of line.
    newLine.draw(win)
    # Record previous point.
    prevPXY = pxy
    
    if (prevY < 0 and y > 0) or (prevY > 0 and y < 0): print(newX)
    
    #pCir = Circle(pxy, 0.5)
    #pCir.setOutline("white")
    #pCir.setFill("white")
    #pCir.draw(win)
    # Now how to pause a short time?
    # time.sleep(0.001)
    if checkInput(): break
   

    if newX > abs(startX): break

    # We have been through loop once, so looping switches from 1 to 2.
    looping = 2

# If we are here, then while loop has terminated, so exit.
print("You have exited :) Thanks for your maths etc.")

