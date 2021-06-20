from ursina import *

app = Ursina()

player = Entity(model='cube', color=color.orange)

def update():   # update gets automatically called.
    player.x += held_keys['d'] * .1
    player.x -= held_keys['a'] * .1

app.run()   # opens a window and starts the game.
