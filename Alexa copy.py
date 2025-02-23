import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage
import threading
import datetime
import speech_recognition as sr
import pyttsx3
import pyjokes
import pywhatkit
import wikipedia
import sys
import logging
import requests
import pyaudio

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize recognizer
listener = sr.Recognizer()

# Talk function for TTS
def talk(text):
    engine.say(text)
    engine.runAndWait()

   
# Function to take user commands via microphone
def take_command():
    try:
        with sr.Microphone() as source:
            output_text.insert(tk.END, "Listening...\n")
            output_text.see(tk.END)
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
            return command
        
    except Exception as e:
        logging.error(f"Error in take_command: {e}")
        output_text.insert(tk.END, f"Error: {e}\n")
        output_text.see(tk.END)
        return ""

# Core assistant logic
def run_assistant():
    while True:
        command = take_command()
        output_text.insert(tk.END, f"User: {command}\n")
        output_text.see(tk.END)
        
        if 'stop' in command or 'exit' in command:
            talk("Goodbye!")
            sys.exit()

        elif 'play' in command:
            song = command.replace('play', '')
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)
        
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"Current time is {time}")
            output_text.insert(tk.END, f"Alexa: Current time is {time}\n")
        
        elif 'who the heck is' in command:
            person = command.replace('who the heck is', '')
            try:
                info = wikipedia.summary(person, sentences=1)
                talk(info)
                output_text.insert(tk.END, f"Alexa: {info}\n")
            except Exception as e:
                logging.error(f"Error fetching information from Wikipedia: {e}")
                talk(f"Sorry, I couldn't find information about {person}")
        
        elif 'date' in command:
            talk("Sorry, I have a headache")
        
        elif 'are you single' in command:
            talk("I am in a relationship with WiFi")
        
        elif 'joke' in command:
            joke = pyjokes.get_joke()
            talk(joke)
            output_text.insert(tk.END, f"Alexa: {joke}\n")

        elif 'hi' in command or 'hello' in command:
            talk("Hello there! How can I assist you today?")
            output_text.insert(tk.END, "Alexa: Hello there! How can I assist you today?\n")
        
        
# Start assistant in a thread
def start_assistant():
    assistant_thread = threading.Thread(target=run_assistant)
    assistant_thread.daemon = True
    assistant_thread.start()

# Stop program function
def stop_program():
    talk("Goodbye!")
    sys.exit()

# GUI setup using Tkinter
root = tk.Tk()
root.title("Alexa Assistant")
root.geometry("600x500")
root.configure(bg="#1a1a1a")  # Set background color to dark for a modern look

# Add Alexa logo
logo = PhotoImage(file=r"C:\Users\nakul\OneDrive\Desktop\project\alexa_logo.png")  # Replace with the path to your Alexa logo image
logo_label = tk.Label(root, image=logo, bg="#1a1a1a")
logo_label.pack(pady=10)

# Add a title label
title_label = tk.Label(root, text="Alexa Voice Assistant", font=("Helvetica", 16, "bold"), fg="#00FFFF", bg="#1a1a1a")
title_label.pack(pady=5)

# Start button
start_button = tk.Button(root, text="Start Alexa", command=start_assistant, bg="#00b894", fg="white", font=("Helvetica", 12, "bold"))
start_button.pack(pady=10)

# Stop button
stop_button = tk.Button(root, text="Stop Alexa", command=stop_program, bg="#d63031", fg="white", font=("Helvetica", 12, "bold"))
stop_button.pack(pady=10)

# Output box for interaction history
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Helvetica", 10), bg="#2c2c2c", fg="white")
output_text.pack(pady=10)

# Run Tkinter event loop
root.mainloop()
