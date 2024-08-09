import streamlit as st
import speech_recognition as sr
import pyttsx3

# st.sidebar.title("walle")
# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to handle commands
def handle_command(command):
    if "add to cart" in command.lower():
        response = "Item added to cart"
    else:
        response = "Sorry, I didn't understand that command."
    return response

# Streamlit UI
st.title("Voice Assistant for Walmart Sparkathon")

st.write("Press the button and give a command like 'add to cart'...")

if st.button("Start Recording"):
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write("You said: " + text)
            
            # Handle command and generate response
            response = handle_command(text)
            st.write("Assistant: " + response)
            
            # Convert text to speech and play
            engine.say(response)
            engine.runAndWait()
        
        except sr.UnknownValueError:
            st.write("Could not understand the audio")
            engine.say("Could not understand the audio")
            engine.runAndWait()
        except sr.RequestError:
            st.write("Could not request results from the speech recognition service")
            engine.say("Could not request results from the speech recognition service")
            engine.runAndWait()
