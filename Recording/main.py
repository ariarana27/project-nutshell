import sounddevice
from os import getcwd
from scipy.io.wavfile import write
import whisper

def record(second = 10, fs = 44100):
    recording = sounddevice.rec( int(second*fs), samplerate=fs, channels=1)
    sounddevice.wait()
    filename = f"{getcwd()}\\audio.wav"
    write(filename, fs, recording)
    return filename

def transcribe_audio(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    print(result["text"])
    return result["text"]

audiofile = record()
print(audiofile)
transcription = transcribe_audio(audiofile)