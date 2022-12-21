"""Maplin USB Robot arm control.
Usage -
>>> import usb_arm
>>> arm = usb_arm.Arm()
>>> arm.move(usb_arm.OpenGrips)
>>> arm.doActions(block_left) # WARNING - ARM SHOULD BE ALL THE WAY RIGHT BEFORE TRYING THIS

Trouble:
"NO back end found" - you need to install a libusb driver on your system.

B New and Jojo notes 14th Dec 2022

No LedOff command
"""

import usb_arm

arm = usb_arm.Arm()

actions = [ [usb_arm.WristDown, 0.5], [usb_arm.OpenGrips, 0.5], [usb_arm.ElbowDown],
                 [usb_arm.ShoulderDown]]
arm.doActions(actions)
arm.move(usb_arm.LedOn)
arm.move(usb_arm.BaseClockWise,3)
arm.move(usb_arm.BaseCtrClockWise,3)





