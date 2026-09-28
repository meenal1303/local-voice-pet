import sys
import termios
import tty

keyboard = sys.stdin.fileno()
original_settings = termios.tcgetattr(keyboard)
recording = False

print("Press \\ to toggle. Press q to quit.", flush=True)

try:
    tty.setcbreak(keyboard)

    while True:
        key = sys.stdin.read(1)

        if key == "q":
            break

        if key == "\\":
            recording = not recording

            if recording:
                print("Recording started", flush=True)
            else:
                print("Recording stopped", flush=True)

finally:
    termios.tcsetattr(keyboard, termios.TCSADRAIN, original_settings)
