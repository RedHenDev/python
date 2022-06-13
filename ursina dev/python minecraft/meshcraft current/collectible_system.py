"""
June 11 2022
Collectible pick-ups system (CPS).

We'll pass the subject, or rather, the inventory
through to this system?

Well, it makes sense to have the inventory system
speak to this system.

We'll want to add an inventory item to hotbar
when picked up by subject. That means
instantiating a new item and placing it near hotbar.
In Minecraft, stacking behaviour would kick in here:
if an item of same type that is not fully stacked,
i.e., is less than 64 items high, then add to this stack.
"""
from ursina import Entity, Vec2, load_model
from config import minerals

pickups=[]
pickup_spin=0

def new_pickable(_model,_texture,_blockType,_position):
    global pickup_spin
    e=Entity(   model=load_model('block.obj',use_deepcopy=True),
                texture=_texture,
                position=_position,
                )
    e.scale=0.33
    e.y+=0.5
    e.original_y=e.y
    e.texture_scale*=64/e.texture.width
    # This is the texture atlas co-ords.
    uu=minerals[_blockType][0]
    uv=minerals[_blockType][1]
    e.model.uvs=([Vec2(uu,uv) + u for u in e.model.uvs])
    e.model.generate()

    pickups.append(e)


