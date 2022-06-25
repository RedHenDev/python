"""
Hello. This is our system for mined blocks
dropping collectable materials.
"""

# Collectible dictionary. Similar to td{}.
# It will store terrain position of a collectible :)
from ursina import Entity, Vec2, Vec4, load_model, Audio
from config import minerals
from math import sin, floor
from random import random
from inventory_system import Item

# *** - no longer needed. Data included in object.
# pop_audio = Audio('pop.mp3',autoplay=False,loop=False)
# pickup_audio = Audio('pickup.mp3',autoplay=False,loop=False)

class Collectible(Entity):

    # cd = {}

    def __init__(this,_blockType,_pos,_tex,_sub):
        super().__init__()
        this.model=load_model('block.obj',use_deepcopy=True)
        this.texture=_tex
        this.scale=0.33
        this.position=_pos

        this.numVertices=len(this.model.vertices)
        this.blockType=_blockType
        this.subject=_sub
        # *** - pick-up sound
        this.pu_sound=Audio('pop.mp3',autoplay=False,loop=False)
        this.pu_sound.pitch=1+random()
        # Record me on the collectibles dictionary.
        # Key is my position.
        # Collectible.cd[this.position]=this
        # Original position for checking pick up by 
        # subject.
        this.o_position=this.position

        # Central position of mining site.
        this.y+=0.5-(this.scale_y*0.5)
        # Orig pos needed for sine bounce!
        this.original_y=this.y

        # Wrap texture from texture atlas.
        this.texture_scale*=64/this.texture.width

        # Does the dictionary entry for this blockType
        # hold colour information? If so, use it :)
        if len(minerals[this.blockType])>2:
            # Decide random tint for colour of block :)
            c = random()-0.5
            # Grab the Vec4 colour data :)
            ce=minerals[this.blockType][2]
            # Adjust each colour channel separately to
            # ensure that hard-coded RGB combination is maintained.
            this.model.colors = ( (Vec4(ce[0]-c,ce[1]-c,ce[2]-c,ce[3]),)*
                                  this.numVertices)
        else:
            # Decide random tint for colour of block :)
            c = random()-0.5
            # *** - colour bug Xextend
            this.model.colors = ( (Vec4(1-c,1-c,1-c,1),)*
                                   this.numVertices)

        # UV information for texture wrap.
        uu=minerals.get(_blockType)[0]
        uv=minerals.get(_blockType)[1]
        this.model.uvs=([Vec2(uu,uv) + u for u in this.model.uvs])
        # Done!
        # Make sound!
        # ***
        e=Audio('pickup.mp3',autoplay=False,loop=False)
        e.pitch=1+random()
        e.play()
        this.model.generate()

    def update(this):
        this.checkPickUp()
        this.bounce()

    def checkPickUp(this):
        x=round(this.subject.position.x)
        y=floor(this.subject.position.y)
        z=round(this.subject.position.z)
        if ((x,y,z)==this.o_position):
            # pick me up!
            # Remove me from the dictionary.
            # Collectible.cd.pop(this.o_position)
            # Send signal to delete me!
            # this.timeToRest=True
            this.pu_sound.play()
            # *** - drop item to inventory
            Item.gen_item_pickup(this.blockType)
            this.disable()

    def bounce(this):
        this.rotation_y+=2
        # Add a little bounce ;)
        this.y = ( this.original_y + 
                sin(this.rotation_y*0.05)*this.scale_y)