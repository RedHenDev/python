# read from a texture and place tiles based on the color
quad = load_model('quad')
dungeon = Entity(model=Mesh(), texture='brick')
model = dungeon.model

texture = load_texture('heightmap_1')
for y in range(texture.height):
    for x in range(texture.width):
        col = texture.get_pixel(x,y)
        # print(col)
        if col.v > .5: #
            model.vertices.extend([Vec3(x,y,0)+v for v in quad.vertices]) # add quad vertices, but offset.
            model.colors.extend((color.random_color(),) * len(quad.vertices)) # add vertex colors.

'''
the uvs are the same for all the squares in this case, but you could also have
them change based on the tile type so you can use a tilemap
'''
model.uvs = (quad.uvs) * (texture.width * texture.height)
model.generate() # call to create the mesh
