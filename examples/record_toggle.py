import sys
import termios
import tty
import numpy as np
import sounddevice as sd
import soundfile as sf

keyboard = sys.stdin.fileno()
original_settings = termios.tcgetattr(keyboard)

device = sd.query_devices(kind="input")
sample_rate = int(device["default_samplerate"])

chunks = []
stream = None


def collect_audio(indata, frames, time_info, status):
    chunks.append(indata.copy())


print("Press \\ to start/stop recording. Press q to quit.", flush=True)

try:
    tty.setcbreak(keyboard)

    while True:
        key = sys.stdin.read(1)

        if key == "q":
            break

        if key != "\\":
            continue

        if stream is None:
            chunks = []
            stream = sd.InputStream(
                samplerate=sample_rate,
                channels=1,
                callback=collect_audio,
            )
            stream.start()
            print("Recording started. Press \\ to stop.", flush=True)

        else:
            stream.stop()
            stream.close()
            stream = None

            if chunks:
                audio = np.concatenate(chunks, axis=0)
                sf.write("mic_test.wav", audio, sample_rate)
                print("Recording saved to mic_test.wav", flush=True)
            else:
                print("No audio captured.", flush=True)

finally:
    try:
        if stream is not None:
            stream.stop()
            stream.close()
    finally:
        termios.tcsetattr(
            keyboard, termios.TCSADRAIN, original_settings
        )
