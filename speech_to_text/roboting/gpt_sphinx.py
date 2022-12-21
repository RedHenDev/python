"""
GPT-3 code.
"""

import pyaudio
import pocketsphinx

# Set up the PocketSphinx decoder
# decoder = pocketsphinx.Decoder.default_decoder()
decoder = pocketsphinx.Decoder()

# Set up the audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

# Start decoding
decoder.start_utt()

# Process the audio
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
    else:
        break

# Finish decoding and search for specific words
decoder.end_utt()
words = [seg.word for seg in decoder.seg()]
if 'robot' in words:
    print('Robot detected!')
if 'goodbye' in words:
    print('Goodbye detected!')

# Clean up
stream.stop_stream()
stream.close()
p.terminate()