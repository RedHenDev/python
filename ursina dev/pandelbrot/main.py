from ursina import *

app=Ursina()

# camera.orthographic=True
# camera.fov=2
moi=EditorCamera()
# time.sleep(3)
window.center_on_screen()
window.color=Vec4(0,.8,0,1)

scalar=0.1
for i in range(1,64):
    for j in range(1,64):
        n=Sprite()
        n.color=Vec4(1/64*i,0,1/64*j,1)
        n.x=i*scalar-4
        n.y=j*scalar-4
        n.scale*=scalar
        

app.run()

