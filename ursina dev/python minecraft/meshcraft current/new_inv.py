"""
New attempt at inventory system.
May 22nd 2022.
"""
from ursina import *
import random as ra
import numpy as np 
from config import *

# Inventory hotbar.
hotbar = Entity(model='quad',parent=camera.ui)
# Set the scale and position.
# So, inventory panel(s) and hotbar must be scaled
# correspondingly--and items--so that they each cater for a 
# grid of hotspots in the same way.
# Also, if hotbar is to fit 10 hotspots across, then
# either the scale of an individual hotspot or the
# scale of the hotbar's width is to fix the scale of
# the other. E.g. if hotbar.scale_x = 0.8 then
#  each hotpot.scale_x must be 0.8/10.
hotbar.scale_y=0.08
hotbar.scale_x=0.68
# Not quite at very bottom (which would be -0.5).
hotbar.y=-0.45 + (hotbar.scale_y*0.5)
# Appearance.
hotbar.color=color.dark_gray

# For some reason this appears on top of draggable items?
# Sorted this with render queue.
inv_panel = Entity(model='quad',parent=camera.ui)
inv_panel.scale=hotbar.scale
inv_panel.scale_y*=4
inv_panel.color=color.dark_gray
inv_panel.y=-0.1
inv_panel.render_queue=0
inv_panel.visible=False

test_spots=[]
test_items=[]

class Hotspot(Entity):
    # Fix scale to divide hotbar across by 10.
    # Must be slightly smaller than hotbar height tho!
    scalar=(hotbar.scale_x/10)*0.9
    def __init__(this):
        super().__init__()
        this.model='quad'
        this.parent=camera.ui
        this.color=color.white
        this.render_queue=1

        this.onHotBar=False
        this.visible=False
        this.occupied=False
        # ***
        this.blockType=None
        
        this.scale_y=Hotspot.scalar
        # Make sure is a square.
        this.scale_x = this.scale_y
        this.texture='white_box'
    
    # NB. this will be called automatically with
    # key presses. More efficient than update() :)
    def input(this,key):
        if key=='e' and not this.visible:
            this.visible=True
            return
        elif key=='e' and this.visible and not this.onHotBar:
            this.visible=False

class Item(Draggable):
    def __init__(this,_blockType='grass'):
        super().__init__()
        this.model='quad'
        this.parent=camera.ui
        # this.color=color.random_color()
        # Scale slightly smaller than hotspots.
        this.scale_y=Hotspot.scalar*0.9
        # Make sure is a square.
        this.scale_x = this.scale_y
        # Pick random spot.
        this.x = ra.random()-0.5
        this.y = (ra.random()-0.5)/1.6
        this.render_queue=2

        # Record of which hotSpot this is anchored to.
        # Harmless to set to 0. See fixpos().Lol --
        # well that did't work out.
        # So, set to -1 as default, then checked b4 use.
        this.iHotspot=-1
        this.onHotBar=False
        this.visible=False

        this.blockType=_blockType
        this.texture='texture_atlas_3.png'
        this.texture_scale*=64/this.texture.width
        # (32/(this.texture.width))  
        # Assume default colour. I'll make this explicit.
        this.color=color.white
        this.setup_texture()
        this.setup_color()

        # Fix to designated interval spot.
        # this.fix_pos()

    @staticmethod
    def set_visibility(_on=False):
        for i in test_items:
            if _on or i.onHotBar:
                i.visible=True
            else:
                i.visible=False

    def setup_texture(this):
        # Use dictionary to access uv co-ords.
        uu=minerals[this.blockType][0]
        uv=minerals[this.blockType][1]
        basemod=load_model('block.obj')
        cb=copy(basemod.uvs)
        del cb[:-33]
        this.model.uvs = [Vec2(uu,uv) + u for u in cb]
        this.model.generate()
        this.rotation_z=180
    
    def setup_color(this):
        # Do we have a color element on the tuple?
        if len(minerals[this.blockType]) > 2:
            # Yes! Set color :)
            this.color=minerals[this.blockType][2]

    def drop(this):
        this.fix_pos()

    def fix_pos(this):
        # Develop (but keep this nice trick)
        # to very different system where items
        # determine the position of the droppped item.
        # I.e. this is just the position of the hotspot.
        """
        scalar=16 # Because 16 is 2 * 10 * 0.8 (scale).
        this.x=round(this.x*scalar)/scalar
        this.y=round(this.y*scalar)/scalar
        """

        # Look through hotspots. Keep closest.
        # Move to that pos.
        closest=9999
        whichSpot=None
        count=-1
        whatCount=-1
        for h in test_spots:
            count+=1
            if not h.visible: continue
            dist=h.position-this.position
            dist=np.linalg.norm(dist)
            if dist < closest:
                if h.occupied: continue
                closest=dist
                whichSpot=h
                whatCount=count
        # If we found an available closest spot...
        if whichSpot:
            this.position=whichSpot.position
            if this.iHotspot != -1:
                test_spots[this.iHotspot].occupied=False
                # ***
                test_spots[this.iHotspot].blockType=this.blockType
            whichSpot.occupied=True
            this.iHotspot=whatCount
            if whichSpot.onHotBar:
                this.onHotBar=True
                this.visible=True
            else: 
                this.onHotBar=False

# Instantiate hotspots for hotbar and panel.
for i in range(10):
    # These are the hotbar's hotspots!
    bud = Hotspot()
    bud.onHotBar=True
    bud.visible=True
    # -0.5 is left side of hotbar. Scale this to hotbar.
    # Then, adjust right according to hotSPOT scale.
    padding=(hotbar.scale_x-bud.scale_x*10)*0.5
    bud.x=-0.5*hotbar.scale_x+(padding)+(hotbar.scale_x/10)*i
    bud.y=hotbar.y
    test_spots.append(bud)
for i in range(10):
    for j in range(4):
        bud = Hotspot()
        # -0.5 is left side of hotbar. Scale this to hotbar.
        # Then, adjust right according to hotSPOT scale.
        padding=(hotbar.scale_x-bud.scale_y*10)*0.5
        bud.x=-0.5*hotbar.scale_x+(padding)+(hotbar.scale_x/10)*i
        # Position on 'top row' of panel.
        padding=(inv_panel.scale_y-bud.scale_y*4)*0.1
        bud.y=inv_panel.y+0.5*inv_panel.scale_y-bud.scale_y*0.5-padding-(inv_panel.scale_y/4)*(j)
        test_spots.append(bud)

# Instantiate our items.
for i in range(40):
    # whatBlockType=ra.randint(0,len(mins)-1)
    whatBlockType=int(i%(len(mins)))
    bud=Item(mins[whatBlockType])
    bud.position=test_spots[10+i].position
    bud.iHotspot=10+i
    test_spots[10+i].occupied=True
    bud.onHotBar=False
    bud.visible=test_spots[10+i].visible
    test_items.append(bud)


def inv_input(key,subject,mouse):
    # Pause and unpause, ready for inventory.
    try:
        wnum=int(key)
        print_on_screen(wnum)
        if wnum < 10 and wnum > 0:
            if test_spots[wnum-1].occupied:
                subject.blockType=test_spots[wnum-1].blockType
                print(test_spots[wnum-1].blockType)
                test_spots[wnum-1].color=color.yellow
    except:
        pass

    if key=='e' and subject.enabled:
        subject.disable()
        mouse.locked=False
        inv_panel.visible=True
        Item.set_visibility(True)
    elif key=='e' and not subject.enabled:
        subject.enable()
        mouse.locked=True
        inv_panel.visible=False
        Item.set_visibility()