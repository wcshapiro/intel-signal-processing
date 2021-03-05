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

# we will use the size of the array
# to determine the duration of the sound
def record():
    fs = 44100
    seconds = 15
    sd.default.device = 'MacBook Pro Microphone'
    myrecording = sd.rec(int(seconds*fs),samplerate=fs,channels=1,dtype=np.int16)
    sd.wait()
    write(f"{np.random.randint(999)}.wav",fs,myrecording)
    
def calc_distances(sound_file):
    #The minimun value for the sound to be recognized as a knock
    min_val = 5000
    fs, data = read(sound_file)
    print(fs)
    data_size = len(data)
    signal_wave = wave.open(sound_file, 'r')
    sample_rate = fs*100
    sig = np.frombuffer(signal_wave.readframes(sample_rate), dtype=np.int16)
    sig = sig[:]
    left, right = data[0::2], data[1::2]
    plt.figure(1)
    plot_a = plt.subplot(211)
    plot_a.plot(sig)
    plot_a.set_xlabel('sample rate * time')
    plot_a.set_ylabel('energy')
    plot_b = plt.subplot(212)
    plot_b.specgram(sig, NFFT=1024, Fs=sample_rate, noverlap=900)
    plot_b.set_xlabel('Time')
    plot_b.set_ylabel('Frequency')
    plt.show()
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
    if len(pattern) > len(test):
        return False
    for i, dt in enumerate(pattern):
        if not dt - test[i] < min_error:
            return False
    return True 

def main():
    choice = input("test(T) or Record(R): ").capitalize()
    if choice == "T":
        names = [_ for _ in os.listdir() if ".wav" in _]
        for i in range(len(names)):
            print(f'{i}: {names[i]}')
        try:
            file1 = int(input("Choose filename to start with number: "))
        except:
            print(f"USAGE: must input an integer between 0 and {len(names)-1}")
            exit()

        if file1 > len(names) or file1 < 0:
            print(f"USAGE: must input an integer between 0 and {len(names)-1}")
            exit()
        print(file1)
        pattern = calc_distances(names[file1])
        file2 = int(input("Test against Another file: "))
        if file2 > len(names) or file2 < 0:
            print(f"USAGE: must input an integer between 0 and {len(names)-1}")
            exit()
        test = calc_distances(names[file2])
# the minimum difference between the patterns in seconds
        min_error = 0.01
        print( accept_test(pattern, test, min_error))
    elif choice == "R":
        print("Start Recording")
        record()
        print("Stop Recording")
    else:
        print("USAGE: Make a choice T or R")
        exit()
if __name__ == '__main__':
    main()