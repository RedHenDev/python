"""
Hello world microphone speech to text.
19 Dec 2022
Following directions found here:-
https://realpython.com/python-speech-recognition/
https://github.com/RedHenDev/python-speech-recognition
"""
from pocketsphinx import LiveSpeech
import os
import re # For regular expressions.
import usb_arm

# Let's set up our robot. Beep boop.
try:
    arm = usb_arm.Arm()
except:
    print('No robot. Naughty.')
    arm = None

def findWholeWord(w):
    # This returns a Pattern object.
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

# def mic_listen():
#     speech = LiveSpeech(keyphrase='robot', kws_threshold=1e-20)
#     for phrase in speech:
#         print(phrase.segments(detailed=True))
#         message=str(phrase)
#         os.system(f"say 'I think you said, {message}?'")
#         return message
def mic_listen():
    speech = LiveSpeech()
    for phrase in speech:
        message=str(phrase)
        # os.system(f"say 'Beep-beep-boop, {message}?'")
        return message

def robot_listen(_message):
    if arm is None or arm == None:
        if _message=='' or _message is None:
            _message = 'An analogy to silence.'
        print(_message)
        print('But no robot connected.')
        return

    print(_message)
    if findWholeWord('light')(_message):
        arm.move(usb_arm.LedOn)
    if findWholeWord('up')(_message):
        arm.move(usb_arm.WristUp)
    if findWholeWord('down')(_message):
        arm.move(usb_arm.WristDown)
    if findWholeWord('yes')(_message):
        for i in range(3):
            arm.move(usb_arm.WristDown,0.4)
            arm.move(usb_arm.WristUp,0.4)
    if findWholeWord('right')(_message):
        arm.move(usb_arm.BaseClockWise,2)
    if findWholeWord('close')(_message):
        arm.move(usb_arm.CloseGrips,1)
    if findWholeWord('open')(_message):
        arm.move(usb_arm.OpenGrips,1)
    if findWholeWord('left')(_message):
        arm.move(usb_arm.BaseCtrClockWise,2)
    if findWholeWord('hello')(_message):
        for i in range(3):
            arm.move(usb_arm.BaseClockWise,0.4)
            arm.move(usb_arm.BaseCtrClockWise,0.4)
    # Just a little movement...
    # To signal either completion or nothing understood.
    arm.move(usb_arm.WristUp,0.1)
    arm.move(usb_arm.WristDown,0.1)

# Procedure: listen to mic. Then, pass result to
# robot listen.
os.system("say 'Im a robot, and my name is Pink.'")
while True:
    # if input("Enter to continue>")=='':
        robot_listen(mic_listen())
    # else: break
    # os.system("say 'Anything else?'")
print('-session complete-')