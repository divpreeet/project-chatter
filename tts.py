from TTS.api import TTS
import sounddevice as sd
import numpy as p
import re

tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)
SPEAKER = "p230"
PAUSE = 0.15

def speak(text):
    sample_rate = tts.synthesizer.output_sample_rate
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
            raw = tts.tts(text=segment, speaker=SPEAKER)
            if isinstance(raw, tuple):
                wave = p.atleast_1d(raw[0])
            elif isinstance(raw, list):
                waves = [p.atleast_1d(r) for r in raw]
                wave = p.concatenate(waves, axis=0)
            else:
                wave = p.atleast_1d(raw)
            all_audio.append(wave)
            all_audio.append(pause_samples)
        i += 2
    if not all_audio:
        return
    full_wave = p.concatenate(all_audio, axis=0)
    sd.play(full_wave, samplerate=sample_rate)
    sd.wait()
