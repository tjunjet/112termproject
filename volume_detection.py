# File for volume detection

import wave
import numpy
import sys
import math
import pyaudio
import aubio

BUFFER_SIZE             = 2048
CHANNELS                = 1
FORMAT                  = pyaudio.paFloat32
METHOD                  = "default"
SAMPLE_RATE             = 44100
HOP_SIZE                = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME    = HOP_SIZE

# So we don't get a truncated string
numpy.set_printoptions(threshold = sys.maxsize)

# Here, we will use the wave library to detect the average volumes in a specific sample

def get_volumes(file):
    # Reading the wave file
    waveFile = wave.open(file, "rb")
    # Getting the parameters of the wave file
    # These parameters include:
    # 0. nchannels
    # 1. sample width
    # 2. Frame Rate / Sampling Rate
    # 3. Number of frames sampled
    # 4. Compression type 
    # 5. Compression Name (If the file is compressed)
    # The S/N is the index that we will extract
    params = waveFile.getparams()
    # Here, we want to find the number of frames sampled from the music
    # Thus, we will use params[3], as mentioned at the top
    numberOfFrames = params[3]
    # Finally, we want to use the .readframes() functions to read the frames
    # This will return us a series of hexadecimal encodings, that we can use to get 
    # volume data
    samples = waveFile.readframes(numberOfFrames)
    # Close the wavefile
    samples = numpy.fromstring(samples, numpy.int16)
    samples = list(samples)

    # Initializing a list of volumes
    volumes = []

    # Using a while loop to get a string of average volumes:
    while len(list(samples)) != 0:
        samps = []
        # Getting a list of samples for every 100 inputs
        for i in range(100):
            samps.append(samples[i])
        # Getting the median of all these volumes
        averageVolume = numpy.median(samps)
        volumes.append(averageVolume)
        # Remove the first 100 values
        for i in range(100):
            samples.pop(i)


    # Compute the energy (volume)
    # of the current frame.
    volume = numpy.sum(samples**2)/len(samples)

    # Format the volume output so it only
    # displays at most six numbers behind 0.
    volume = "{:6f}".format(volume)
    return volume

print(get_volumes("Music/Forever Bound - Stereo Madness.wav"))