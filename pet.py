from ollama import chat
from kokoro import KPipeline
from parakeet_mlx import from_pretrained
from recorder import record_audio
import sounddevice as sd
import soundfile as sf
import subprocess

print("Loading speech models...", flush=True)
pipeline = KPipeline(lang_code="a")
stt_model = from_pretrained("mlx-community/parakeet-tdt-0.6b-v2")

#def record_audio():
#    device = sd.query_devices(kind="input")
#    sample_rate = int(device["default_samplerate"])
#
#    print("Recording for five seconds. Speak now!", flush=True)
#    audio = sd.rec(
#        frames=5 * sample_rate,
#        samplerate=sample_rate,
#        channels=1,
#    )
#    sd.wait()
#
#   sf.write("mic_test.wav", audio, sample_rate)

def speak(text):
    for words, phonemes, audio in pipeline(text, voice="af_heart"):
        sf.write("reply.wav", audio, 24000)
        subprocess.run(["afplay", "reply.wav"], check=True)


messages = [
    {
        "role": "system",
        "content": "Reply conversationally in one or two short sentences.",
    }
]

print("Ready!", flush=True)

while True:
    
    audio_file = record_audio()
    if audio_file is None:
        break

    print("Transcribing...", flush=True)
    result = stt_model.transcribe(audio_file)
    user_text = result.text.strip()
    print("You said:", user_text)

    if not user_text:
        print("No words recognized.")
        continue

    messages.append({"role": "user", "content": user_text})

    print("Thinking...", flush=True)
    response = chat(
        model="llama3.2:3b",
        messages=messages,
        stream=False,
    )

    reply = response.message.content
    print("Pet:", reply)
    messages.append({"role": "assistant", "content": reply})

    speak(reply)
