"""Maplin USB Robot arm control"""
import os
os.environ['DYLD_LIBRARY_PATH'] = '/opt/local/lib'
import usb.core
from time import sleep


class BitPattern(object):
    """A bit pattern to send to a robot arm"""
    __slots__ = ['arm', 'base', 'led']

    def __init__(self, arm, base, led):
        self.arm = arm
        self.base = base
        self.led = led

    def __iter__(self):
        return iter([self.arm, self.base, self.led])

    def __getitem__(self, item):
        return [self.arm, self.base, self.led][item]

    def __or__(self, other):
        return BitPattern(self.arm | other.arm,
                          self.base | other.base,
                          self.led | other.led)

CloseGrips =    BitPattern(1, 0, 0)
OpenGrips =     BitPattern(2, 0, 0)
Stop =          BitPattern(0, 0, 0)
WristUp =       BitPattern(0x4, 0, 0)
WristDown =     BitPattern(0x8, 0, 0)
ElbowUp =       BitPattern(0x10, 0, 0)
ElbowDown =     BitPattern(0x20, 0, 0)
ShoulderUp =    BitPattern(0x40, 0, 0)
ShoulderDown =  BitPattern(0x80, 0, 0)
BaseClockWise = BitPattern(0, 1, 0)
BaseCtrClockWise = BitPattern(0, 2, 0)
LedOn =         BitPattern(0, 0, 1)


class Arm(object):
    """Arm interface"""
    __slots__ = ['dev']

    def __init__(self):
        self.dev = usb.core.find(idVendor=0x1267)
        self.dev.set_configuration()

    def tell(self, msg):
        """Send a USB messaqe to the arm"""
        self.dev.ctrl_transfer(0x40, 6, 0x100, 0, msg)

    def safe_tell(self, fn):
        """Send a message to the arm, with a stop
        to ensure that the robot stops in the
        case of an exception"""
        try:
            fn()
        except:
            self.tell(Stop)
            raise

    def move(self, pattern, time=1):
        """Perform a pattern move with timing and stop"""
        self.tell(pattern)
        sleep(time)
        self.tell(Stop)

    def doActions(self, actions):
        """Params: List of actions - each is a list/tuple of BitPattern and time
         (defaulting to 1 if not set)"""
        #Validate
        for action in actions:
            if not 1 <= len(action) <= 2:
                raise ValueError("Wrong number of parameters in action %s" %
                                 (repr(action)))
            if not isinstance(action[0], BitPattern):
                raise ValueError("Not a valid action")
        #Do
        try:
            for action in actions:
                if len(action) == 2:
                    time = action[1]
                else:
                    time = 1
                self.move(action[0], time)
        except:
            self.move(Stop)
            raise


block_left = [[ShoulderDown], [CloseGrips, 0.4], [ShoulderUp],
              [BaseClockWise, 10.2], [ShoulderDown],
              [OpenGrips, 0.4], [ShoulderUp, 1.2]]
block_right = [[ShoulderDown], [CloseGrips, 0.4], [ShoulderUp],
               [BaseCtrClockWise, 10.2], [ShoulderDown],
               [OpenGrips, 0.4], [ShoulderUp, 1.2]]
left_and_blink = list(block_left)
left_and_blink.extend([[LedOn, 0.5], [Stop, 0.5]] * 3)
