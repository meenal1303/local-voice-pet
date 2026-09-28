import sounddevice as sd
import soundfile as sf
import subprocess

device = sd.query_devices(kind="input")
sample_rate = int(device["default_samplerate"])
duration = 5

print(f"Microphone: {device['name']}")
input("Press Enter, then speak for five seconds: ")

audio = sd.rec(
    frames=duration * sample_rate,
    samplerate=sample_rate,
    channels=1,
)
sd.wait()

sf.write("mic_test.wav", audio, sample_rate)
print("Recording finished. Playing it back...")
subprocess.run(["afplay", "mic_test.wav"], check=True)
