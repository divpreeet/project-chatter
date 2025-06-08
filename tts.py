from piper import PiperVoice
import sounddevice as sd
import numpy as p
import re
import tempfile
import wave

VOICE = "models/UK/en_GB-northern_english_male-medium.onnx"
CONFIG = "models/UK/en_GB-northern_english_male-medium.onnx.json"
PAUSE = 0.15

voice = PiperVoice.load(VOICE, CONFIG)


def wave_to_p(wav_path):
    with wave.open(wav_path, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        dtype = p.int16 if wf.getsampwidth() == 2 else p.int32
        audio = p.frombuffer(frames, dtype=dtype).astype(p.float32) / p.iinfo(dtype).max
        return audio, wf.getframerate()

def speak(text):
    sample_rate = voice.config.sample_rate
    pause_samples = p.zeros(int(PAUSE * sample_rate), dtype=p.float32)
    parts = re.split(r'([.,?!])', text)
    all_audio = []
    i = 0
    while i < len(parts):
        segment = parts[i]
        if i + 1 < len(parts) and parts[i+1] in ".,?!":
            segment += parts[i+1]
        segment = segment.strip()
        if segment:
            with tempfile.NamedTemporaryFile(suffix=".wav") as tmp_wav:
                with wave.open(tmp_wav.name, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(voice.config.sample_rate)
                    voice.synthesize(segment, wav_file)

                audio, sr = wave_to_p(tmp_wav.name)
                all_audio.append(audio)
                all_audio.append(pause_samples)
        i += 2
    if not all_audio:
        return
    full_wave = p.concatenate(all_audio, axis=0)
    max_val = p.max(p.abs(full_wave))
    if max_val > 0:
        full_wave = full_wave / max_val
    sd.play(full_wave, samplerate=sample_rate)
    sd.wait()
