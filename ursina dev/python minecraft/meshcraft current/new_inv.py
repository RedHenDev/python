"""
New attempt at inventory system.
May 22nd 2022.
"""
from operator import index
from ursina import *
import random as ra
import numpy as np 

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
hotbar.scale_x=0.8
# Not quite at very bottom (which would be -0.5).
hotbar.y=-0.45 + (hotbar.scale_y*0.5)
# Appearance.
hotbar.color=color.dark_gray

# For some reason this appears on top of draggable items?
inv_panel = Entity(model='quad',parent=camera.ui)
inv_panel.scale=hotbar.scale
inv_panel.color=color.light_gray
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

        # if this.onHotBar==False:
        #     this.visible=False
        # else: this.visible=True

class Item(Draggable):
    def __init__(this):
        super().__init__()
        this.model='quad'
        this.parent=camera.ui
        this.color=color.random_color()
        # Scale slightly smaller than hotspots.
        this.scale_y=Hotspot.scalar*0.9
        # Make sure is a square.
        this.scale_x = this.scale_y
        # Pick random spot.
        this.x = ra.random()-0.5
        this.y = (ra.random()-0.5)/1.6
        this.render_queue=2

        this.iHotspot=None

        # Fix to designated interval spot.
        this.fix_pos()
    
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
        closest=None
        whichSpot=0
        i=-1
        if type(this.iHotspot) is int:
            test_spots[this.iHotspot].occupied=False
        for h in test_spots:
            i+=0
            if not h.visible: continue
            dist=h.position-this.position
            np.linalg.norm(dist)
            if closest == None or dist < closest:
                if h.occupied: continue
                closest=dist
                whichSpot=h
                this.iHotspot=i
        if whichSpot:
            this.position=whichSpot.position
            whichSpot.occupied=True

for i in range(10):
    test_items.append(Item())

    # These are the hotbar's hotspots!
    bud = Hotspot()
    bud.onHotBar=True
    bud.visible=True
    test_spots.append(bud)
    # -0.5 is left side of hotbar. Scale this to hotbar.
    # Then, adjust right according to hotSPOT scale.
    padding=(hotbar.scale_x-bud.scale_x*10)*0.5
    bud.x=-0.5*hotbar.scale_x+(padding)+(hotbar.scale_x/10)*i
    bud.y=hotbar.y

# More hotspots. On the panel...
for i in range(10):
    bud = Hotspot()
    test_spots.append(bud)
    # -0.5 is left side of hotbar. Scale this to hotbar.
    # Then, adjust right according to hotSPOT scale.
    padding=(hotbar.scale_x-bud.scale_x*10)*0.5
    bud.x=-0.5*hotbar.scale_x+(padding)+(hotbar.scale_x/10)*i
    bud.y=inv_panel.y

test_items[0].color=color.red
test_items[0].x=-0.6
test_items[0].y=0

def inv_input(key,subject,mouse):
    # Pause and unpause, ready for inventory.
    if key=='e' and subject.enabled:
        subject.disable()
        mouse.locked=False
        inv_panel.visible=True
    elif key=='e' and not subject.enabled:
        subject.enable()
        mouse.locked=True
        inv_panel.visible=False