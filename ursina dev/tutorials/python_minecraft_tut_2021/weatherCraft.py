"""
Weather functions.
"""
from ursina import color, window, time

class Weather:
    def __init__(this, rate=0.1):
        this.red = 0
        this.green = 200
        this.blue = 211

        this.darknessRate = rate

        this.towardsNight = 1

    def setSky(this):
        window.color = color.rgb(   this.red,
                                    this.green,
                                    this.blue)

    def update(this):
        if this.green > 0:
            this.green -= this.darknessRate * time.dt
        if this.blue > 0:
            this.blue -= this.darknessRate * time.dt
        this.setSky()
