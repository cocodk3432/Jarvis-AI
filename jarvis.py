import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import datetime
import requests

engine = pyttsx3.init()

def speak_fun(audio):
    engine.say(audio)
    engine.runAndWait()

def take_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        result = recognizer.recognize_google(audio, language='en')
        print(f'User said: {result}')
        return result
    except Exception as e:
        print(e)
        return ""

def open_website(url):
    webbrowser.open(url)
    speak_fun(f"Opening {url}")

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak_fun(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak_fun("It seems there are multiple matching results. Can you please be more specific?")
    except wikipedia.exceptions.PageError as e:
        speak_fun("I couldn't find any relevant information on that topic.")

def check_weather():
    city = "New York"  # Change this to the desired city
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"] - 273.15  # Convert to Celsius
        speak_fun(f"The weather in {city} is {weather} and the temperature is {temperature:.1f} degrees Celsius.")
    else:
        speak_fun("I couldn't retrieve the weather information at the moment.")

def main():
    speak_fun("Hello! I am your voice assistant. How can I assist you today?")

    while True:
        user_input = take_speech().lower()

        if "what's the time" in user_input:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak_fun(f"The current time is {current_time}")

        elif "open YouTube" in user_input:
            open_website("https://www.youtube.com")

        elif "open Google" in user_input:
            open_website("https://www.google.com")

        elif "search on Wikipedia" in user_input:
            speak_fun("What would you like to search on Wikipedia?")
            search_query = take_speech()
            if search_query:
                search_wikipedia(search_query)
            else:
                speak_fun("I didn't catch that. Please repeat your search query.")

        elif "check the weather" in user_input:
            check_weather()

        elif "exit" in user_input:
            speak_fun("Goodbye!")
            break

        else:
            speak_fun("I didn't understand that. Please repeat your command.")

if __name__ == "__main__":
   while True:
       main()
