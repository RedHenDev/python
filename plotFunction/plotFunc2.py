

# So, the aim here is to
# define a mathematical function
# and then, to begin with, output
# return values as each new input
# is given by the user.

""" plotFunc 2.0 """

""" Here, we aim to iterate automatically. """

# Math module used for floor() in version 1.0.
from math import *

# Our input value.
x = float(1)
# Our current value for x.
newX = float(0)

# Our integer-cum-bool for while looping indefinitely.
looping = 1

# Note that function definition has to appear before it is called in python.
# Does this have something to do with not having 'hoisting' like javascript?
def func(_x):
    return float(float(_x) * float(_x))

# Loop continues indefinitely.
while looping != 0:

    if looping == 1:
        x = input("\nWhat X to input?   fn(x): ")
        # OK, we have now taken initial X value,
        # so on next iteration, take increment value instead.
        newX = float(x)
    else:
        x = input("\nWhat increment (n) to X?  fn(x+n): ")

    # Check if user wishes to exit.
    if x == "exit" or x == "Exit" or x == "EXIT" or x == "x" or \
       x == "X":
            break
    try:
        tX = int(x)
    except:
        try:
            tX = float(x)
        except:
            if x == "" and looping == 2:
                # If no input value entered, just Enter key,
                # then assume increment value is 1.
                # I.e, if  looped through more than once.
                x = float(1)
            else:
                print("Sorry: invalid input, buddy.")
                # Assign x the value zero, so as to unaffect progress.
                x = float(0)
                # Old method below: break.
                # Now stop while loop with break.
                # break
                

    # Have we looped through at least once?
    if looping == 2:
        # Increment current X value by increment value.
        newX += float(x)
    else:
        looping = 2

    # Print output Y to screen; function is called in print's string concatenation.
    print("Thanks. When x = " + str(float(newX)) + " y = " + \
          str(func(float(newX))) + " ")

# If we are here, then while loop has terminated, so exit.
print("You have exited :) Thanks for your maths etc.")

