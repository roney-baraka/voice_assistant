import speech_recognition as sr
import pyttsx3
import spacy
import datetime
import webbrowser
import wikipedia
from weather_helper import get_weather 
from email_helper import send_email
import config
import openai

openai.api_key = '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'

recognizer = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init()

def set_default_voice(engine):

    engine.setProperty('voice', None)  
    engine.setProperty('rate', 180)  

set_default_voice(engine)

# Define a user agent for Wikipedia API
import wikipediaapi
user_agent = 'voice_assistant/1.0 (barakaroney001@gmail.com)'
wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
page = wiki.page('Python (programming language)')
print(page.summary[:100])

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
        log_correction("Sorry, I did not understand")
        return None
    
def get_factual_answer(query):
    try:
        query = query.replace("who is", "").replace("what is", "").strip()
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Can you be more specific? Did you mean {e.options[:5]}?"
    except wikipedia.exceptions.PageError:
        return "I couldn't find anything related to that."
    
def get_llm_response(prompt):
    try:
        response = openai.Completion.create(
            engine = "GPT-4",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

def log_correction(command):
    with open("corrections.txt", "a") as file:
        file.write(f"Unrecognized command: {command}\n")

def learn_from_mistakes(user_query, assistant_response):
    prompt = f"The assistant responded to the following query incorrectly:\n\nUser query: {user_query}\nAssistant response: {assistant_response}\n\nHow could the assistant improve this response?"
    correction = get_llm_response(prompt)
    with open("corrections.txt", "a") as f:
        f.write(f"User query: {user_query}\nAssistant response: {assistant_response}\nCorrection: {correction}\n\n")

    return correction

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
        if recipient:
            speak("What is the subject?")
            subject = listen_command()
            if subject:
                speak("What is the message?")
                message = listen_command()
                if message:
                    try:
                        send_email(recipient, subject, message)
                        speak("Email has been sent.")
                    except Exception as e:
                        speak(f"Failed to send email: {str(e)}")
                else:
                    log_correction(command)
            else:
                log_correction(command)
        else:
            log_correction(command)
    elif "search" in command:
        speak("What would you like to search for?")
        query = listen_command()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query}")
    elif "wikipedia" in command:
        speak("What topic do you want to know about?")
        topic = listen_command()
        if topic:
            try:
                summary = wiki.page(topic).summary
                speak(summary)
            except Exception as e:
                speak("I couldn't fetch information from Wikipedia.")
                log_correction(command)
    else:
        speak("I cannot perform that task right now.")
        log_correction(command)

# Main loop for voice assistant
if __name__ == "__main__":
    assistant_name = "A DATA"
    speak(f"Hello, I am {assistant_name}. What's your name?")
    
    user_name = listen_command()  # Store the user's name
    speak(f"Nice to meet you, {user_name}!")

    while True:
        command = listen_command()

        if command:
            process_command(command)
        else:
            speak("I couldn't hear you clearly, please try again.")

        if command and "exit" in command:
            speak("Goodbye!")
            break

