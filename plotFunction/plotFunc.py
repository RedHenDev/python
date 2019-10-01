

# So, the aim here is to
# define a mathematical function
# and then, to begin with, output
# return values as each new input
# is given by the user.

# First, let's do it simply.
# Next, we'll go OOP.

# Is this a could initial/default
# value for x?

from math import *

# Our input value.
x = float(1)

# Our integer-cum-bool for while looping indefinitely.
looping = 1

def func(_x):
    return float(float(x) * float(x))

# Loop continues indefinitely.
while looping == 1:
    x = input("\nWhat X to input?   fn(x): ")

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
            print("Sorry: invalid input, buddy.")
            # To stop while loop.
            break

    print("Thanks. When x = " + str(float(x)) + " y = " + \
          str(func(float(x))) + " ")

print("You have exited :) Thanks for your maths etc.")

