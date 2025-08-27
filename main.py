import speech_recognition as sr
import webbrowser
import musicLibrary
import google.generativeai as genai
from gtts import gTTS
import pygame
import os

is_speaking = False

genai.configure(api_key="####")

recognizer = sr.Recognizer()


def speak(text):
    global is_speaking
    is_speaking = True
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    is_speaking = False


def aiProcess(command):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"You are a virtual assistant named Jarvis. Keep responses short.\nUser: {command}"
    response = model.generate_content(prompt)
    return response.text


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        song = song.lower()
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak(f"Sorry, I don't know the song {song}")
    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Cypher....")
    while True:
        try:
            if not is_speaking:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening for wake word...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                try:
                    word = recognizer.recognize_google(audio)
                    print(f"Heard: {word}")
                except sr.UnknownValueError:
                    continue
                if word.lower() == "cypher":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Cypher Active... Listening for command...")
                        audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
                    try:
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")
                        processCommand(command)
                    except sr.UnknownValueError:
                        speak("Sorry, I didn’t catch that.")
        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            print(f"Error: {e}")
            continue
