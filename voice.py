import sounddevice as sd
from scipy.io.wavfile import write
import pyttsx3
import tempfile
import os
import time
import sys
import numpy as np
from faster_whisper import WhisperModel

# -------- Whisper Setup --------
print("Loading Whisper model...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
print("Whisper ready.")


def speak(text):
    """Speak ORION's response."""
    print(f"ORION: {text}\n")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    for voice in voices:
        if "male" in voice.name.lower() or "david" in voice.name.lower() or "mark" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    del engine
    time.sleep(0.3)


def listen(sample_rate=16000, silence_threshold=500, silence_duration=2.0, max_duration=30):
    """
    Record until the user stops speaking.
    - Starts recording when you speak
    - Stops automatically after silence_duration seconds of silence
    - Max recording time is max_duration seconds (safety limit)
    """
    print("🎙️  Listening... (speak freely, stops when you stop talking)")

    # Reset audio device
    try:
        sd.stop()
        sd._terminate()
        sd._initialize()
        time.sleep(0.2)
    except:
        pass

    chunk_size = int(sample_rate * 0.1)  # 100ms chunks
    all_chunks = []
    silent_chunks = 0
    speaking_started = False
    max_chunks = int(max_duration / 0.1)
    silence_chunks_needed = int(silence_duration / 0.1)  # how many silent chunks = stop

    try:
        with sd.InputStream(samplerate=sample_rate, channels=1,
                            dtype='int16', blocksize=chunk_size) as stream:

            for _ in range(max_chunks):
                chunk, _ = stream.read(chunk_size)
                volume = np.abs(chunk).mean()

                if volume > silence_threshold:
                    # User is speaking
                    speaking_started = True
                    silent_chunks = 0
                    all_chunks.append(chunk.copy())
                else:
                    # Silence detected
                    if speaking_started:
                        all_chunks.append(chunk.copy())
                        silent_chunks += 1
                        if silent_chunks >= silence_chunks_needed:
                            # Enough silence after speech — stop recording
                            break
                    # If not started speaking yet, just wait

        if not all_chunks or not speaking_started:
            print("(No speech detected)")
            return ""

        print("⏹️  Got it. Processing...")

        audio_data = np.concatenate(all_chunks, axis=0)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name
            write(temp_path, sample_rate, audio_data)

        segments, _ = whisper_model.transcribe(temp_path, language="en")
        text = " ".join(segment.text for segment in segments).strip()
        os.remove(temp_path)

        if text:
            print(f"You said: {text}")
        else:
            print("(Could not understand speech)")

        return text

    except Exception as e:
        print(f"(Mic error: {e})")
        return ""