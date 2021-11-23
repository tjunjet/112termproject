# Referenced: https://www.codegrepper.com/code-examples/python/get+length+of+audio+file+python

import wave
import contextlib

# This function gets the duration of the music in seconds
def getDurationOfMusic(filename):
    with contextlib.closing(wave.open(filename, "r")) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration