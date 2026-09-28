import sys
import termios
import tty
import numpy as np
import sounddevice as sd
import soundfile as sf


def record_audio():
    keyboard = sys.stdin.fileno()
    original_settings = termios.tcgetattr(keyboard)
    device = sd.query_devices(kind="input")
    sample_rate = int(device["default_samplerate"])
    chunks = []

    def collect_audio(indata, frames, time_info, status):
        chunks.append(indata.copy())

    print("Press \\ to record, or q to quit.", flush=True)

    try:
        tty.setcbreak(keyboard)

        while True:
            key = sys.stdin.read(1)
            if key == "q":
                return None
            if key == "\\":
                break

        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            callback=collect_audio,
        ):
            print("Recording... Press \\ to stop.", flush=True)

            while True:
                key = sys.stdin.read(1)
                if key == "q":
                    return None
                if key == "\\":
                    break

    finally:
        termios.tcsetattr(
            keyboard, termios.TCSADRAIN, original_settings
        )

    if not chunks:
        return None

    audio = np.concatenate(chunks, axis=0)
    filename = "mic_test.wav"
    sf.write(filename, audio, sample_rate)
    return filename
