# core_input_keys.py
# Adapted B New 9/1/2022
from raylibpy import *


def main():

    screen_width: int = 800
    screen_height: int = 450

    # init_window(screen_width, screen_height, "raylib [core] example - keyboard input")

    # Define the camera to look into our 3d world (position, target, up vector)
    init_window(screen_width, screen_height, "raylib [core] example - 3d camera 1st person")
    # camera = Camera(
    #     Vector3(4.0, 2.0, 4.0),
    #     Vector3(0.0, 1.8, 0.0),
    #     Vector3(0.0, 1.0, 0.0),
    #     60.0,
    #     CAMERA_PERSPECTIVE
    # )

    # set_camera_mode(camera, CAMERA_FIRST_PERSON)

    origin = screen_width / 2.
    ball_position: Vector2 = Vector2(origin-64, screen_height/2.)
    # pos = Vector3(0.0,0.0,0.0)

    set_target_fps(90)

    while not window_should_close():

        if is_key_down(KEY_RIGHT) or is_key_down(KEY_D):
            ball_position.x += 2.0
        if is_key_down(KEY_LEFT):
            ball_position.x -= 2.0
        if is_key_down(KEY_UP):
            ball_position.y -= 2.0
        if is_key_down(KEY_DOWN):
            ball_position.y += 2.0

        begin_drawing()

        clear_background(RAYWHITE)
        
        draw_text("move the ball with arrow keys", 10, 10, 20, DARKGRAY)

        draw_circle_v(ball_position, 50, MAROON)
        # draw_sphere(pos,50,GREEN)
        
        end_drawing()

    close_window()


if __name__ == '__main__':
    main()