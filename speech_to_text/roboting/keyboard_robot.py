"""
Control robot with keyboard
22 Feb 2023

"""
import os
import usb_arm
from pynput import keyboard

# Let's set up our robot. Beep boop.
try:
    arm = usb_arm.Arm()
except:
    print('No robot. Maybe it is talking to GPT-4?')
    arm = None

def on_press(key):
    try:
        if key == keyboard.Key.up:
            print('The up arrow key is pressed')
            arm.move(usb_arm.LedOn)
        elif key == keyboard.Key.down:
            print('The down arrow key is pressed')
        elif key == keyboard.Key.left:
            arm.move(usb_arm.BaseCtrClockWise,2)
            print('The left arrow key is pressed')
        elif key == keyboard.Key.right:
            arm.move(usb_arm.BaseClockWise,2)
            print('The right arrow key is pressed')
    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Procedure: listen to input. Then, pass result to
# robot listen.
os.system("say 'Im a robot, and you can control me. Hopefully.'")
while True:
    pass


print('-session complete-')
