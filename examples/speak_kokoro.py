from kokoro import KPipeline
import soundfile as sf
import subprocess

pipeline = KPipeline(lang_code="a")
text = "Hello Meenal. I am your local voice companion."

for index, (words, phonemes, audio) in enumerate(
    pipeline(text, voice="af_heart")
):
    filename = f"voice_test_{index}.wav"
    sf.write(filename, audio, 24000)
    print(f"Playing: {filename}")
    subprocess.run(["afplay", filename], check=True)
