import sounddevice
from os import getcwd
from scipy.io.wavfile import write
import whisper
from queue import Queue
import threading
import uuid

class RecordingService(threading.Thread):
    def __init__(self, audio_segments: Queue):
        threading.Thread.__init__(self)
        self.audio_segments = audio_segments
    
    def run(self):
        fs = 44100
        second = 30
        while True:
            recording = sounddevice.rec( int(second*fs), samplerate=fs, channels=1)
            sounddevice.wait()
            file_name = str(uuid.uuid4())
            filename = f"{getcwd()}\\{file_name}.wav"
            write(filename, fs, recording)
            self.audio_segments.put(filename)

class TranscriptionService(threading.Thread):
    def __init__(self, audio_segments: Queue):
        threading.Thread.__init__(self)
        self.audio_segments = audio_segments
    
    def run(self):
        model = whisper.load_model("base")
        while True:
            result = model.transcribe(self.audio_segments.get())
            print(result.get("text"))

audio_segments = Queue()
recorder = RecordingService(audio_segments)
transciber = TranscriptionService(audio_segments)

recorder.start()
transciber.start()

#def record(second = 10, fs = 44100):
    #recording = sounddevice.rec( int(second*fs), samplerate=fs, channels=1)
    #sounddevice.wait()
    #filename = f"{getcwd()}\\audio.wav"
    #write(filename, fs, recording)
    #return filename

#def transcribe_audio(filename):
    #model = whisper.load_model("base")
    #result = model.transcribe(filename)
    #return result.get("text")
