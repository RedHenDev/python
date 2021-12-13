from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import random

app = Ursina()

scene.color=color.rgb(0,200,255)

me = FirstPersonController()
me.y = 100
me.x = me.z = 16

mod = load_model('cube')
terrain = Entity(model=Mesh(), texture='grey_noise.png')
model = terrain.model
terrain.color=color.green

texture = load_texture('map_3.png')
for z in range(64):
    for x in range(64):
        px = texture.get_pixel(x,z)

        model.vertices.extend([Vec3(x,floor(px.v*10),z)+
                                v for v in mod.vertices])

        # Decide random tint for colour of block :)
        c = random()-0.5
        model.colors.extend( (Vec4(1-c,1-c,1-c,1),)*
                                len(mod.vertices))
        model.uvs.extend([Vec2(0,0) + u for u in mod.uvs])
model.generate()

me.gravity=0
def update():
    try:
        me.y = lerp(me.y,floor(texture.get_pixel(
        floor(me.x+0.5),floor(me.z+0.5)).v * 10 + 1),6*time.dt)
    except: me.y = me.y
app.run()