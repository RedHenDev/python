from random import randrange
from ursina import *
from perlin_noise import PerlinNoise
from ursina.color import random_color
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.scripts import merge_vertices

app = Ursina()

# window.exit_button.visible=False
window.color = color.rgb(0,200,222)
scene.fog_density=0.07
scene.fog_color=color.rgb(0,200,222)

noise = PerlinNoise(octaves=6, seed=1984)

class VertexSheet(Entity):
    def __init__(this, _orig):
        super().__init__(
            color=color.lime
        )
        this.orig = _orig
        this.quads = []
        scalar = 1
        for q in range(64):
            bub = Entity(model='quad',scale=scalar)
            bub.rotation_x=90
            bub.x = floor(this.orig[0]+(q/8)*scalar)
            bub.z = floor(this.orig[2]+(q%8)*scalar)
            bub.y = 0
            # bub.color=color.random_color()
            # bub.color[0]=0
            # bub.color[2]=0
            bub.color=color.rgb(0,111,0)
            bub.parent = this
            this.quads.append(bub)
        this.combine(auto_destroy=True)
        
        this.model.vertices, this.model.triangles = merge_vertices.merge_overlapping_vertices(
            this.model.vertices,
            this.model.triangles
        )
        for i in this.model.vertices:
            freq = 22
            amp = 12
            x = i[0]
            z = i[2]
            i[1] = floor((noise([x/freq,z/freq]))*amp)
        this.model.generate()
        this.collider = 'mesh'
terrain = Entity()
vs = []
for v in range(16):
    o = Vec3(floor(v/4)*8,0,floor(v%4)*8)
    v = VertexSheet(o)
    v.parent = terrain
    vs.append(v)
terrain.combine(auto_destroy=True)
terrain.texture='mono64.png'
locZ = 0
def newRegen():
    global locZ
    freq = 22
    amp = 12
    locZ -= 1
    for i in terrain.model.vertices:
        x = i[0]
        z = i[2]
        z -= locZ
        i[1] = floor((noise([x/freq,z/freq]))*amp)
    terrain.model.generate()

def input(key):
    if key=='q' or key=='escape':
        quit()
    if key=='g':
        newRegen()

subject = FirstPersonController()
subject.gravity = 0.0
subject.y = 3

app.run()