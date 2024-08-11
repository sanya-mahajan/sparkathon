# tts_script.py
import pyttsx3
import sys

def speak_message(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else "Hello"
    speak_message(message)
