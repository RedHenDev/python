"""
New attempt at inventory system.
May 22nd 2022.
"""
from ursina import *
import random as ra

# Inventory hotbar.
hotbar = Entity(model='quad',parent=camera.ui)
# Set the size and position.
hotbar.scale_y=0.08
hotbar.scale_x=0.8
hotbar.y=-0.5 + (hotbar.scale_y*0.5)
# Appearance.
hotbar.color=color.dark_gray

class Hotspot(Entity):
    def __init__(this):
        super().__init__()
        this.model='quad'
        this.parent=hotbar
        this.color=color.white
        this.scale=(1,0.5)
        this.texture='white_box'

class Item(Draggable):
    def __init__(this):
        super().__init__()
        this.model='quad'
        this.parent=camera.ui
        this.color=color.random_color()
        # Make slightly smaller than hotbar row height.
        this.scale=hotbar.scale * 0.8
        # Make sure is a square.
        this.scale_x = this.scale_y
        # Pick random spot.
        this.x = ra.random()-0.5
        this.y = (ra.random()-0.5)/1.6
        # Fix to designated interval spot.
        this.fix_pos()
    
    def drop(this):
        this.fix_pos() 

    def fix_pos(this):
        scalar=16 # Because 16 is 2 * 10 * 0.8 (scale).
        this.x=round(this.x*scalar)/scalar
        this.y=round(this.y*scalar)/scalar

hotspot=Hotspot()
test_items=[]
for i in range(10):
    test_items.append(Item())

test_items[0].color=color.red
test_items[0].x=-0.6
test_items[0].y=0
# test_items[99].fix_pos()

def inv_input(key,subject,mouse):
    # Pause and unpause, ready for inventory.
    if key=='e' and subject.enabled:
        subject.disable()
        mouse.locked=False
    elif key=='e' and not subject.enabled:
        subject.enable()
        mouse.locked=True