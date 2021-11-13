# Adapted from: https://newbedev.com/trying-to-get-the-frequencies-of-a-wav-file-in-python

import aubio
from aubio import source
import pyaudio

# Initializing paramters
BUFFER_SIZE             = 2048
CHANNELS                = 1
FORMAT                  = pyaudio.paFloat32
METHOD                  = "default"
SAMPLE_RATE             = 4410
HOP_SIZE                = BUFFER_SIZE // 4
PERIOD_SIZE_IN_FRAME    = HOP_SIZE
WIN_SIZE = 4096

# Creating a function to get the pitch

def get_pitch(file):
    s = source(file, SAMPLE_RATE, HOP_SIZE)
    # SAMPLE_RATE = s.samplerate

    tolerance = 0.8

    pitch_o = aubio.pitch("yin", WIN_SIZE, HOP_SIZE, SAMPLE_RATE)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    # Creating a list of pitches
    pitches = []
    # Creating confidence level for the pitch
    confidences = []

    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        pitches += [pitch]
        confidence = pitch_o.get_confidence()
        confidences += [confidence]
        total_frames += read
        if read < HOP_SIZE: break

    # Getting the pitches at different intervals
    return pitches