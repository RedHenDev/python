from ursina import *                    # this will import everything we need from ursina with just one line.

# Define some characters we want to use to represent the map
TEMPTY    = ' '
TFLOOR    = '.'
TCORRIDOR = '='
TDOOR     = '&'
TDEADEND  = '^'
TWALL     = '#'
TOBSTACLE = '%'
TCAVE     = '@'
TWATER    = '~'
TROAD     = '*'
TENTRY    = 'E'

CAMERA_SPEED = 10
SCALE = 2
texoffset = 0.0                         # define a variable that will keep the texture offset

def update():
    global texoffset                                 # Inform we are going to use the variable defined outside
    texoffset += time.dt * 0.05                       # Add a small number to this variable
    for tile in water:
        setattr(tile, "texture_offset", (texoffset, texoffset))  # Assign as a texture offset

# Move the camera to a new position but check if it is valid before moving
def moveto(newposition):
    mapposition = newposition / SCALE                       # get the map coords from that position
    if tilemap[int(mapposition[2])][int(mapposition[0])] != TWALL:        # if the new position doesn't have a wall
        camera.position = newposition
    else:
        print("There is a wall in that direction")

def input(key):
    if key == 'i': moveto(camera.position + camera.forward * SCALE)    # where will I move
    if key == 'k': moveto(camera.position + camera.back * SCALE)
    if key == 'j': moveto(camera.position + camera.left * SCALE)
    if key == 'l': moveto(camera.position + camera.right * SCALE)
    if key == 'u': camera.rotation_y -= 90              # rotate camera left
    if key == 'o': camera.rotation_y += 90              # rotate camera righa

app = Ursina()

window.title = 'Ursina Dungeons'                # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Go Fullscreen
window.exit_button.visible = False      # Show the in-game red X that loses the window
window.fps_counter.enabled = True       # Show the FPS (Frames per second) counter

# Open your dungeon map for read
tilemap=[]
with open('dungeon.map') as f:
   for line in f:                       # For each line
       tilemap.append(list(line[:-1]))      # append the line to the map but break it in individual characters first

water = []

for py, line in enumerate(tilemap):
    for px, tile in enumerate(line):
        if tile == TEMPTY:
            continue
        if tile == TFLOOR or tile == TENTRY:    
            if tilemap[px+1][py] == TWATER or tilemap[px-1][py] == TWATER or tilemap[px][py+1] == TWATER or tilemap[px][py-1] == TWATER:
                Entity(model='cube', color=color.white, texture="floor", collider="box", position=(px * SCALE, -0.5 * SCALE, py * SCALE), scale=(SCALE,SCALE,SCALE))
            else:
                Entity(model='plane', color=color.white, texture="floor", collider="box", position=(px * SCALE, 0, py * SCALE), scale=(SCALE,SCALE,SCALE))
            if tile == TENTRY: camera.position = (px*SCALE, 1, py*SCALE)
        if tile == TCORRIDOR:
            Entity(model='plane', color=color.white, texture="corridor", collider="box", position=(px * SCALE, 0, py * SCALE), scale=(SCALE,SCALE,SCALE))
        if tile == TDOOR:
            Entity(model='plane', color=color.white, texture="floor", collider="box", position=(px * SCALE, 0, py * SCALE), scale=(SCALE,SCALE,SCALE))
            Entity(model='cube', color=color.white, texture="door", collider="box", position=(px * SCALE, 0.5 * SCALE, py * SCALE), scale=(SCALE,SCALE,SCALE))
        if tile == TDEADEND:
            Entity(model='plane', color=color.white, texture="deadend", collider="box", position=(px * SCALE, 0, py * SCALE), scale=(SCALE,SCALE,SCALE))
        if tile == TWALL: 
            Entity(model='plane', color=color.white, texture="floor", collider="box", position=(px * SCALE, 0, py * SCALE), scale=(SCALE,SCALE,SCALE))
            Entity(model='cube', color=color.white, texture="wall", collider="box", position=(px * SCALE, 0.5 * SCALE, py * SCALE), scale=(SCALE,SCALE,SCALE))
        if tile == TOBSTACLE:
            Entity(model='plane', color=color.white, texture="obstacle", collider="box", position=(px * SCALE, 0, py * SCALE), scale=(SCALE,SCALE,SCALE))
        if tile == TCAVE:
            Entity(model='plane', color=color.white, texture="cave", collider="box", position=(px * SCALE, 0, py * SCALE), scale=(SCALE,SCALE,SCALE))
        if tile == TWATER:
            Entity(model='plane', color=color.white, texture="floor", collider="box", position=(px * SCALE, -1 * SCALE, py * SCALE), scale=(SCALE,SCALE,SCALE))
            water.append(Entity(model='plane', color=color.rgba(256,256,256,128), texture="water", collider="box", position=(px * SCALE, 0, py * SCALE), scale=(SCALE,SCALE,SCALE)))
        if tile == TROAD:
            Entity(model='plane', color=color.white, texture="road", collider="box", position=(px * SCALE, 0, py * SCALE), scale=(SCALE,SCALE,SCALE))

camera.fov = 110
camera.lens.setNearFar(0.6, 1000)

app.run()                               # opens a window and starts the game.
[Ursina Dungeons for Dummies.txt](https://github.com/pokepetter/ursina/files/4496622/Ursina.Dungeons.for.Dummies.txt)

