from random import randrange
from ursina import *
from perlin_noise import PerlinNoise
from ursina.color import random_color
from ursina.scripts import merge_vertices

from settings import * # Includes app = Ursina()



class VertexSheet(Entity):
    def __init__(this):
        super().__init__(
            color=color.lime
        )
        this.quads = []
        for q in range(100):
            bub = Entity(model='quad')
            bub.rotation_x=90
            bub.x = floor(q/10)
            bub.z = floor(q%10)
            bub.y = 0
            bub.color=color.random_color()
            bub.parent = this
            this.quads.append(bub)
        this.combine(auto_destroy=True)
        
        this.model.vertices, this.model.triangles = merge_vertices.merge_overlapping_vertices(
            this.model.vertices,
            this.model.triangles
        )
        this.model.generate()
        for i in this.model.vertices:
            i[1] += randrange(-2,2)*0.1
        this.model.generate()
        
        

v = VertexSheet()
i = 0


EditorCamera()
app.run()