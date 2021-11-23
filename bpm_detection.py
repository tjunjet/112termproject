import argparse
import array
import math
import wave

import numpy
import pywt
from scipy import signal

# Adapted From: https://github.com/scaperot/the-BPM-detector-python/blob/master/bpm_
# detection/bpm_detection.py
# Modified by me
def read_wav(filename):
    # open file, get metadata for audio
    try:
        waveFile = wave.open(filename, "rb")
    except IOError as error:
        print(error)
        return

    # type = choose_type( waveFile.getsampwidth() ) 
    numberOfSamples = waveFile.getnframes()
    assert numberOfSamples > 0

    samplingFrequency = waveFile.getframerate()
    assert samplingFrequency > 0

    # Read entire file and make into an array
    samps = list(array.array("i", waveFile.readframes(numberOfSamples)))

    try:
        assert numberOfSamples == len(samps)
    except AssertionError:
        print(numberOfSamples, "not equal to", len(samps))

    return samps, samplingFrequency


# Adapted From: https://github.com/scaperot/the-BPM-detector-python/blob/master/bpm_
# detection/bpm_detection.py
# Modified by me
def noAudioData():
    print("No audio data for sample, skipping...")
    return None, None


# Adapted From: https://github.com/scaperot/the-BPM-detector-python/blob/master/bpm_
# detection/bpm_detection.py
# Modified by me
def peakDetect(data):
    maxValue = numpy.amax(abs(data))
    peak_ndx = numpy.where(data == maxValue)
    if len(peak_ndx[0]) == 0:  # if nothing found then the max must be negative
        peak_ndx = numpy.where(data == -maxValue)
    return peak_ndx

# Adapted From: https://github.com/scaperot/the-BPM-detector-python/blob/master/bpm_
# detection/bpm_detection.py
def bpmDetector(data, samplingFrequency):
    cA = []
    cD = []
    correl = []
    cD_sum = []
    levels = 4
    max_decimation = 2 ** (levels - 1)
    min_ndx = math.floor(60.0 / 220 * (samplingFrequency / max_decimation))
    max_ndx = math.floor(60.0 / 40 * (samplingFrequency / max_decimation))

    for loop in range(0, levels):
        cD = []
        # 1. Discrete Wavelet Transform using pywt
        if loop == 0:
            [cA, cD] = pywt.dwt(data, "db4")
            cD_minlen = len(cD) / max_decimation + 1
            cD_sum = numpy.zeros(math.floor(cD_minlen))
        else:
            [cA, cD] = pywt.dwt(cA, "db4")

        # 2) Filter
        cD = signal.lfilter([0.01], [1 - 0.99], cD)

        # 3) Decimate for reconstruction later.
        cD = abs(cD[:: (2 ** (levels - loop - 1))])
        cD = cD - numpy.mean(cD)

        # 4) Recombine the signal before ACF
        #    Essentially, each level the detail coesamplingFrequency (i.e. the HPF values) are concatenated to the beginning of the array
        cD_sum = cD[0 : math.floor(cD_minlen)] + cD_sum

    if [b for b in cA if b != 0.0] == []:
        return noAudioData()

    # Adding in the approximate data as well...
    cA = signal.lfilter([0.01], [1 - 0.99], cA)
    cA = abs(cA)
    cA = cA - numpy.mean(cA)
    cD_sum = cA[0 : math.floor(cD_minlen)] + cD_sum

    # ACF
    correl = numpy.correlate(cD_sum, cD_sum, "full")

    midpoint = math.floor(len(correl) / 2)
    correl_midpoint_tmp = correl[midpoint:]
    peak_ndx = peakDetect(correl_midpoint_tmp[min_ndx:max_ndx])
    if len(peak_ndx) > 1:
        return noAudioData()

    peak_ndx_adjusted = peak_ndx[0] + min_ndx
    bpm = 60.0 / peak_ndx_adjusted * (samplingFrequency / max_decimation)
    # print(bpm)
    return bpm, correl

# Main function to get the median BPM of the code
# This function was modified to get a list of bpms and eventually extract the average bpm
def getBPM(filename):
    parser = argparse.ArgumentParser(description="Process .wav file to determine the Beats Per Minute.")
    parser.add_argument(
        "--window",
        type=float,
        default=3,
        help="Size of the the window (seconds) that will be scanned to determine the bpm. Typically less than 10 seconds. [3]",
    )

    args = parser.parse_args()
    samps, samplingFrequency = read_wav(filename)
    data = []
    bpm = 0
    n = 0
    numberOfSamples = len(samps)
    window_samps = int(args.window * samplingFrequency)
    samps_ndx = 0  # First sample in window_ndx
    max_window_ndx = math.floor(numberOfSamples / window_samps)
    bpms = numpy.zeros(max_window_ndx)

    # Iterate through all windows
    for window_ndx in range(0, max_window_ndx):

        # Get a new set of samples
        # print(n,":",len(bpms),":",max_window_ndx_int,":",samplingFrequency,":",numberOfSamples,":",samps_ndx)
        data = samps[samps_ndx : samps_ndx + window_samps]
        if not ((len(data) % window_samps) == 0):
            raise AssertionError(str(len(data)))

        bpm, correl_temp = bpmDetector(data, samplingFrequency)
        if bpm is None:
            continue
        bpms[window_ndx] = bpm
        correl = correl_temp

        # Iterate at the end of the loop
        samps_ndx = samps_ndx + window_samps

        # Counter for debug...
        n = n + 1

    bpm = numpy.median(bpms)
    print(bpms)
    return bpm

# Things to note:
# 1. bpms: List of the beats_per_minute
# 2. bpm: Average bpm of the music
# 3. Eventually, might need to sync the parameters for beat and beat detection