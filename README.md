# Local Voice Pet

A learning project: a voice companion that listens through a Mac's
microphone, generates a reply locally, and speaks it aloud.

Built and tested on an Apple Silicon M3 Mac with 18 GB RAM
and Python 3.12.

## How it works

Microphone → Parakeet v2 → Ollama → Kokoro → speakers

- **Speech recognition:** Parakeet-TDT-0.6B v2 through parakeet-mlx
- **Conversation:** llama3.2:3b through Ollama
- **Speech generation:** Kokoro
- **Recording:** sounddevice
- **Playback:** macOS afplay

Model files download during initial setup or first use.
Audio processing and model inference run locally.
Model-loading libraries may contact hosting services to check files.

## Setup

Install Python 3.12, Homebrew, and Ollama first.

From the project folder:

```bash
brew install ffmpeg
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
ollama pull llama3.2:3b
```

Keep Ollama running, then start the pet:

```bash
python pet.py
```

Allow microphone access when macOS requests it.
The first startup can take longer while speech models download.

`requirements.txt` captures the development environment. A fresh installation has not yet
been independently verified.

## Controls

With Terminal focused:

- Press backslash (`\`) to start recording.
- Press backslash again to stop and send your turn.
- Press `q` at the recording prompt to quit.
- Pressing `q` during recording discards that turn and quits.

Wait for the pet to finish speaking before starting another turn.
Interrupting a spoken reply is not implemented.

## Project files

- `pet.py`: conversation loop and spoken replies
- `recorder.py`: keyboard-controlled microphone recording
- `examples/`: standalone experiments used during development

Run examples from the project root, for example:

```bash
python examples/record_mic.py
```

Files named `test_` during development were manual experiments,
not automated tests.

## Current limitations

- macOS with Apple Silicon is the supported setup.
- English speech only.
- Conversation history lasts only until the program exits.
- Replies can be inaccurate or invent details.
- No wake word, visual pet, or API backend switching yet.
- Audio is temporarily saved as `mic_test.wav` and `reply.wav`.
  These files remain on disk and are overwritten by later turns.
  Git ignores WAV files.
- Whisper transcription was unusually slow in this setup;
  Parakeet is used by the main application.

## Next steps

- Add an OpenAI-compatible conversation backend.
- Develop the pet's personality.
- Improve error handling and timing visibility.
- Refine dependency management.

## Model credits

- NVIDIA Parakeet-TDT-0.6B v2 — CC-BY-4.0:
  https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2
- Parakeet MLX implementation:
  https://github.com/senstella/parakeet-mlx
- Kokoro-82M:
  https://huggingface.co/hexgrad/Kokoro-82M
- Llama 3.2 through Ollama:
  https://ollama.com/library/llama3.2

Models and dependencies retain their respective licenses.
