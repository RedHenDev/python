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
from ursina import Entity, Vec2, load_model, destroy
from config import minerals
# ***
from math import sin, floor

# *** - handling collectibles via dictionary
# *** [0]blockType, [1]entity_itself
# collectibles=[] - no longer used
cd={}

def drop_collectible(_texture,_blockType,_position):
    e=Entity(   model=load_model('block.obj',use_deepcopy=True),
                texture=_texture,
                position=_position,
                )
    e.scale=0.33
    # *** - and as tuple
    # record collectible presence on collectible dic.
    # NB BEFORE we move to central pos.
    x=floor(e.x)
    y=floor(e.y)
    z=floor(e.z)
    # ***
    cd[(x,y,z)]=(_blockType,e)
    e.y+=0.5-(e.scale_y*0.5)
    e.original_y=e.y
    
    # print(cd.get(e.position))
    e.texture_scale*=64/e.texture.width
    # This is the texture atlas co-ords.
    uu=minerals[_blockType][0]
    uv=minerals[_blockType][1]
    e.model.uvs=([Vec2(uu,uv) + u for u in e.model.uvs])
    e.model.generate()

    # collectibles.append(e)

# ***
# Called from mining_system's highlight -- since 
# this itself called in an update().
# Return's blockType of collectible.
def collectible_pickup(s_pos):
    x=round(s_pos[0])
    y=floor(s_pos[1])
    z=round(s_pos[2])
    b = cd.get((x,y,z))
    if b is not None:
        print(f"Oooo what's this? {b[1]}")
        destroy(b[1])
        cd.pop((x,y,z))
        return b[0]
    else: return None

# Called from mining_system's highlight -- since 
# itself called in an update().
def collectible_bounce():
    for key in cd:
        # NB cd[key][1] is entity itself. [0] is blockType.
        c = cd[key][1]
        c.rotation_y+=2
        # Add a little bounce ;)
        c.y = ( c.original_y + 
                sin(c.rotation_y/50)*
                c.scale_y)