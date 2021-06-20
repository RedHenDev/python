"""
Minecraft in Python with Ursina tut 2
PREP version
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
from perlin_noise import PerlinNoise  

app = Ursina()

window.color = color.rgb(0,200,211)
window.exit_button.visible = False

scene.fog_color = color.rgb(0,200,211)
scene.fog_density = 0.04

grassStrokeTex = load_texture('grass_14.png')

def input(key):
    if key == 'q' or key == 'escape':
        quit()

def update():
    global prevZ, prevX
    if  abs(subject.z - prevZ) > 1 or \
        abs(subject.x - prevX) > 1:
            generateShell()
            prevX = subject.x
            prevZ = subject.z

terrain = Entity(model=None,collider=None)
noise = PerlinNoise(octaves=2,seed=2021)
amp = 6
freq = 24

terrainWidth = 10
terrainData = []
for i in range(terrainWidth*terrainWidth):
    x = floor(i/terrainWidth)
    z = floor(i%terrainWidth)
    y = floor((noise([x/freq,z/freq]))*amp)
    terrainData.append(y)
    print(str(y))

shellWidth = 6
shellbies = []
shell = Entity(model=None,collider=None)
for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube',color=color.green)
    bud.parent = shell
    shellbies.append(bud)

def generateShell():
    global shellWidth, terrainWidth
    for i in range(len(shellbies)):
        shellbies[i].x = floor(subject.x + (i/shellWidth) - (shellWidth*0.5))
        shellbies[i].z = floor(subject.z + (i%shellWidth) - (shellWidth*0.5))
        shellbies[i].y = floor(terrainData[int((x*terrainWidth)+z)])
        print(str(shellbies[i].y))
        shellbies[i].visible=False
    shell.model=None
    shell.combine(auto_destroy=False)
    shell.collider='mesh'
    shell.texture=grassStrokeTex

subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0.5
subject.x = subject.z = 5
subject.y = 12
prevX = subject.x
prevZ = subject.z

chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel,scale=1,
                x=22,z=16,y=7.1,
                texture='chicken.png',
                double_sided=True)

generateShell()

app.run()