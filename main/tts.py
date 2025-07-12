from piper import PiperVoice
import sounddevice as sd
import numpy as p
import wave
import io
import threading
import queue
import importlib.resources
import pathlib

package_models_dir = importlib.resources.files('main').joinpath('models/UK')

VOICE = str(package_models_dir / 'en_GB-northern_english_male-medium.onnx')
CONFIG = str(package_models_dir / 'en_GB-northern_english_male-medium.onnx.json')
PAUSE = 0.15

voice = PiperVoice.load(VOICE, CONFIG)
sample_rate = voice.config.sample_rate

tts_queue = queue.Queue()


def wave_to_p(buffer):
    buffer.seek(0)
    with wave.open(buffer, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        dtype = p.int16 if wf.getsampwidth() == 2 else p.int32
        audio = p.frombuffer(frames, dtype=dtype).astype(p.float32)
        audio /=  p.iinfo(dtype).max
        return audio

def _worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break

        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            voice.synthesize(text,wf)

        audio = wave_to_p(buf)

        mx = p.max(p.abs(audio))
        if mx > 0:
            audio /= mx

        sd.play(audio, samplerate=sample_rate)
        sd.wait()

        tts_queue.task_done()

# start the thread and hope it works
threading.Thread(target=_worker, daemon=True).start()

def speak(text):
    tts_queue.put(text)
    tts_queue.join()
