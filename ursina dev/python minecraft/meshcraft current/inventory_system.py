
from ursina import *
import random as ra
from config import mins,minerals
import numpy as np

hotspots=[]
items=[]

# Inventory hotbar.
hotbar = Entity(model=None)
hotbar.parent=camera.ui
hotbar.model=load_model('quad')
# Set the size and position.
print(hotbar.position)
# ***
import sys
window.fullscreen=True
if window.fullscreen==False and sys.platform.lower()=='darwin':
    pass
    # camera.ui.scale_x*=0.05*1/window.aspect_ratio
    # camera.ui.scale_y*=0.05
# ui_scalar + use of 1/aspect_ratio.
hot_cols=9
hot_wid=1/16 # Width of hotspot is 1/16 of window height.
hb_wid=hot_wid*hot_cols # Hotbar width no. of cols times this.
hotbar.scale=Vec3(hb_wid,hot_wid,0)
hotbar.y=(-0.45 + (hotbar.scale_y*0.5))

# Appearance.
hotbar.color=color.dark_gray

# Inventory main panel.
iPan = Entity()
iPan.parent=camera.ui
iPan.model=load_model('quad')
# Set the size and position.
iPan.rows=3
iPan.scale_y=hotbar.scale_y * iPan.rows
iPan.scale_x=hotbar.scale_x

# Appearance.
iPan.color=color.light_gray
# iPan.render_queue=0
iPan.visible=False

class Hotspot(Entity):
    # Fix width of hospot to height of hotbar.
    scalar=hotbar.scale_y*0.9
    # How many hotspots to fit across hotbar?
    rowFit=9
    def __init__(this):
        # ***
        super().__init__(
        parent=camera.ui,
        model=None,
        scale_y=Hotspot.scalar,
        scale_x=Hotspot.scalar,
        color=color.white,
        z=-1
        )
        this.model=load_model('quad')
        this.texture='white_box'
        this.onHotbar=False
        this.visible=False
        this.occupied=False
        # What item are we hosting?
        this.item=None
        # New stack system :)
        # Start with no items as default.
        this.stack=0
        # Text for number of blocks in stack.
        this.t = Text("",scale=1.5)

    @staticmethod
    def matchPos(_blockType,_onHotbar=False):
        """
        Find matching stack among populated hotspots.
        """
        # First, iterate over non-hotbar hotspots.
        # Next, I have to add in check whether
        # we found a matching stack, else,
        # find empty spot.
        for h in hotspots:
            if not h.occupied: continue
            if h.onHotbar != _onHotbar: continue
            if h.item.blockType==_blockType:
                h.stack+=1
                return True
        return False

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
                h.t.visible=True
                if h.item:
                    h.item.visible=True
                    # Enable item?
            elif not h.onHotbar:
                # Gameplay mode.
                h.visible=False
                h.t.visible=False
                if h.item:
                    h.item.visible=False
                    # Disable item?


class Item(Draggable):

    def __init__(this,_blockType):
        super().__init__(
        parent=camera.ui,
        z=-2
        )
        this.model=load_model('quad')
        # *** 0.8 to fit in white lines.
        this.scale_x=Hotspot.scalar*0.8
        this.scale_y=this.scale_x
        this.color=color.white
        this.texture='texture_atlas_3.png'
        this.texture_scale*=64/this.texture.width

        if _blockType is not None:
            this.blockType=_blockType
        else:
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
        basemod=load_model('block.obj')
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
            if h.occupied and h.item!=this: continue
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
            closestHotty.stack=this.currentSpot.stack
            # Update previous host-spot's status.
            # Finally, update current host spot.
            if this.currentSpot!=closestHotty:
                this.currentSpot.stack=0
                # *** No need for spaces in string.
                this.currentSpot.t.text = ""
                this.currentSpot.occupied=False
                this.currentSpot.item=None
                this.currentSpot=closestHotty
        elif this.currentSpot:
            # No hotspot available? Just move back.
            this.position=this.currentSpot.position
    
    def update_stack_text(this):
        # Display how many blocks in this hotspot's stack.
        stackNum = this.currentSpot.stack
        myText="<white><bold>"+str(stackNum)
        this.currentSpot.t.text = myText
        this.currentSpot.t.origin=(0,0)
        this.currentSpot.t.z=-3
        this.currentSpot.t.x=this.currentSpot.x
        this.currentSpot.t.y=this.currentSpot.y

    def drop(this):
        # ***
        if toggledOFF:
            return
        this.fixPos()
        # Display how many blocks in this hotspot's stack.
        this.update_stack_text()
        

    @staticmethod
    def stack_check(_blockType):
        for h in hotspots:
            if h.onHotbar==False: continue
            if h.occupied==False: continue
            # OK -- found an occupied hotbar hotspot.
            if h.item.blockType==_blockType:
                h.stack+=1
                h.item.update_stack_text()
                return True
        # No matching stacks.
        return False

    @staticmethod
    def new_item(_blockType):
        # First, check whether there is already
        # a stack of this blockType on the hotbar.
        # If yes, increment hotspot's stack.
        # If no, and space available on hotbar,
        # create a new stack of 1 of that item -
        # which means, creating a new Item.
        aStack = Item.stack_check(_blockType)
        if aStack==False:
            # Space available on hotbar?
            for h in hotspots:
                if not h.onHotbar or h.occupied: continue
                else:
                    h.stack=1
                    b=Item(_blockType)
                    b.currentSpot=h
                    items.append(b)
                    # Refactor this later!
                    # Dedicated function please :)
                    h.item=b
                    h.occupied=True
                    b.onHotbar=True
                    b.visible=True
                    b.x = h.x
                    b.y = h.y
                    b.update_stack_text()
                    break
        
# Hotspots for the hotbar.
for i in range(Hotspot.rowFit):
    bud=Hotspot()
    bud.onHotbar=True
    bud.visible=True
    bud.y=hotbar.y
    padding=(hotbar.scale_x-Hotspot.scalar*Hotspot.rowFit)*0.5
    # *** *1.1 and 1.2 in order to space out...
    bud.x=  (   hotbar.x-hotbar.scale_x*0.5*1.1 +
                Hotspot.scalar*0.5 *1.2+ 
                padding +
                i*Hotspot.scalar*1.1
            )
    hotspots.append(bud)

# Hotspots for the main inventory panel.
for i in range(Hotspot.rowFit):
    for j in range(iPan.rows):
        bud=Hotspot()
        bud.onHotbar=False
        bud.visible=False
        # Position.
        # *** 
        padding_x=(iPan.scale_x-Hotspot.scalar*Hotspot.rowFit)*0.5
        padding_y=(iPan.scale_y-Hotspot.scalar*iPan.rows)*0.5
        bud.y=  (   iPan.y+iPan.scale_y*0.5 -
                    Hotspot.scalar*0.5 -
                    padding_y -
                    Hotspot.scalar * j
                )
        # *** 
        bud.x=  (   iPan.x-iPan.scale_x*0.5*1.1 +
                    Hotspot.scalar*0.5*1.2 +
                    padding_x +
                    i*Hotspot.scalar*1.1
                )
        hotspots.append(bud)

# Main inventory panel items. 
# for i in range(8):
#     bud=Item(None)
#     bud.onHotbar=False
#     bud.visible=False
#     bud.x=ra.random()-0.5
#     bud.y=ra.random()-0.5
#     bud.fixPos()
#     items.append(bud)

# ***
# To hide items that are not on hotbar
# at start. NB needs to happen twice.
Hotspot.toggle()
Hotspot.toggle()

# Where am I?
wai=Text(   '<black><bold>Nowhere',
            scale=2.4,position=(-.8,.5))

# ***
toggledOFF=True
def inv_input(key,subject,mouse):
    global toggledOFF
    # Since we may have moved, update location text.
    wai.text=f'<black><bold>east:{floor(subject.x)}, north:{floor(subject.z)}'
    
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
        toggledOFF=False
    elif key=='e' and not subject.enabled:
        # Gameplay mode.
        Hotspot.toggle()
        subject.enable()
        mouse.locked=True
        toggledOFF=True