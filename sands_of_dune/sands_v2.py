from ursina import *
import random

app = Ursina()

window.color = color.rgb(255, 255, 255)
window.title = 'Falling Sands 3D'

grid_size = 20
grid = [[None] * grid_size for _ in range(grid_size)]

def input(key):
    if key == 'escape' or key == 'q':
        application.quit()

class Sand(Entity):
    def __init__(self, position=(0, 0, 0), color=color.rgb(194, 178, 128)):
        super().__init__(
            model='cube',
            position=position,
            scale=1,
            color=color,
            texture='brick'
        )

    def input(self, key):
        if key == 'left mouse down':
            destroy(self)

camera = EditorCamera()

def update():
    for y in range(grid_size-2, -1, -1):
        for x in range(grid_size):
            if grid[y][x] and not grid[y+1][x] and random.random() < 0.1:
                grid[y][x].y -= 1
                grid[y+1][x] = grid[y][x]
                grid[y][x] = None

    if held_keys['left mouse']:
        mouse_position = mouse.position
        x, y = int(mouse_position.x), int(mouse_position.y)
        if 0 <= x < grid_size and 0 <= y < grid_size and not grid[y][x]:
            grid[y][x] = Sand(position=(x, y, 0))

app.run()
