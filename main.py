import os
import random
from datetime import datetime

import pyttsx3 as p
import requests  # send http req
import speech_recognition as sr
import wikipedia
from bs4 import BeautifulSoup  # handel html feature to found it (req)
from googletrans import Translator
from playsound import playsound
from selenium import webdriver  # open browser
from selenium.webdriver.chrome.options import Options  # not to close browser
from selenium.webdriver.common.by import By  # select element

from Speaker_Identification import *

engine = p.init()
engine.setProperty('rate', 180)  # speed
voices = engine.getProperty('voices')  # get list of available gender
r = sr.Recognizer()
r.energy_threshold = 10000
translator = Translator()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 1)
            print("listening")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print("user input:", text)
                return text.lower()
            except:
                print("error")
                speak("I didn't hear you. please tell me again")


def save_my_voice(name):
    speak("Speak for 3 seconds")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, 1)
        audio = r.listen(source)
    file_name = F"user_{name}.wav"
    with open(file_name, "wb") as file:
        file.write(audio.get_wav_data())
    vi_response = add_known_voice(file_name, name)
    os.remove(file_name)
    speak(vi_response)


def know_who_am_i():
    speak("Speak for 3 seconds")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, 1)
        audio = r.listen(source)
    file_name = F"user_{random.randint(0, 100_000)}.wav"
    with open(file_name, "wb") as file:
        file.write(audio.get_wav_data())
    vi_response = get_unknown_voice(file_name)
    os.remove(file_name)
    speak("you are " + vi_response)


def query_wiki(q):
    return wikipedia.summary(q, sentences=3,auto_suggest=True)


def query_youtube(text):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=" + text)
    video = driver.find_element(By.XPATH, '//*[@id="video-title"]').get_attribute("href")
    driver.get(video)


def send_whatsapp(text, phone_number):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(F"https://wa.me/{phone_number}?text={text}")


def get_current_date_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now


def trans(text, src="auto", dest="en"):
    translated_text = translator.translate(text, src=src, dest=dest)
    print(translated_text.text)
    return translated_text.text


def next_prayer():
    html_response = requests.get('https://www.google.com/search?q=prayer+times&hl=en', headers=headers)
    soup = BeautifulSoup(html_response.content, 'html.parser')
    next_prayer_time = soup.find('div', attrs={"class": "Uaexyd"}).text
    return next_prayer_time


def get_current_temperature():
    html_response = requests.get('https://www.google.com/search?q=temperature&hl=en', headers=headers)
    soup = BeautifulSoup(html_response.content, 'html.parser')
    temperature = soup.find('div', attrs={"class": "vk_bk TylWce SGNhVe"})
    temperature = temperature.find('span', attrs={"style": "display:inline"}).text
    unit = soup.find('div', attrs={"class": "vk_bk wob-unit"})
    unit = unit.find('span', attrs={"style": "display:inline"}).text
    return F"temperature now is {temperature}{unit}"


def get_latest_news():
    html_response = requests.get('https://www.google.com/search?q=news&hl=en', headers=headers)
    soup = BeautifulSoup(html_response.content, 'html.parser')
    news = soup.find_all('div', attrs={"class": "mCBkyc tNxQIb ynAwRc nDgy9d"})
    news = [i.text.replace("...", "").strip() for i in news]
    return news


speak("Hello sir, i'm your voice assistant. How are you? Do you want to continue with a male or female voice assistant")
response = listen()
while True:
    if "female" in response:
        engine.setProperty('voice', voices[1].id)
        break
    elif "male" in response:
        engine.setProperty('voice', voices[0].id)
        break
    else:
        speak(
            "Who you want to you continue with you? a male or a female voice assistant?")
        response = listen()

speak("Hello sir, thank you for choosing me. what can i do for you ?")
response = listen()
while True:
    if "information" in response:
        speak("okay sir but which topic?")
        response = listen()
        result = query_wiki(response)
        speak(result)

    elif "youtube" in response:
        speak("Okay sir but which video?")
        response = listen()
        query_youtube(response)

    elif "time" in response or "date" in response:
        speak(get_current_date_time())

    elif "translate" in response:
        # speak("from which language?")
        # source = listen()
        # speak("to which language?")
        # destination = listen()
        speak("What you want me translate for you ?")
        words = listen()
        speak(trans(words, ))

    elif "prayer" in response:
        speak(next_prayer())

    elif "temperature" in response:
        speak(get_current_temperature())

    elif "news" in response:
        for news in get_latest_news():
            speak(news)

    elif "send" in response or "whatsapp" in response:
        speak("Please Enter the phone number with the Country code?")
        phone_number = input("Phone Number: ")
        speak("Please say the message?")
        message = listen()
        print(message, phone_number)
        speak("I am sending the message now")
        send_whatsapp(message, phone_number)

    elif "sport" in response:
        playsound(r"audio.wav")

    elif "save" in response:
        speak("What's your name")
        name = listen()
        save_my_voice(name)
    elif "who" in response:
        know_who_am_i()

    speak("anything else ?")
    response = listen()
    if "no" in response:
        speak("Welcome, I am waiting for you again")
        break
