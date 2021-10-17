"""Text file to 3D map"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

grund = Entity(model='quad',rotation_x=90,scale=100)
grund.collider = 'box'
grund.animate_color(color.green,0.1)
eye = FirstPersonController() #EditorCamera()
eye.y = 32

def load():
    import sys, os

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)

    with open('test_map.txt', 'r') as f:
        txt_data = f.read()

    mo = Text(  text='<white><bold>loading:\n'+txt_data,
                background=True)
    mo.background.color = color.black66
    mo.scale *= 1.4
    mo.x = -0.52
    mo.y = 0.4
    mo.appear(speed=0.15)

    z = 0
    count = 0
    for i in txt_data:
        if i=='\n': 
            z+=2
            count=0
        else: 
            # ii=copy(i)
            x = count*2
            e = Entity(model='cube',x=x,y=float(i)/2,z=-z,scale_y=int(i))
            e.texture='brick'
            e.texture_scale.y /= (e.scale_y/2)
            e.collider='box'
            count+=1

def input(key):
    if key=='escape': quit()

load()

app.run()