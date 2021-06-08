""" Tutorial for a solar system using Ursina """
# Part 4.

from ursina import *
#from ursina.prefabs.first_person_controller import FirstPersonController
import random as ra
import numpy as np

app = Ursina()

window.color = color.black # color.rgb(0,0,0)

# Our list of planets.
planets = []

# Data from the real solar system!
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
# Let's name our solar system - Copernicus (daughter?).
# Million km
dataDist = [57.9,	108.2,	149.6,	227.9,	778.6,	1433.5,
            2872.5,	4495.1,	5906.4]
# Km/s
dataVel = [47.4,	35.0,	29.8,
           24.1,	13.1,	9.7,	6.8,	5.4,	4.7]
# Km
dataDia = [4879,	12104,	12756,	6792,	142984,	120536,
           51118,	49528,	2370]

scalar_Ov = 0.001
scalar_Di = 0.006
scalar_Dist = 2


def input(key):
    if key == 'escape' or key == 'q':
        quit()
    if key == 'space':
        sun.scale *= 2

def update():
    sun.rotation_y += 1
    sun.rotation_x += 1

    for p in planets:
        p.orbit()
        p.rotate()

# Our Planet class -- for making planets.
class Planet:
    def __init__(this):
        #randS = ra.randint(3,24)
        this.name = 'default'
        this.orbitalTheta = ra.randint(0,360)
        this.orbitalVel = 0.01
        this.solarDist = 100
        this.rings = False
        this.ent = Entity(model='sphere',scale=1,
                          color=color.lime,texture='assets/2k_moon')

    def orbit(this):
        this.ent.x = this.solarDist * np.cos(this.orbitalTheta) * 1.4
        this.ent.z = this.solarDist * np.sin(this.orbitalTheta)
        this.orbitalTheta += this.orbitalVel

    def rotate(this):
        this.ent.rotation_y -= 0.1

# The sun (centre of the solar system -> )
sun = Entity(model='sphere',
             texture='assets/2k_sun',scale=64)


# Birth our planets in a loop. Add/append them to the planets[] list.
for p in range(9):
    baby = Planet()
    baby.solarDist = dataDist[p] * scalar_Dist
    baby.orbitalVel = dataVel[p] * scalar_Ov
    baby.ent.scale = dataDia[p] * scalar_Di
    planets.append(baby)

# Colours of each planet.
planets[2].ent.color=color.blue
planets[3].ent.color=color.red

planets[5].rings = True # Saturn ;)
ring = Entity(model='sphere',scale=planets[5].ent.scale*1.6)
ring.position = planets[5].ent.position
ring.scale_y = 1
ring.color=color.yellow
ring.reparent_to(planets[5].ent)

smithy = EditorCamera(move_speed=1000)
camera.clip_plane_far=20000

smithy.y = 8500
smithy.rotation_x = 90

#jessie = Sky()
#jessie.texture = 'assets/starsTex'

#subject = FirstPersonController()
app.run()











