from random import randrange
from ursina import *
from perlin_noise import PerlinNoise
from ursina.color import random_color
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.scripts import merge_vertices
from nMap import nMap

app = Ursina()

# window.exit_button.visible=False
window.color = color.rgb(0,200,222)
scene.fog_density=0.002
scene.fog_color=color.rgb(0,200,222)

noise = PerlinNoise(octaves=1, seed=1984)

scale_terrain = 6
width_terrain = 1
prevTime = 0
subSpeed = 0.2

class VertexSheet(Entity):
    def __init__(this, _orig=Vec2(0,0)):
        super().__init__(
            color=color.lime
        )
        this.orig = _orig
        this.quads = []
        scalar = scale_terrain
        this.width = width = width_terrain
        area = width*width
        for q in range(area):
            bub = Entity(model='quad',scale=scalar)
            bub.rotation_x=90
            bub.x = floor(this.orig[0]+((q)/width))*scalar
            bub.z = floor(this.orig[1]+((q)%width))*scalar
            bub.y = 0
            # bub.color=color.random_color()
            # bub.color[0]=0
            # bub.color[2]=0
            # bub.color=color.rgb(0,111,0)
            bub.parent = this
            this.quads.append(bub)
        this.combine(auto_destroy=True)
       
        # this.model.vertices, this.model.triangles = merge_vertices.merge_overlapping_vertices(
        #     this.model.vertices,
        #     this.model.triangles
        # )
        # this.model.generate()

        for i in this.model.vertices:
            freq = 1024
            amp = 1000
            x = i[0]
            z = i[2]
            i[1] = ((noise([x/freq,z/freq]))*amp)
        for i in this.model.vertices:
            freq = 76
            amp = 60
            x = i[0]
            z = i[2]
            i[1] += ((noise([x/freq,z/freq]))*amp)
        for i in this.model.vertices:
            freq = 24
            amp = 20
            x = i[0]
            z = i[2]
            i[1] += ((noise([x/freq,z/freq]))*amp)
        for i in this.model.vertices:
            freq = 1
            amp = 1
            x = i[0]
            z = i[2]
            i[1] += ((noise([x/freq,z/freq]))*amp)
        this.model.generate()

# For new position of subset.
currentVec = 0
iterations = 0
toIterate = 1
changes = -1
subPos = Vec2(0,0)
swirlVecs = [
    Vec2(0,0),
    Vec2(0,1),
    Vec2(1,0),
    Vec2(0,-1),
    Vec2(-1,0)
]

# pos = Vec3(0,0,0)
# terrain = VertexSheet(pos)
# terrain.texture = load_texture('mono64.png')
# terrain.collider='mesh'

# pos = Vec3(width_terrain,0,0)
# t2 = VertexSheet(pos)
# t2.texture = load_texture('mono64.png')
# t2.color = color.rgb(0,0,244)
# t2.collider='mesh'

subsets = []
def genSubset():
    global iterations, toIterate, currentVec
    global changes, subPos
    subPos.x += swirlVecs[currentVec].x*width_terrain
    subPos.y += swirlVecs[currentVec].y*width_terrain
    pos = subPos
    sub = VertexSheet(pos)
    sub.texture = load_texture('mono64.png')
    g = nMap(sub.model.vertices[0][1],0,444,100,255)
    sub.color = color.rgb(0,g,0)
    sub.collider='mesh'
    subsets.append(sub)

    # Co-ordinate new vector by iteration around swirl.
    iterations+=1
    if iterations == toIterate:
        currentVec+=1
        if currentVec == len(swirlVecs):
            currentVec = 1
        changes+=1
        iterations = 0
        if changes == 2:
            changes=0
            toIterate+=1

# roof = duplicate(terrain)
# roof.collider='mesh'
# roof.y += 64
# roof.rotation_x = 180
# roof.z += (terrain.width-1) * scale_terrain

def update():
    global prevTime, subSpeed
    if time.time() - prevTime > subSpeed:
        genSubset()
        prevTime = time.time()

def input(key):
    if key=='q' or key=='escape':
        quit()
    if key=='g':
        genSubset()
        # newRegen()
    if key=='f':
        subject.y += 10

subject = FirstPersonController()
subject.gravity = 0.2
subject.speed = 16
subject.y = 111
subject.z = 5
subject.x = 5

app.run()