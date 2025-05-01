import speech_recognition as sr
import os
import webbrowser
import pyttsx3
import subprocess
import openai
import imageio

# Initialize OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)

    try:
        # Request to OpenAI GPT-3.5 Turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        )
        response_text = response.choices[0].message['content'].strip()

        chatStr += f"vinayak: {query}\n: {response_text}\n"

        say(response_text)

        return response_text

    except Exception as e:
        print(f"Error: {e}")
        return "I'm sorry."

def say(text):
    if os.name == 'nt':
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()

def take_snapshot():
    try:
        video_reader = imageio.get_reader("<video0>")
        frame = video_reader.get_next_data()
        save_path = "C:\\Users\\sinha\\OneDrive\\Desktop\\picc\\snapshot.jpg"
        imageio.imwrite(save_path, frame)
        print(f"Snapshot taken successfully and saved to {save_path}")
        say("Snapshot taken successfully")
    except Exception as e:
        print(f"Error: {e}")
        say("Unable to capture snapshot")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"you: {query}")
            return query
        except Exception as e:
            print(f"Error recognizing speech: {e}")
            return "Some Error Occurred. Sorry."

def open_chrome(search_query=None):
    if os.name == 'nt':
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if not os.path.exists(chrome_path):
            chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        if search_query:
            subprocess.Popen([chrome_path, f"https://www.google.com/search?q={search_query}"])
        else:
            subprocess.Popen([chrome_path])

def snap():
    if os.name == 'nt':
        application_path = "C:\\Users\\sinha\\OneDrive\\Desktop\\picc\\snapshot.jpg"
        os.startfile(application_path)

def close():
    if os.name == 'nt':
        os.system("taskkill /f /im MicrosoftPhotos.exe")

def close_chrome():
    if os.name == 'nt':
        os.system("taskkill /f /im chrome.exe")

if __name__ == '__main__':
    print('Welcome')
    say("Hello")
    while True:
        query = takeCommand()
        if "bye" in query.lower():
            say("Goodbye")
            break
        elif "hello" in query.lower():
            say("hello how are you")
        elif "how are you?" in query.lower():
            say("I am good, how are you?")
        elif "i am good" in query.lower():
            say("That's nice")
        elif "open google chrome" in query.lower():
            say("Opening Google Chrome")
            open_chrome()
        elif "close snap" in query.lower():
            say("Closing picture viewer")
            close()
        elif "close google chrome" in query.lower():
            say("Closing Google Chrome")
            close_chrome()
        elif "show snap" in query.lower():
            say("Showing you the snapshot")
            snap()
        elif "take a snap" in query.lower():
            say("Taking a snapshot")
            take_snapshot()
        elif "search" in query.lower():
            search_query = query.lower().replace("search", "").strip()
            say(f"Searching for {search_query}")
            open_chrome(search_query)
        else:
            response = chat(query)
            print(response)
