#Packages 
import speech_recognition as sr 
import pyttsx3 
import pygetwindow as gw 
import os 
import datetime 
import time 
import subprocess # to run specific application 
import sys # to stop the application 
import pywhatkit # to perform certain task on application  
import pyautogui  
import random  
recognizer = sr.Recognizer()
import requests 

def ask_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",  # free models available
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        return reply
    else: 
        return "Error connecting to AI" 
def speak(text): 
    import pyttsx3 
    print("Jarvis:", text)

    engine = pyttsx3.init('sapi5')   # force windows driver
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop() 
#Snippet - 3 
def open_software(software_name):
    if 'chrome' in software_name:
        program = r"C:\Users\Srihari\AppData\Local\Google\Chrome\Application\chrome.exe"
        subprocess.Popen("start chrome", shell=True)
    elif 'chatgpt' in software_name:
        program = r"C:\Users\Srihari\Downloads\ChatGPT Installer.exe"
        subprocess.Popen([program])
    elif 'vscode' in software_name or 'visual studio' in software_name: 
        program = r"C:\Users\Srihari\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        subprocess.Popen([program])
    elif 'notepad' in software_name:
        subprocess.Popen(['notepad.exe']) 
    elif 'calculator' in software_name:
        subprocess.Popen(['calc.exe']) 
    else:
        speak(f"I couldn't find the software {software_name}") 

#Snippet 4
def close_software(software_name):
    if 'chrome' in software_name:
        os.system("taskkill /f /im chrome.exe") 
    elif 'chatgpt' in software_name:
        os.system("taskkill /f /im ChatGPT Installer.exe")
    elif 'notepad' in software_name:
        os.system("taskkill /f /im notepad.exe") 
    elif 'calculator' in software_name:
        os.system("taskkill /f /im calc.exe") 
    else:
        speak(f"I couldn't find any open software named {software_name}")     
#Snippet 2   
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for wake word") 
        while True: 
            recognizer.adjust_for_ambient_noise(source,duration=0.5) # removing noise 
            recorded_audio = recognizer.listen(source)#listening user speech  
            try:
                                 #google API speech to text                                        
                text = recognizer.recognize_google(recorded_audio,language= 'en_us')
                text = text.lower() 
                if 'jarvis' in text:
                    print("Wake word detected!") 
                    speak('Hi bro, How can I help you?') 
                    return True 
            except Exception as ex: 
                print("Could not understand audio, please try again") 
#if its correct 
def cmd():
    global last_song 
    # 🎤 Step 1: Listen
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    # ❌ Step 2: mic closed here

    # 🧠 Step 3: convert speech → text
    try:
        text = recognizer.recognize_google(audio, language='en_us')
        text = text.lower()
        print("You said:", text)
    except:
        speak("Sorry, I didn't catch that")
        return

    # 🚀 Step 4: Execute commands

    if 'stop' in text:
        speak('Stopping the program. Goodbye!')
        sys.exit()

    elif 'open' in text:
        software_name = text.replace('open', '').strip()
        speak(f"Opening {software_name}")
        open_software(software_name)

    elif 'close' in text:
        software_name = text.replace('close', '').strip()
        speak(f"Closing {software_name}")
        close_software(software_name)

    elif 'time' in text: 
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(current_time) 
        
    elif 'search' in text:
        query = text.replace('search', '').strip()
        speak(f"Searching for {query}") 
        pywhatkit.search(query)
    elif 'play' in text:
        song = text.replace('play','').strip() 
        last_song = song 
        speak(f"playing {song}") 
        pywhatkit.playonyt(song) 
    elif 'pause' in text:
        speak("Pausing Video")
        pyautogui.press('space') 
    elif 'resume' in text or 'play video' in text:
        speak("Playing video") 
        pyautogui.press('space') 
        if last_song != "":
            pywhatkit.playonyt(last_song + " next")
        else:
            pywhatkit.playonyt("latest songs")
    elif 'what is your name' in text:
        speak("My name is Jarvis your AI")
    else:
        speak("Thinking...")
        answer = ask_ai(text)
        print("AI:", answer)
        speak(answer[:10000])
        
while True:
    if listen_for_wake_word():
        while True:
            cmd()