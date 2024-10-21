import speech_recognition as sr
import pyttsx3
import spacy
import datetime
import webbrowser
from weather_helper import get_weather 
from email_helper import send_email
import config 

recognizer = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand")
        return None

# Process command and use NLP
def process_command(command):
    doc = nlp(command)
    
    if "time" in command:
        current_time = datetime.datetime.now().strftime('%H:%M')
        speak(f"The time is {current_time}")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        speak(f"Today's date is {current_date}")
    elif "weather" in command:
        speak("Which city?")
        city = listen_command()
        if city:
            weather = get_weather(city)
            speak(weather)
    elif "email" in command:
        speak("Who do you want to send the email to?")
        recipient = listen_command()
        speak("What is the subject?")
        subject = listen_command()
        speak("What is the message?")
        message = listen_command()
        if recipient and subject and message:
            send_email(recipient, subject, message)
            speak("Email has been sent.")
    elif "search" in command:
        speak("What would you like to search for?")
        query = listen_command()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query}")
    else:
        speak("I cannot perform that task right now.")

# Main loop for voice assistant
if __name__ == "__main__":
    speak("Hello, I am your assistant. How can I help you today?")

    while True:
        command = listen_command()

        if command:
            process_command(command)
        else:
            speak("I couldn't hear you clearly, please try again.")

        if command and "exit" in command:
            speak("Goodbye!")
            break
