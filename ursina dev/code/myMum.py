from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import numpy

app = Ursina()

# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.

jacob = Entity(model='sphere',position=(0,10,0),scale=(2,2,2),color=color.lime)

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.rgba(0, random.uniform(200,222), 0, 255),
            highlight_color = color.lime,
        )


    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                voxel = Voxel(position=self.position + mouse.normal)

            if key == 'right mouse down':
                destroy(self)


for z in range(24):
    for x in range(24):
        y = numpy.sin(x)
        y += numpy.cos(z) * 0.5
        voxel = Voxel(position=(x,y,z))


targetY = 1

def update():
    global targetY
    if jacob.y > targetY:
        jacob.y -= 0.01
        #jacob.scale_y *= 1.001
    if jacob.y < targetY:
        jacob.y += 0.01
    if jacob.y <= 1.1: targetY = 10
    elif jacob.y >= 10: targetY = 1


player = FirstPersonController()
Sky()
app.run()
