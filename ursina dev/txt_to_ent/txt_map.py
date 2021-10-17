"""Text file to 3D map"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Create ground with collider.
grund = Entity(model='quad',rotation_x=90,scale=100)
grund.collider = 'box'
grund.texture='grass'
grund.texture_scale*=10
# Sky colour.
window.color = color.cyan

# Setup camera/subject.
eye = FirstPersonController() #EditorCamera()
eye.y = 32
eye.cursor.visible=False

# Output to textbox.
mo = None
def report(_string):
    global mo
    if mo != None: destroy(mo)
    mo = Text(  text='<white><bold>'+_string,
                background=True)
    mo.background.color = color.black66
    mo.scale *= 1
    mo.x = -0.52
    mo.y = 0.4
    # mo.appear(speed=0.05)

def mesh_build(_string):
    c = 0
    z = 0
    x = 0
    y = 0
    shape = load_model('cube')
    terrain = Entity(model=Mesh())
    model = terrain.model
    # r_string = reversed(_string)
    for i in _string:
        if i=='\n':
            c = 0
            z += 1
        else:
            x = c
            c += 1
            y = int(i)
            # We multiply by Vec3(x,0,z) in order to scale by
            # value of character from _string.
            # We add 0.5 to y in first Vec3 in order to align
            # with 0 on y axis.
            """
            model.vertices.extend(  [Vec3(1,y+1,1)*(Vec3(x,0,z) +
                                    v) for v in shape.vertices])
            """
            model.vertices.extend(  [Vec3(1,1+y/10,1)*(Vec3(x,0.5,1-z) +
                                    v) for v in shape.vertices])
            # add vertex colors [PA note.]
            """
            model.colors.extend(    (color.random_color(),) * 
                                    len(shape.vertices))
            """
            y += 0.01
            model.colors.extend(    (color.rgba(0,255/y,255/y,255),) * 
                                    len(shape.vertices))
            
            '''
            [PA note]
            the uvs are the same for all the squares in this case, but you could also have
            them change based on the tile type so you can use a tilemap
            '''
            model.uvs = (shape.uvs) * (len(_string))
            # Now actually generate the mesh and
            # add collider.
            terrain.collider=model
            model.generate()


def city_build(_string):
    z = 0
    count = 0
    for i in _string:
        if i=='\n': 
            z+=2
            count=0
        else: 
            x = count*2
            e = Entity( model='cube',x=x,y=float(i)/2,z=-z,
                        scale_y=int(i))
            e.texture='brick'
            e.texture_scale.y = (e.scale_y*2)
            e.collider='box'
            count+=1

def pi_city_build(_string):
    global mrPi
    z = 0
    count = 0
    for i in _string:
        if i=='\n': 
            z+=1
            count=0
        elif i==' ':
            continue
        else: 
            x = count
            e = Entity( model='cube',x=x,y=0.5,z=-z)
            e.scale_y = 1 + int(i)/10
            # e.texture='brick'
            # e.texture_scale.y = (e.scale_y*2)
            e.collider='box'
            y = int(i) + 0.01 # Prevent division by zero.
            # e.color = color.rgba(0,255/y,255/y,255)
            if i == '1': e.color=color.green
            else: e.color = color.rgba(0,255/y,255/y,255)
            count+=1
            e.parent=mrPi

def ord_city_build(_string):
    global mrPi
    z = 0
    count = 0
    for i in _string:
        if i=='\n': 
            z+=2
            count=0
        elif i==' ':
            count += 1
            continue
        else: 
            x = count
            e = Entity( model='cube',x=x,y=0.5,z=-z)
            e.scale_y = 4 + ord(i)/100
            # e.texture='brick'
            # e.texture_scale.y = (e.scale_y*2)
            e.collider='box'
            y = ord(i)/100 + 0.01 # Prevent division by zero.
            e.color = color.rgba(0,255/y,255/y,200)
            count+=1
            e.parent=mrPi

def load(_fileName):
    import sys, os

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)

    with open(_fileName, 'r') as f:
        txt_data = f.read()

    return txt_data

def update():
    if mouse.hovered_entity!=None:
        # report(str(round((mouse.hovered_entity.scale.y-1)*10)))
        report(chr(round((mouse.hovered_entity.scale_y-4)*100)))

def input(key):
    if key=='escape': quit()
    if key=='h': report("hi")

# Load file, report content to textbox, and build.
# _data = load('test_map.txt')
_data = load('test_2_map.txt')
report(_data)
# city_build(_data)
mrPi = Entity()
# pi_city_build(_data)
ord_city_build(_data)
# mrPi.combine(auto_destroy=True)
# mrPi.collider=mrPi.model
# mesh_build(_data)

app.run()