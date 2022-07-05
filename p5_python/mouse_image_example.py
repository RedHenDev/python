

from p5 import *

i = load_image("JOJOhead.png")


def setup():
  
  size(400, 400)
  frame_rate(60)
  noCursor()
  
  
  
def draw():

  
  image(i,mouse.x,mouse.y,40,60)


run()