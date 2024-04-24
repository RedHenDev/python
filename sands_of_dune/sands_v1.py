from ursina import *
from random import randint
from ursina.prefabs import first_person_controller

app = Ursina()

# Define block size and grid dimensions
block_size = 1
grid_width = 10
grid_height = 10
grid_depth = 10

# Create empty grid to store block data
grid = [[[None for _ in range(grid_depth)] for _ in range(grid_width)] for _ in range(grid_height)]

# Function to spawn a new block at the top of the grid
def spawn_block():
    global grid
    # Choose a random block type
    block_type = randint(1, 6)
    # Find an empty slot in the top row
    for x in range(grid_width):
        if grid[x][grid_height - 1][0] is None:
            # Place the block
            grid[x][grid_height - 1][0] = Entity(model="cube", color=color.rgb(randint(0, 255), randint(0, 255), randint(0, 255)), scale=block_size)
            return
    # Grid is full, game over
    print("Game Over!")
    #app.quit()

# Function to check if a block can fall down
def can_fall(x, y, z):
    global grid
    if y <= 0 or grid[x][y - 1][z] is not None:
        return False
    return True

# First-person camera and movement
camera = first_person_controller.FirstPersonController()
camera.gravity = 0.0
speed = 4

# Function to update the grid and move falling blocks
def update():
    global grid
    for x in range(grid_width):
        for y in range(grid_height):
            for z in range(grid_depth):
                if grid[x][y][z] is not None:
                    if can_fall(x, y, z):
                        # Check if the block below exists before accessing its position
                        if grid[x][y - 1][z] is not None:
                            # Move the block down only if there's a block below
                            grid[x][y][z].position = grid[x][y - 1][z].position
                            grid[x][y - 1][z] = grid[x][y][z]
                            grid[x][y][z] = None


    # Movement based on WASD keys
    dt = 0.1
    if held_keys["d"]:
        camera.position += camera.right * speed * dt
    if held_keys["a"]:
        camera.position -= camera.right * speed * dt
    if held_keys["w"]:
        camera.position += camera.forward * speed * dt
    if held_keys["s"]:
        camera.position -= camera.forward * speed * dt
        spawn_block()                            
# Spawn the initial block
spawn_block()
app.run()
# Game loop
while True:
    update()
    
