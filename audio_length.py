# Adapted from: https://www.codegrepper.com/code-examples/python/get+length+of+audio+file+python

import wave
import contextlib

def getDurationOfMusic(filename):
    with contextlib.closing(wave.open(filename, "r")) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration

print(getDurationOfMusic("Music/Forever Bound - Stereo Madness.wav"))
