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
            arm.move(usb_arm.WristUp,0.5)
        elif key == keyboard.Key.down:
            arm.move(usb_arm.WristDown,0.5)
            print('The down arrow key is pressed')
        elif key == keyboard.Key.left:
            arm.move(usb_arm.BaseCtrClockWise,0.5)
            print('The left arrow key is pressed')
        elif key == keyboard.Key.right:
            arm.move(usb_arm.BaseClockWise,0.5)
            print('The right arrow key is pressed')
        elif key==keyboard.Key.space:
            arm.move(usb_arm.LedOn)
    except AttributeError:
        pass

os.system("say 'Im a robot, and you can control me. Hopefully.'")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Procedure: listen to input. Then, pass result to
# robot listen.

#while True:
#    pass

print('-session complete-')
