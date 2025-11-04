import speech_recognition as sr
import webbrowser
import pyttsx3
import pywhatkit
import requests
import time
import multiprocessing
import datetime
import json
from openai import OpenAI



# ---------------------------------------------
# --- Demo Contacts.....Plzz Do Not Call ---
# ---------------------------------------------
contacts = {
    "satya": "+919830751267",
    "mom": "+919830751252",
    "dad": "+919812345678"
}
# ---------------------------------------------

def speak(text):
    print("Jarvis:", text)
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 175)
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.2)
    except Exception as e:
        print("Speech error:", e)


def aiProcess(command):
  client = OpenAI(
  )

  completion = client.chat.completions.create(
  model = "gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "you are a virtual assistance named Jarvis skilled in general tasks like amazon and google cloud"},
    {"role": "user", "content": command}
  ]
  )
  return completion.choices[0].message.content

def send_whatsapp_message(contact_number, message):
    try:
        speak(f"Sending your message to {contact_number}")
        pywhatkit.sendwhatmsg_instantly(contact_number, message, wait_time=15, tab_close=True)
        speak("Message sent successfully.")
    except Exception as e:
        print("WhatsApp Error:", e)
        speak("Sorry, I couldn't send the WhatsApp message right now.")

def processCommand(c):
    c = c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://www.google.com/")

    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com/")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com/")

    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com/feed/")

    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        if song:
            speak(f"Playing {song} on YouTube")
            try:
                pywhatkit.playonyt(song)
            except Exception as e:
                print("Error:", e)
                speak("Sorry, I couldn't play that song right now.")
        else:
            speak("Please tell me which song to play.")

    elif "news" in c:
        speak("Fetching top headlines...")
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                if articles:
                    for article in articles[:5]:
                        speak(article['title'])
                else:
                    speak("Sorry, I couldn't find any news right now.")
            else:
                speak("Sorry, I failed to fetch the news.")
        except Exception as e:
            print("News error:", e)
            speak("There was a problem getting the news.")

    elif "message" in c and "whatsapp" in c:
        try:
            recognizer = sr.Recognizer()

            # Step 1: Ask for contact
            speak("Who should I message?")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                contact_name = recognizer.recognize_google(audio).lower()

            if contact_name not in contacts:
                speak(f"I don't have a WhatsApp contact saved for {contact_name}.")
                return

            # Step 2: Ask for message
            speak(f"What message should I send to {contact_name}?")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=7)
                message = recognizer.recognize_google(audio)

            # Step 3: Send message
            send_whatsapp_message(contacts[contact_name], message)

        except Exception as e:
            print("Error in WhatsApp message:", e)
            speak("Something went wrong while sending the message.")

    else:
        output = aiProcess(c)
        speak(output)
        # speak("Sorry, I didn't understand that command.")

def listen_for_wake_word(recognizer):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening for wake word 'Jarvis'...")
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=3)
            word = recognizer.recognize_google(audio)
            print("Heard:", word)
            return word.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print("Error:", e)
            return ""

def listen_for_command(recognizer):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        speak("Yes")
        print("Jarvis Active. Listening for your command...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)
            command = recognizer.recognize_google(audio)
            print("Command:", command)
            return command
        except sr.WaitTimeoutError:
            speak("I didn't hear any command.")
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except Exception as e:
            print("Error:", e)
            return ""

def main_loop():
    recognizer = sr.Recognizer()
    speak("Initializing Jarvis in background... Ready for your command.")
    while True:
        try:
            wake_word = listen_for_wake_word(recognizer)
            if wake_word == "jarvis":
                command = listen_for_command(recognizer)
                if command:
                    processCommand(command)
            time.sleep(0.3)
        except Exception as e:
            print("Main loop error:", e)
            time.sleep(1)

if __name__ == "__main__":
    jarvis_process = multiprocessing.Process(target=main_loop)
    jarvis_process.daemon = True
    jarvis_process.start()

    print("Jarvis is running in background. You can minimize this window.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        speak("Goodbye!")
        jarvis_process.terminate()
