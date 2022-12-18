from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import random

app = Ursina()

Sky(color=color.rgb(0,200,255))
window.fullscreen=False

me = FirstPersonController()
me.y = 100
me.x = me.z = 16
me.cursor.visible=False

mod = load_model('cube',use_deepcopy=True)
terrain = Entity(model=Mesh(), texture='grey_noise.png')
model = terrain.model
# terrain.color=color.green

texture = load_texture('map_4.png')
if texture.width > 64: terrainWidth = 64
else: terrainWidth = texture.width
for z in range(terrainWidth):
    for x in range(terrainWidth):
        px = texture.get_pixel(x,z)

        model.vertices.extend([Vec3(x,floor(px.v*10),z)+
                                v for v in mod.vertices])
        model.colors.extend( (Vec4(px.r,px.g,px.b,1),)*
                                len(mod.vertices))
        model.uvs.extend([Vec2(0,0) + u for u in mod.uvs])
model.generate()

class Flake:
    def __init__(this):
        this.ent=Entity(model='quad',texture='flake_1.png')
        this.ent.double_sided=True
        this.ent.scale=random()*0.2
        this.rotSpeed=random()*500

    def update(this):
        this.ent.rotation_y += this.rotSpeed*time.dt
        this.ent.y+=-1*time.dt
        if this.ent.y < 2:
            this.ent.y = me.y + 3 + random() * 5
            this.ent.x = me.x + random() * 20 - 10
            this.ent.z = me.z + random() * 20 - 10

flakes = []

for i in range(512):
    e = Flake()
    e.ent.y = 3 + random()*5
    e.ent.x = random()*20-10
    e.ent.z = random()*20-10
    flakes.append(e)

me.gravity=0
def update():
    for f in flakes:
        f.update()
    try:
        me.y = lerp(me.y,floor(texture.get_pixel(
        floor(me.x+0.5),floor(me.z+0.5)).v * 10 + 1),6*time.dt)
    except: me.y = me.y
app.run()
