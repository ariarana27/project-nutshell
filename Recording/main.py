import sounddevice
from scipy.io.wavfile import write

def record(second = 10, fs = 44100):
    recording = sounddevice.rec( int(second*fs), samplerate=fs, channels=2, dtype='float64')
    sounddevice.wait()
    write("out.wav", fs, recording)

record()