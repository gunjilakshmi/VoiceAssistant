import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import datetime
import requests
import sounddevice as sd
from scipy.io import wavfile
import io

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)  # 1 for female voice, 0 for male voice

def speak(audio):
    """Makes the assistant speak the text passed to it."""
    engine.say(audio)
    engine.runAndWait()

def take_command():
    """Listens using sounddevice (No PyAudio required!) and converts to text."""
    r = sr.Recognizer()
    sample_rate = 16000  # Google Speech API standard rate
    duration = 4         # Records in 4-second intervals
    
    print("\nListening...")
    try:
        # Record audio directly via sounddevice (Bypasses PyAudio entirely!)
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until the 4 seconds are up
        print("Recognizing...")
        
        # Convert recording in memory to a format SpeechRecognition understands
        wav_io = io.BytesIO()
        wavfile.write(wav_io, sample_rate, audio_data)
        wav_io.seek(0)
        
        with sr.AudioFile(wav_io) as source:
            audio = r.record(source)
            
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        return "none"

if __name__ == '__main__':
    speak("Amigo assistance activated")
    speak("How can I help you today?")
    
    while True:
        query = take_command()
        
        if query == "none":
            continue

        # 1. Wikipedia Searching
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", '').strip()
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception:
                speak("I couldn't find any relevant results on Wikipedia.")
            
        # 2. Basic Identity
        elif 'are you' in query:
            speak("I am Amigo, your personal assistant, developed by Jaspreet Singh.")
            
        # 3. Dynamic Time & Date Commands
        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {str_time}")

        elif 'the date' in query or 'today\'s date' in query:
            str_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today is {str_date}")

        # 4. Live Weather Integration
        elif 'weather in' in query:
            city = query.split("weather in")[-1].strip()
            speak(f"Checking the weather for {city}")
            try:
                url = f"https://wttr.in/{city}?format=%C+and+%t"
                res = requests.get(url, timeout=5).text
                speak(f"The weather in {city} is currently {res}")
            except Exception:
                speak("I was unable to retrieve the weather report.")

        # 5. Fun Features
        elif 'joke' in query:
            try:
                joke = requests.get("https://official-joke-api.appspot.com/random_joke").json()
                speak(joke['setup'])
                speak(joke['punchline'])
            except Exception:
                speak("Why did the programmer quit his job? Because he didn't get arrays.")

        # 6. Web Browsing Commands
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")
        elif 'open github' in query:
            speak("Opening GitHub")
            webbrowser.open("https://github.com")
        elif 'open stackoverflow' in query:
            speak("Opening Stack Overflow")
            webbrowser.open("https://stackoverflow.com")
            
        # 7. Local App Launching (WhatsApp)
        elif 'open whatsapp' in query:
            speak("Opening WhatsApp")
            loc = os.path.expanduser("~") + "\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
            alt_loc = os.path.expanduser("~") + "\\AppData\\Local\\Microsoft\\WindowsApps\\WhatsApp.exe"
            
            if os.path.exists(loc):
                os.startfile(loc)
            elif os.path.exists(alt_loc):
                os.startfile(alt_loc)
            else:
                speak("Opening Web WhatsApp instead.")
                webbrowser.open("https://web.whatsapp.com")
                
        # 8. Local System Storage Navigation
        elif 'local disk d' in query:
            speak("Opening local disk D")
            os.startfile("D://")
        elif 'local disk c' in query:
            speak("Opening local disk C")
            os.startfile("C://")
            
        # 9. System Exit
        elif 'sleep' in query or 'exit' in query or 'goodbye' in query:
            speak("Goodbye!")
            exit(0)