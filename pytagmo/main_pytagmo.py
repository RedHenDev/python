from pytagmo import *


def main():
    """ Update loop for this program.
         Plan is to let user call newMessage()
         each time user inputs.
    """

    # Wow -- this actually works.
    # Will loop for each new return press.
    # If anything other than null entered, ends loop.
    i = ""
    while i == "":
        print("\n" + randomSentence())
        i = input("\nPress return for new random sentence:")
        

# Program starts here.
main()

# Program ends here.
print("\n" + "Thank you. Program terminated.")

















# Old ultracrepidarian stuff, you know.

def simpleMain():
    """ Update loop for this program.
         Plan is to let user call newMessage()
         each time user inputs.
    """
    # Wow -- this actually works.
    while input("Press return for new random sentence :O") != None:
        newMessage()
    
def oldMain():
    """ Update loop for this program.
         Just loops round 10 times.
    """
    i = 0
    loops = 10
    while i < loops:
        i+=1
        print(str(i) + " ", end="")
        newMessage()
