import sounddevice as sd
print(sd.query_devices())
print("Default output:", sd.default.device)
