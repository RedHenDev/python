# Imports
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Create app
app = Ursina()

# Terrain
t = Entity(
    model=Terrain("imageHeight225058", skip=3),
    scale=(1024, 50, 1024),
    texture="copy"
)

t.collider = t.model

water = Entity(model="plane", collider="plane", color=rgb(184, 221, 247), scale=(1024, 1, 1024))
water.position = (0, 22.5, 0)

# Misc
player = FirstPersonController()
player.position = (0, 75, 0)
scene.fog_color = color.gray
scene.fog_density = .005
Sky()

# Run app
app.run()

# https://stackoverflow.com/questions/59867493/how-to-make-perlin-noise-color-gradient-generation-in-python-similar-to-the-nois
