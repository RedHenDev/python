import numpy as np
import noise
from PIL import Image
import random

seed = random.randint(0, 999999)

water = [106, 146, 169]
water1 = [125, 169, 198]
water2 = [143, 194, 223]
water3 = [184, 221, 247]

sand = [255, 255, 153]

grass = [71, 163, 71]
grass1 = [91, 163, 91]

stone = [161, 161, 161]
darkStone = [141, 141, 141]

snowNStone = [200, 200, 200]
snow = [250, 250, 250]

shape = (512, 512)
width = shape[0]
height = shape[1]
scale = 100  # Number that determines at what distance to view the noisemap
octaves = 4  # the number of levels of detail you want you perlin noise to have
persistence = 0.5  # number that determines how much detail is added or removed at each octave (adjusts frequency)
lacunarity = 2.60  # number that determines how much each octave contributes to the overall shape (adjusts amplitude)

world = np.zeros(shape)
for x in range(width):
    for y in range(height):
        world[x][y] = noise.pnoise2(x / scale,
                                    y / scale,
                                    octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=500,
                                    repeaty=500,
                                    base=0)


def add_color(arr):
    color_world = np.zeros(arr.shape + (3,))
    for x in range(width):
        for y in range(height):
            if arr[x][y] < .10:
                color_world[x][y] = water
            elif arr[x][y] < .20:
                color_world[x][y] = water1
            elif arr[x][y] < .30:
                color_world[x][y] = water2
            elif arr[x][y] < .40:
                color_world[x][y] = water3
            elif arr[x][y] < .475:
                color_world[x][y] = sand
            elif arr[x][y] < .60:
                color_world[x][y] = grass
            elif arr[x][y] < .70:
                color_world[x][y] = grass1
            elif arr[x][y] < .80:
                color_world[x][y] = stone
            elif arr[x][y] < .90:
                color_world[x][y] = darkStone
            elif arr[x][y] < .95:
                color_world[x][y] = snowNStone
            elif arr[x][y] < 1.0:
                color_world[x][y] = snow
    return color_world


# get world between 0 and 1
max_grad = np.max(world)
min_grad = np.min(world)
world = (world - min_grad) / (max_grad - min_grad)

# Show noise
im = Image.fromarray(np.uint8(world * 255), "L")
im.save("../assets/resources/gen/imageHeight" + str(seed) + ".png")
im.show()

# make world height colorful
color_world = add_color(world)

# Create colored world height map image to view
im = Image.fromarray(color_world.astype("uint8"), "RGB")
im.save("../assets/resources/gen/imageColor" + str(seed) + ".png")
im.show()
