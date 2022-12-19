"""
Hello world microphone speech to text.
19 Dec 2022
Following directions found here:-
https://realpython.com/python-speech-recognition/
https://github.com/RedHenDev/python-speech-recognition
"""
import speech_recognition as sr
import re # For regular expressions.
import usb_arm

# Let's set up our robot. Beep boop.
try:
    arm = usb_arm.Arm()
except:
    print('No robot. Naughty.')
    arm = None

print(sr.__version__)
print(sr.Microphone.list_microphone_names())

r = sr.Recognizer()
# index 0 - i.e. default mic.
# NB Microphone is a context manager.
mic = sr.Microphone(device_index=0)

# Now let's try to listen to something...
# NB duration should be no less than 0.5.
with mic as source:
    print('Wait one second please...')
    r.adjust_for_ambient_noise(source,duration=0.75)
    print('Listening...please speak:')
    audio=r.listen(source)

# Set up a response dictionary.
response = {
    "success": True,
    "error": None,
    "transcription": None
}

# Try to recognise speech in the recording.
# If a RequestError or UnknownValueError exception 
# is caught, update the response object.
try:
    response["transcription"] = r.recognize_google(audio)
except sr.RequestError:
    # API unreachable or unresponsive.
    response["success"] = False
    response["error"] = "API unavailable"
except sr.UnknownValueError:
    # Speech garbled.
    response["error"] = "Unable to recognise speech"

# def contains_word(s, w):
#     return (' ' + w + ' ') in (' ' + s + ' ')

def findWholeWord(w):
    # This returns a Pattern object.
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

if arm is None or arm == None:
    print(response["transcription"])
    print('But no robot connected.')
else:
    if findWholeWord('light')(str(response["transcription"])):
        arm.move(usb_arm.LedOn)
    if findWholeWord('yes')(str(response["transcription"])):
        for i in range(3):
            arm.move(usb_arm.WristDown,0.4)
            arm.move(usb_arm.WristUp,0.4)