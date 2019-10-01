from random import *    # So that we can have random numbers.

def main():

    mum = "Eileen"
    dad = "Sydney"
    wife = "Laura"
    place = "Sydney"
    print(id(mum))

    print("Hi, Mom")
    print(id(dad))
    print(id(place))


main()

# Note that the ids of dad and place are identical.
# This is an example of Python's 'interning'.
