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

class Item(Draggable):
    def __init__(this):
        super().__init__()
        this.model='quad'
        this.parent=camera.ui
        this.color=color.random_color()
        this.scale=hotbar.scale
        this.scale_x = this.scale_y
        this.x = ra.random()-0.5
        this.y = ra.random()-0.5
        this.fix_pos()
    
    def drop(this):
        this.fix_pos() 

    def fix_pos(this):
        this.x=round(this.x*10)/10
        this.y=round(this.y*10)/10

hotspot=Hotspot()
test_items=[]
for i in range(100):
    test_items.append(Item())

def inv_input(key,subject,mouse):
    # Pause and unpause, ready for inventory.
    if key=='e' and subject.enabled:
        subject.disable()
        mouse.locked=False
    elif key=='e' and not subject.enabled:
        subject.enable()
        mouse.locked=True