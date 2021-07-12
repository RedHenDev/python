from random import randrange
from ursina import *
from perlin_noise import PerlinNoise
from ursina.color import random_color
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.scripts import merge_vertices

app = Ursina()

# window.exit_button.visible=False
window.color = color.rgb(0,200,222)
scene.fog_density=0.001
scene.fog_color=color.rgb(0,200,222)

noise = PerlinNoise(octaves=1, seed=1984)

scale_terrain = 36

class VertexSheet(Entity):
    def __init__(this, _orig=Vec3(0,0,0)):
        super().__init__(
            color=color.lime
        )
        this.orig = _orig
        this.quads = []
        scalar = scale_terrain
        width = 10
        area = width*width
        for q in range(area):
            bub = Entity(model='quad',scale=scalar)
            bub.rotation_x=90
            bub.x = floor(this.orig[0]+((q)/width))*scalar
            bub.z = floor(this.orig[2]+((q)%width))*scalar
            bub.y = 0
            bub.color=color.random_color()
            # bub.color[0]=0
            # bub.color[2]=0
            # bub.color=color.rgb(0,111,0)
            bub.parent = this
            this.quads.append(bub)
        this.combine(auto_destroy=True)

        """
        this.model.vertices, this.model.triangles = merge_vertices.merge_overlapping_vertices(
            this.model.vertices,
            this.model.triangles
        )
        """
        for i in this.model.vertices:
            freq = 200
            amp = 100
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
            freq = 2
            amp = 1
            x = i[0]
            z = i[2]
            i[1] += ((noise([x/freq,z/freq]))*amp)
        this.model.generate()

pos = Vec3(0,0,0)
terrain = VertexSheet(pos)
terrain.texture = load_texture('mono64.png')
terrain.collider='mesh'


roof = duplicate(terrain)
roof.collider='mesh'
roof.y += 50
roof.rotation_x = 180
#roof.z += 32


locZ = 0
def newRegen():
    global locZ
    locZ -= 10
       
    for i in terrain.model.vertices:
        freq = 200
        amp = 100
        x = i[0]
        z = i[2] - locZ
        i[1] = ((noise([x/freq,z/freq]))*amp)
    for i in terrain.model.vertices:
        freq = 76
        amp = 60
        x = i[0]
        z = i[2] - locZ
        i[1] += ((noise([x/freq,z/freq]))*amp)
    for i in terrain.model.vertices:
        freq = 24
        amp = 20
        x = i[0]
        z = i[2] - locZ
        i[1] += ((noise([x/freq,z/freq]))*amp)
    for i in terrain.model.vertices:
        freq = 2
        amp = 1
        x = i[0]
        z = i[2] - locZ
        i[1] += ((noise([x/freq,z/freq]))*amp)
    terrain.model.generate()

def input(key):
    if key=='q' or key=='escape':
        quit()
    if key=='g':
        newRegen()
    if key=='space':
        subject.y += 1

subject = FirstPersonController()
subject.gravity = 0.0
subject.speed = 32
subject.y = 20
subject.z = 32
subject.x = 32

app.run()
