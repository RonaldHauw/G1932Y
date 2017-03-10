
import numpy
import analyse
import pyaudio
import wave
from math import *
import time


def get_spectrum(data):
    low_F = Middelpuntsregel(f, 18, data)
    mid_F = Middelpuntsregel(f, 500, data)
    high_F = Middelpuntsregel(f, 10000, data)
    return low_F, mid_F, high_F


def Middelpuntsregel(f, k, dataset):
    h = 0.00048828125
    sum = f(dataset[0], k, 0) * 0.5
    for i in range(1, 2047):
        step = i*h
        sum += f(dataset[i], k, step)
    sum += f(dataset[2047], k, 2047*h) * 0.5
    sum *= h
    return sum


def f(x, k, i):
    return x * sin(k * i)


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
ANAL_RATE = 10 # number of sepate spectrums analysis per second

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)


print "recording..."
treshold = 3
nbsuccesses = 2
Running = True
lenf = 8
meaner_tot = []
mean = []
index = []
for i in range(0,8):
    meaner_tot.append(0)
    mean.append(0)
    index.append(0)
while Running:
    meaner_tot = []
    for i in range(0,8):
        meaner_tot.append(0)
    print "REFRESH"
    #sample
    for k in range(1, 700): ## aantal metingen nodig in dat deel
        data = stream.read(CHUNK)
        samps = numpy.fromstring(data, dtype=numpy.int16)
        lenf = 8
        fou = numpy.fft.fft(samps,lenf)
        four = []
        for i in range(0,lenf):
            x= int(abs(fou[i]))
            four.append(x)
            meaner_tot[i] += x
            mean[i] = float(meaner_tot[i])/float(k)
            if four[i]> treshold*mean[i]:
                index[i] +=1
            elif four[i] > 0.5*treshold*mean[i]:
                index[i] += 0
            else:
                index[i] =0
            if index[i] >= nbsuccesses:
                print "beat"





print "finished recording"




# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()



#####################################################
# import numpy
# import pyaudio
# import analyse
#
# # Initialize PyAudio
# pyaud = pyaudio.PyAudio()
#
# # Open input stream, 16-bit mono at 44100 Hz
# # On my system, device 4 is a USB microphone
# stream = pyaud.open(
#     format = pyaudio.paInt16,
#     channels = 1,
#     rate = 44100,
#     input_device_index = 2,
#     input = True)
#
# while True:
#     # Read raw microphone data
#     rawsamps = stream.read(1024)
#     # Convert raw data to NumPy array
#     samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
#     # Show the volume and pitch
#     print analyse.loudness(samps), analyse.musical_detect_pitch(samps)