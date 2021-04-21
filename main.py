from scipy.io.wavfile import read,write
import pyaudio
import numpy as np
# import pylab
import matplotlib.pyplot as plt
from scipy.io import wavfile
import time
import sys
import wave
import seaborn as sns
import os
import sounddevice as sd
import json
import asyncio
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer


def callback(indata, outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = indata

def record():
    fs =  48000 #44100
    seconds = 6
    sd.default.device = ['MacBook Pro Microphone','MacBook Pro Speakers']
    myrecording = sd.rec(int(seconds*fs),samplerate=fs,channels=1,dtype=np.int16)
    # instream = sd.InputStream(samplerate=fs,dtype=np.int16,device = 'MacBook Pro Microphone')
    # outstream = sd.OutputStream(samplerate=fs,dtype=np.int16,device = 'MacBook Pro Speakers')
    # with sd.Stream(device=('MacBook Pro Microphone', 'MacBook Pro Speakers'),
    #                samplerate=fs, 
    #                dtype=np.int16, callback=callback):
    #     print('#' * 80)
    #     print('press Return to quit')
    #     print('#' * 80)
    #     strem = sd.get_stream()
    #     strem.
    sd.wait()
    # sd.stop()
    # print(myrecording)
    # sd.play(myrecording)
    # exit()


    # instream.start()
    # outstream.start()
    return myrecording
    
    # sd.wait()
    # write(f"{np.random.randint(999)}.wav",fs,myrecording)
    
def calc_distances(data): # was sound_file
    #The minimun value for the sound to be recognized as a beep
    fs = 48000
    min_val = 4000
    # fs, data = read(sound_file)
    # print(fs)
    data_size = len(data)
    # signal_wave = wave.open(sound_file, 'r')
    sample_rate = fs*100
    # sig = np.frombuffer(signal_wave.readframes(sample_rate), dtype=np.int16)

    #write to json
    # sig = data
    # sig = sig[:]
    # left, right = data[0::2], data[1::2]
    # plt.figure(1)
    # plot_a = plt.subplot(211)
    # plot_a.plot(sig)
    # plot_a.set_xlabel('sample rate * time')
    # plot_a.set_ylabel('energy')
    # plot_b = plt.subplot(212)
    # plot_b.specgram(sig[0], NFFT=1024, Fs=sample_rate, noverlap=900)
    # plot_b.set_xlabel('Time')
    # plot_b.set_ylabel('Frequency')
    # plt.show()
    #plotting
    #The number of indexes on 0.15 seconds
    focus_size = int(0.15 * fs)
    focuses = []
    distances = []
    idx = 0
    while idx < len(data):
        if data[idx] > min_val:
            
            mean_idx = idx + focus_size // 2
            focuses.append(float(mean_idx) / data_size)
            if len(focuses) > 1:
                last_focus = focuses[-2]
                actual_focus = focuses[-1]
                distances.append(actual_focus - last_focus)
            idx += focus_size
        else:
            
            idx += 1
    return distances 

def accept_test(pattern, test, min_error):
    for element in test:
        for i, dt in enumerate(pattern):
            #print(test[element][0]['distance'])
            if dt - test[element][0]['distance'][i] < min_error:
                return [True,element]
        # if len(pattern) > len(test[element][0]['distance']):
        #     return [False,None ]
        # for i, dt in enumerate(pattern):
        #     if not dt - test[element][0]["distance"][i] < min_error:
        #         return [False,None ]
    return [False,None ]

def main():
    with open("dejavu.cnf.SAMPLE") as f:
        config = json.load(f)

    # create a Dejavu instance
    djv = Dejavu(config)

    # Fingerprint all the mp3's in the directory we give it
    djv.fingerprint_directory("audio_samples", [".wav"])
    print("complete")

    secs = 5
    results = djv.recognize(MicrophoneRecognizer, seconds=secs)
    if results is None:
        print("Nothing recognized -- did you play the song out loud so your mic could hear it? :)")
    else:
        print(f"From mic with {secs} seconds we recognized: {results}\n")


    # choice = input("test(T) or Record(R): ").capitalize()
    # if choice == "T":
    #     names = [_ for _ in os.listdir() if ".wav" in _]
    #     for i in range(len(names)):
    #         print(f'{i}: {names[i]}')
    #     try:
    #         file1 = int(input("Choose filename to start with number: "))
    #     except:
    #         print(f"USAGE: must input an integer between 0 and {len(names)-1}")
    #         exit()

    #     if file1 > len(names) or file1 < 0:
    #         print(f"USAGE: must input an integer between 0 and {len(names)-1}")
    #         exit()
    #     print(file1)
    #     pattern = calc_distances(names[file1])
    #     file2 = int(input("Test against Another file: "))
    #     if file2 > len(names) or file2 < 0:
    #         print(f"USAGE: must input an integer between 0 and {len(names)-1}")
    #         exit()
    #     test = calc_distances(names[file2])

    # with open('data.txt') as json_file:
    #     data = json.load(json_file)
    # # sound_file = "patientCall.wav"
    # # data[sound_file] = []
    # # data[sound_file].append({
    # #     "distance": calc_distances(sound_file)
    # # })    
    # # with open('data.txt', 'w') as outfile:
    # #     json.dump(data, outfile)
    # # exit()
    # min_error = 0.005
    # while(1):
    #     recording = record()
    #     distance_list = calc_distances(recording)
    #     match = accept_test(distance_list,data,min_error)
    #     print(match[1])
# the minimum difference between the patterns in seconds
        
        # print( accept_test(pattern, test, min_error))
    # elif choice == "R":
    #     print("Start Recording")
    #     record()
    #     print("Stop Recording")
    # else:
    #     print("USAGE: Make a choice T or R")
    #     exit()
if __name__ == '__main__':
    main()