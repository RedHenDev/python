
from ursina import *
import random as ra
from config import mins,minerals
import numpy as np

hotspots=[]
items=[]

# Inventory hotbar.
hotbar = Entity(model=None)
hotbar.parent=camera.ui
hotbar.model=load_model('quad',use_deepcopy=True)
# Set the size and position.
print(hotbar.position)
# ***
window.fullscreen=False
if window.fullscreen==False:
    camera.ui.scale_x*=0.05*1/window.aspect_ratio
    camera.ui.scale_y*=0.05
# ui_scalar + use of 1/aspect_ratio.
hot_cols=9
hot_wid=1/16 # Width of hotspot is 1 tenth of window height.
hb_wid=hot_wid*hot_cols # Hotbar width no. of cols times this.
hotbar.scale=Vec3(hb_wid,hot_wid,0)
# ui_cols=hotbar.scale[0]/9
hotbar.y=(-0.45 + (hotbar.scale_y*0.5))
# *** - corrects for fullScreen panel overflow.
# hotbar.scale_x=hotbar.scale_y*9*1.1 # Ought to be rowFit.
# hotbar.y=-0.45 + (hotbar.scale_y*0.5)
# Appearance.
hotbar.color=color.dark_gray
hotbar.render_queue=0

# Inventory main panel.
iPan = Entity()
iPan.parent=camera.ui
iPan.model=load_model('quad',use_deepcopy=True)
# Set the size and position.
iPan.rows=3
iPan.scale_y=hotbar.scale_y * iPan.rows
iPan.scale_x=hotbar.scale_x
# iPan.basePosY=hotbar.y+(hotbar.scale_y*0.5)+(iPan.scale_y*0.5)
# iPan.gap=hotbar.scale_y
# iPan.y=iPan.basePosY+iPan.gap
# Appearance.
iPan.color=color.light_gray
iPan.render_queue=0
iPan.visible=False

class Hotspot(Entity):
    # Fix width of hospot to height of hotbar.
    scalar=hotbar.scale_y*0.9
    # How many hotspots to fit across hotbar?
    rowFit=9
    def __init__(this):
        super().__init__(
        parent=camera.ui,
        model=None,
        scale_y=Hotspot.scalar,
        scale_x=Hotspot.scalar,
        color=color.white,
        )
        this.model=load_model('quad',use_deepcopy=True)
        this.texture='white_box'
        this.render_queue=3
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

    def __init__(this,_blockType):
        super().__init__(
        parent=camera.ui
        )
        this.model=load_model('quad',use_deepcopy=True)
        # *** 0.8 to fit in white lines.
        this.scale_x=Hotspot.scalar*0.8
        this.scale_y=this.scale_x
        this.color=color.white
        this.texture='texture_atlas_3.png'
        this.texture_scale*=64/this.texture.width
        this.render_queue=2

        # ***
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
        
        # Item.text_pickup(this.blockType)
        # ***
        # if this.stack_text is not None:
        #     destroy(this.stack_text)
        # this.stack_text = Text()
        # # this.stack_text.parent=this
        # this.stack_text.text="<white><scale:0.1>"+str(this.blockType)
    
    # ***
    stack_text=None
    @staticmethod
    def text_pickup(_blockType):
        try:
            destroy(Item.stack_text)
        except:
            pass
        Item.stack_text = Text()
        # this.stack_text.parent=this
        Item.stack_text.text="<white><scale:1>"+str(_blockType)
        destroy(Item.stack_text,5)

    # ***
    @staticmethod
    def gen_item_pickup(_blockType):
        """Generates an item"""
        e=Item(_blockType)
        e.onHotbar=True
        e.visible=False
        e.fixPos()
        items.append(e)
        # *** text on screen
        # Item.text_pickup(_blockType)
        print("new item added: " + str(items[-1].blockType))

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
                # ***
                try:
                    destroy(this.currentSpot.t)
                except:
                    pass
                try: destroy(this.currentSpot.tt)
                except: pass
            # Finally, update current host spot.
            this.currentSpot=closestHotty
            # ***
            try: destroy(this.currentSpot.tt)
            except: pass
        elif this.currentSpot:
            # No hotspot available? Just move back.
            this.position=this.currentSpot.position

    def drop(this):
        if toggledOFF:
            return
        print('drop fired!')
        this.fixPos()
        # ***
        # Can we display stack value here?
        # First, we'll just try to display blockType.
        this.currentSpot.t=Text(parent=camera.ui_camera,
                                scale=2)
        this.currentSpot.t.origin=(0,0)
        this.currentSpot.t.bg=Entity(   model='quad',
                                        color=color.white,
                                        scale=0.1)
        this.currentSpot.t.bg.parent=camera.ui
        this.currentSpot.t.bg.render_queue=3
        this.currentSpot.t.render_queue=3
        this.currentSpot.t.text=("<black><bold>"+
                                str(this.blockType))
        this.currentSpot.t.position=this.currentSpot.position
        destroy(this.currentSpot.t,5)
        destroy(this.currentSpot.t.bg,5)
        # * tooltip version
        # try: destroy(this.currentSpot.tt)
        # except: pass
        # this.currentSpot.tt=Tooltip("<black><bold>"
        # +str(this.blockType)+': '+str(3),scale=1)
        # this.currentSpot.tt.background.color=color.white
        # this.currentSpot.tt.enabled=True
        # destroy(this.currentSpot.tt,5)
        

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
    # ***
    bud.render_queue=1

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
        bud.x=  (   iPan.x-iPan.scale_x*0.5 +
                    Hotspot.scalar*0.5 +
                    padding_x +
                    i*Hotspot.scalar
                )
        hotspots.append(bud)
        # ***
        bud.render_queue=1
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

# ***
# Text experiments.
# descr = dedent('''
#     Rainstorm
#     <\n>
#     <black>
#     <scale:2>
# Boop 64''').strip()

# Text.default_resolution = 1080 * Text.size
# test = Text(text=descr, wordwrap=44)
# *** - to stop drop behaviour if in play mode.
toggledOFF=True
def inv_input(key,subject,mouse):
    global toggledOFF
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