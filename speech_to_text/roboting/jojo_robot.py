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

arm.move(usb_arm.LedOn)
arm.move(usb_arm.BaseClockWise,3)
arm.move(usb_arm.BaseCtrClockWise,3)
arm.move(usb_arm.WristDown,1)
arm.move(usb_arm.WristUp,1)
arm.move(usb_arm.LedOn)

#actions = [[usb_arm.ElbowDown, 0.5], [usb_arm.CloseGrips, 0.5], [usb_arm.ElbowUp]]
#arm.doActions(actions)

""""
arm.move(usb_arm.ElbowDown)
arm.move(usb_arm.ElbowUp)
arm.move(usb_arm.ElbowUp)
#arm.move(usb_arm.ShoulderUp)
#arm.move(usb_arm.ShoulderUp)
arm.move(usb_arm.ShoulderDown)
arm.move(usb_arm.BaseClockWise)

for i in range(3):
    arm.move(usb_arm.LedOn)
    arm.move(usb_arm.WristDown)
    arm.move(usb_arm.WristDown)
    #arm.move(usb_arm.WristUp)
"""

#for i in range(3):
    #arm.move([0,0,1])
    #arm.move([16,0,0])
    #arm.move([32,0,0])
    #arm.move(usb_arm.CloseGrips)
    #arm.move(usb_arm.OpenGrips)
    
    #arm.move(usb_arm.LedOn)
    #arm.move(usb_arm.WristUp) 
    #arm.move(usb_arm.WristDown)
    
    #arm.move(usb_arm.LedOn)
    #arm.move(usb_arm.OpenGrips)
    #arm.move(usb_arm.ElbowUp)
    #arm.move(usb_arm.CloseGrips)
    #arm.move(usb_arm.ElbowDown)
    
# arm.doActions(actions)

