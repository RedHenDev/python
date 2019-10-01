from random import *

nom = input('Hello. What is your name? \n')

print('Thanks, ' + nom + '.')

rnd = str(int(random()*10)+1)

print('\n...and here is a random number: ' + rnd)

iters = 0

howMany = int(rnd)

# We'll iterate the number of times given by the random number.
while iters < howMany:

    rnd = str(int(random()*10)+1)
    
    print('\n...and here is another... ' + rnd)

    iters+=1

#********************************************
#********************************************

from graphics import *

def main():
    win = GraphWin("Hello Graphics", 200, 200)
    c = Circle(Point(100,100), 42)
    c.draw(win)

    i = 0
    while i < 101:
        i+=1
        if i < 51: c.move(1,0)
        else:
            c.move(-1,0)
            c.setFill(color_rgb(0,i*2,i+42))
        #c.undraw()
        #c.draw(win)

    mess = Text(Point(100,42), '-Tap this window to exit :)')
    mess.draw(win)

    print("\n-Select window and press any key to exit :)")
    
    win.getMouse()    # Pause to view result.
    win.close()     # Close window when done.

    
main()

    
