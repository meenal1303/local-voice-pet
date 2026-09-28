from time import perf_counter
from parakeet_mlx import from_pretrained

print("Loading Parakeet v2...", flush=True)
start = perf_counter()

model = from_pretrained("mlx-community/parakeet-tdt-0.6b-v2")

print(f"Model loading took {perf_counter() - start:.1f}s", flush=True)

for attempt in range(1, 3):
    print(f"Starting transcription {attempt}...", flush=True)
    start = perf_counter()

    result = model.transcribe("mic_test.wav")

    print(f"Transcription took {perf_counter() - start:.1f}s", flush=True)
    print("You said:", result.text, flush=True)
