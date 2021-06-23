from ursina import *

class SubjectiveController(Entity):
    def __init__(this, **kwargs):
        this.cursor = Entity(parent=camera.ui, model='quad', color=color.black, scale=.04, rotation_z=45)
        super().__init__()
        this.speed = 5
        this.height = 2
        this.camera_pivot = Entity(parent=this, y=this.height)

        camera.parent = this.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        this.mouse_sensitivity = Vec2(40, 40)

        this.gravity = 1
        this.grounded = False
        this.jump_height = 2
        this.jump_duration = .5
        this.jumping = False
        this.air_time = 0
        this.step_height = .5

        for key, value in kwargs.items():
            setattr(this, key ,value)


    def update(this):
        this.rotation_y += mouse.velocity[0] * this.mouse_sensitivity[1]

        this.camera_pivot.rotation_x -= mouse.velocity[1] * this.mouse_sensitivity[0]
        this.camera_pivot.rotation_x= clamp(this.camera_pivot.rotation_x, -90, 90)

        this.direction = Vec3(
            this.forward * (held_keys['w'] - held_keys['s'])
            + this.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

        feet_ray = raycast(this.position+Vec3(0,0.5,0), this.direction, ignore=(this,), distance=.5, debug=False)
        head_ray = raycast(this.position+Vec3(0,this.height-.1,0), this.direction, ignore=(this,), distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            this.position += this.direction * this.speed * time.dt

        # Step up obstacle, e.g. 1 unit cube.
        step_ray_over = raycast(this.position+Vec3(0,this.step_height+0.1,0), this.direction, ignore=(this,), distance=1, debug=False)
        step_ray_under = raycast(this.position+Vec3(0,0.5,0), this.direction, ignore=(this,), distance=1, debug=False)
        if not step_ray_over.hit and step_ray_under.hit:
            this.y += this.step_height

        if this.gravity:
            # gravity
            ray = raycast(this.world_position+(0,this.height,0), this.down, ignore=(this,))
            # ray = boxcast(this.world_position+(0,2,0), this.down, ignore=(this,))

            if ray.distance <= this.height+.1:
                if not this.grounded:
                    this.land()
                this.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - this.world_y < .5: # walk up slope
                    this.y = ray.world_point[1]
                return
            else:
                this.grounded = False

            # if not on ground and not on way up in jump, fall
            this.y -= min(this.air_time, ray.distance-.05) * time.dt * 100
            this.air_time += time.dt * .25 * this.gravity


    def input(this, key):
        if key == 'space':
            this.jump()


    def jump(this):
        if not this.grounded:
            return

        this.grounded = False
        this.animate_y(this.y+this.jump_height, this.jump_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(this.start_fall, delay=this.jump_duration)


    def start_fall(this):
        this.y_animator.pause()
        this.jumping = False

    def land(this):
        # print('land')
        this.air_time = 0
        this.grounded = True


    def on_enable(this):
        mouse.locked = True
        this.cursor.enabled = True


    def on_disable(this):
        mouse.locked = False
        this.cursor.enabled = False