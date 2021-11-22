# Using aubio to get a list of pitches

import aubio
from aubio import source

# Initializing the parameters
BUFFER_SIZE             = 2048
SAMPLE_RATE             = 341
HOP_SIZE                = BUFFER_SIZE // 4
CHANNELS                = 1
WIN_SIZE                = 4096

# Function to get a list of pitches of the song
def getListOfPitches(file):
    # Creating the source object that allows us to sample the file based on a 
    # specific sample rate and hop_size
    sourceObject = source(file, SAMPLE_RATE, HOP_SIZE)
    # Setting the sound tolerance
    tolerance = 0.8

    # Creating a pitch object
    pitchObject = aubio.pitch("yin", WIN_SIZE, HOP_SIZE, SAMPLE_RATE)
    pitchObject.set_unit("midi")
    pitchObject.set_tolerance(tolerance)

    # Creating a list of pitches
    pitches = []
    
    while True:
        samples, read = sourceObject()
        pitch = pitchObject(samples)[0]
        pitches.append(pitch)
        if read < HOP_SIZE: break

    # Getting the pitches at different intervals 
    # Sample Rate = 4410
    return pitches