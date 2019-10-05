

# So, the aim here is to
# define a mathematical function
# and then, to begin with, output
# return values as each new input
# is given by the user.

""" plotFunc 4.0 """

""" Here, we aim to try different function equations. """

# Math module used for floor() in version 1.0.
from math import *
import time
from graphics import *

# Our input value.
x = float(1)
# Our current value for x.
newX = float(0)
# Our current increment value.
iX = float(1)

# Our integer-cum-bool for while looping indefinitely.
looping = 1

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

# Note that function definition has to appear before it is called in python.
# Does this have something to do with not having 'hoisting' like javascript?
def func(_x):
    a = -0.11
    b = 0.4
    c = 2.5
    return float(a*(_x*_x) + (b*_x )+ c)

# Loop continues indefinitely.
while looping != 0:

    if looping == 1:
        x = input("\nWhat x to input?   fn(x): ")

        try:
            tX = int(x)
        except:
            try:
                tX = float(x)
            except:
                if x == "":
                    x = float(-50)
                    print("\nx set to default: -50")
                    # If no input value entered, just Enter key,
                    # then assume default value.
                else:
                    print("Sorry: invalid input, buddy.")
                    break

        newX = float(x)
        # OK, we have now taken initial X value.
        xi = input("\nWhat increment (n) to x?  fn(x+n): ")
        # If nothing entered, default to 1 for inc value.
          

    # Check if user wishes to exit.
    if x == "exit" or x == "Exit" or x == "EXIT" or x == "x" or \
       x == "X":
            break
    # Check if user wishes to exit.
    if xi == "exit" or xi == "Exit" or xi == "EXIT" or xi == "x" or \
       xi == "X":
            break

    # Test whether input is acceptable -- i.e. can be
    # converted into either an int or a float.
    if looping == 1:
        iX = xi
        try:
            tX = int(xi)
        except:
            try:
                tX = float(xi)
            except:
                if xi == "":
                    # If no input value entered, just Enter key,
                    # then assume increment value is 1.
                    # I.e, if  looped through more than once.
                    iX = float(0.7)
                    print ("\nDefault value for increment set: 0.7")
                elif xi != "":
                    print("Sorry: invalid input, buddy. Default value set for increment: 0.7")
                    # Assign x the value zero, so as to unaffect progress.
                    iX = float(0.7)

    # Have we looped through at least once?
    if looping == 2:
        # Increment current X value by increment value.
        newX += float(iX)
    else:
        looping = 2
        # Don't increment first time through :)
        newX = float(x)

    # Print output Y to screen; function is called in print's string concatenation.
    #print("Thanks. When x = " + str(float(newX)) + " y = " + \
    #     str(func(float(newX))) + " ")
    prevY = func(float(newX - float(iX)))
    y = func(float(newX))
    print("x: " + str(float(newX)) + " y: " + str(y))
    scalar = 4
    pxy = Point(350+float(newX)*scalar, 350-(func(float(newX))*scalar))
    
    if (prevY < 0 and y > 0) or (prevY > 0 and y < 0): print(newX)
    
    pCir = Circle(pxy, 1.5)
    pCir.setOutline("white")
    pCir.setFill("white")
    pCir.draw(win)
    # Now how to pause a short time?
    time.sleep(0.01)
    if win.checkKey() == "x" or win.checkKey() == "X" or win.checkKey() == "q" or \
       win.checkKey() == "Q":
        win.close()
        break

    if newX > 42: break

# If we are here, then while loop has terminated, so exit.
print("You have exited :) Thanks for your maths etc.")

