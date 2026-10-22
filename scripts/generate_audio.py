from __future__ import annotations

import math
import struct
import wave
from pathlib import Path


SAMPLE_RATE = 44_100
OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "audio"


def envelope(index: int, length: int, attack: float = 0.04, release: float = 0.25) -> float:
    position = index / max(length - 1, 1)
    attack_gain = min(1.0, position / attack) if attack else 1.0
    release_gain = min(1.0, (1.0 - position) / release) if release else 1.0
    return max(0.0, min(attack_gain, release_gain))


def write_tone(name: str, duration: float, frequencies: list[float], volume: float = 0.22) -> None:
    total = int(SAMPLE_RATE * duration)
    frames = bytearray()
    for index in range(total):
        time = index / SAMPLE_RATE
        sample = sum(math.sin(2 * math.pi * frequency * time) for frequency in frequencies) / len(frequencies)
        sample *= envelope(index, total) * volume
        frames.extend(struct.pack("<h", int(sample * 32767)))

    path = OUTPUT / name
    with wave.open(str(path), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(SAMPLE_RATE)
        audio.writeframes(frames)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    write_tone("click.wav", 0.08, [880], 0.14)
    write_tone("signal.wav", 0.48, [330, 495], 0.16)
    write_tone("success.wav", 0.7, [523.25, 659.25, 783.99], 0.18)
    write_tone("error.wav", 0.35, [185, 174], 0.17)
    print(f"Audio generado en {OUTPUT}")


if __name__ == "__main__":
    main()

