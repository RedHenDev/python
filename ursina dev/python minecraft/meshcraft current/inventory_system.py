
from ursina import *
import random as ra
from config import mins,minerals
import numpy as np

hotspots=[]
items=[]

# Inventory hotbar.
hotbar = Entity(model='quad',parent=camera.ui)
# Set the size and position.
hotbar.scale_y=0.08
# *** - corrects for fullScreen panel overflow.
hotbar.scale_x=hotbar.scale_y*9*1.1 # Ought to be rowFit.
hotbar.y=-0.45 + (hotbar.scale_y*0.5)
# Appearance.
hotbar.color=color.dark_gray
hotbar.render_queue=0

# Inventory main panel.
iPan = Entity(model='quad',parent=camera.ui)
# Set the size and position.
iPan.rows=3
iPan.scale_y=hotbar.scale_y * iPan.rows
iPan.scale_x=hotbar.scale_x
iPan.basePosY=hotbar.y+(hotbar.scale_y*0.5)+(iPan.scale_y*0.5)
iPan.gap=hotbar.scale_y
iPan.y=iPan.basePosY+iPan.gap
# Appearance.
iPan.color=color.light_gray
iPan.render_queue=0
iPan.visible=False

class Hotspot(Entity):
    # Fix size of hospot to height of hotbar.
    scalar=hotbar.scale_y*0.9
    # How many hotspots to fit across hotbar?
    rowFit=9
    def __init__(this):
        super().__init__()
        this.model='quad'
        this.parent=camera.ui
        this.scale_y=Hotspot.scalar
        this.scale_x=this.scale_y
        this.color=color.white
        this.texture='white_box'
        this.render_queue=1

        this.onHotbar=False
        this.visible=False
        this.occupied=False
        # What item are we hosting?
        this.item=None
    
    @staticmethod
    def toggle():
        if iPan.visible:
            iPan.visible=False
        else:
            iPan.visible=True
        # Toggle non-hotbar hotspots and their items.   
        for h in hotspots:
            # Gameplay mode? I.e. not visible?
            if not h.visible and not h.onHotbar:
                # Inventory mode.
                h.visible=True
                if h.item:
                    h.item.visible=True
                    # Enable item?
            elif not h.onHotbar:
                # Gameplay mode.
                h.visible=False
                if h.item:
                    h.item.visible=False
                    # Disable item?


class Item(Draggable):
    def __init__(this):
        super().__init__()
        this.model=load_model('quad',use_deepcopy=True)
        this.scale_x=Hotspot.scalar*0.9
        this.scale_y=this.scale_x
        this.color=color.white
        this.texture='texture_atlas_3.png'
        this.texture_scale*=64/this.texture.width
        this.render_queue=2

        # Pick a random block type.
        this.blockType=mins[ra.randint(0,len(mins)-1)]

        this.onHotbar=False
        this.visible=False
        this.currentSpot=None

        this.set_texture()
        this.set_colour()
    
    def set_texture(this):
        # Use dictionary to access uv co-ords.
        uu=minerals[this.blockType][0]
        uv=minerals[this.blockType][1]
        basemod=load_model('block.obj',use_deepcopy=True)
        e=Empty(model=basemod)
        cb=copy(e.model.uvs)
        del cb[:-33]
        this.model.uvs = [Vec2(uu,uv) + u for u in cb]
        this.model.generate()
        this.rotation_z=180

    def set_colour(this):
        # Do we have a color element on the tuple?
        if len(minerals[this.blockType]) > 2:
            # Yes! Set color :)
            this.color=minerals[this.blockType][2]
    
    def fixPos(this):
        # Look through all the hotspots.
        # Find the unoccupied hotspot that is closest.
        # If found, copy that hotspot's position.
        # Set previous hotspot host to unoccupied.
        # Download item's blocktype info etc. into
        # host hotspot -- so that subject can use item.
        # !?! Can't find an available hotspot?
        # Return to current host position.

        closest=-1
        closestHotty=None
        for h in hotspots:
            if h.occupied: continue
            # Found a unoccupied hotspot :)
            # How close is it?
            dist=h.position-this.position
            # Find the magnitude - i.e. distance.
            dist=np.linalg.norm(dist)
            if dist < closest or closest == -1:
                # We have a new closest!
                closestHotty=h
                # Always remember to set current record!
                closest=dist
        # Finished iterating over hotspots.
        if closestHotty is not None:
            # We've found an available closest :)
            this.position=closestHotty.position
            # Update new host's information about item.
            closestHotty.occupied=True
            closestHotty.item=this
            # Update previous host-spot's status.
            if this.currentSpot:
                this.currentSpot.occupied=False
                this.currentSpot.item=None
            # Finally, update current host spot.
            this.currentSpot=closestHotty
        elif this.currentSpot:
            # No hotspot available? Just move back.
            this.position=this.currentSpot.position

    def drop(this):
        this.fixPos()

# Hotspots for the hotbar.
for i in range(Hotspot.rowFit):
    bud=Hotspot()
    bud.onHotbar=True
    bud.visible=True
    bud.y=hotbar.y
    padding=(hotbar.scale_x-Hotspot.scalar*Hotspot.rowFit)*0.5
    bud.x=  (   hotbar.x-hotbar.scale_x*0.5 +
                Hotspot.scalar*0.5 + 
                padding +
                i*Hotspot.scalar
            )
    hotspots.append(bud)

# Hotspots for the main inventory panel.
for i in range(Hotspot.rowFit):
    for j in range(iPan.rows):
        bud=Hotspot()
        bud.onHotbar=False
        bud.visible=False
        # Position.
        padding_x=(iPan.scale_x-Hotspot.scalar*Hotspot.rowFit)*0.5
        padding_y=(iPan.scale_y-Hotspot.scalar*iPan.rows)*0.5
        bud.y=  (   iPan.y+iPan.scale_y*0.5 -
                    Hotspot.scalar*0.5 -
                    padding_y -
                    Hotspot.scalar * j
                )
        bud.x=  (   iPan.x-iPan.scale_x*0.5 +
                    Hotspot.scalar*0.5 +
                    padding_x +
                    i*Hotspot.scalar
                )
        hotspots.append(bud)
# Main inventory panel items. 
for i in range(8):
    bud=Item()
    bud.onHotbar=True
    bud.visible=True
    bud.x=ra.random()-0.5
    bud.y=ra.random()-0.5
    bud.fixPos()
    items.append(bud)

# ***
# To hide items that are not on hotbar
# at start. NB needs to happen twice.
Hotspot.toggle()
Hotspot.toggle()

# ***
# Text experiments.
descr = dedent('''
    Rainstorm
    <pink>
    Summon a rain storm to deal 5 water 
    damage to everyone, including yourself.
    1234 1234 1234 1234 1234 1234 2134 1234 1234 
    1234 1234 1234 2134 2134 1234 1234 1234 1234
    Lasts for 4 rounds.''').strip()

Text.default_resolution = 1080 * Text.size
test = Text(text=descr, wordwrap=30)

def inv_input(key,subject,mouse):
    try:
        wnum = int(key)
        if wnum > 0 and wnum < 10:
            # Make sure no hotspots are highlighted.
            for h in hotspots:
                h.color=color.white
            # Adjust wnum to list indexing (1=0).
            wnum-=1
            hotspots[wnum].color=color.black
            # Is this hotspot occupied with an item?
            if hotspots[wnum].occupied:
                # Set subject's new blocktype from this item.
                subject.blockType=hotspots[wnum].item.blockType
            # ***
            else:
                subject.blockType=None
    except:
        pass
    # Pause and unpause, ready for inventory.
    if key=='e' and subject.enabled:
        # Inventory mode.
        Hotspot.toggle()
        subject.disable()
        mouse.locked=False
    elif key=='e' and not subject.enabled:
        # Gameplay mode.
        Hotspot.toggle()
        subject.enable()
        mouse.locked=True