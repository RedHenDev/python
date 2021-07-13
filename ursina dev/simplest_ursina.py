from ursina import *

app = Ursina()

helloWorld = Entity(model='sphere',scale=6,texture='earth')
helloWorld.collider='sphere'
helloWorld.tooltip = Tooltip('<scale:1><pink>Hello World!')

def update():
    helloWorld.rotation_y += 0.1

    if helloWorld.hovered == True:
        helloWorld.tooltip.enabled = True
    else: helloWorld.tooltip.enabled = False 

app.run()
