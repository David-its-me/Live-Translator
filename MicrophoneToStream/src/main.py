import io
import os
import threading
import time

import speech_recognition as sr # pip install SpeechRecognition
# import pyttsx3
from langdetect import detect
from deepl import Translator  # pip install --upgrade deepl
from speech_recognition import AudioData
from gtts import gTTS # pip install gTTS
from io import BytesIO
from pygame import mixer
import queue

auth_key = 'b2b22326-eca3-05b6-50d1-ad80fe8f3ada:fx'

global counter
counter: int = 0

class MusicPlayer():

    def __init__(self):
        self.queue = queue.Queue()

    def append(self, path: str):
        self.queue.put(path)

    def handle_queue(self):

        while True:
            try:
                path = self.queue.get()
                mixer.music.load(path)
                mixer.music.play()
                while mixer.music.get_busy():
                    time.sleep(0.2)
            except Exception as e:
                print(e)

    def run(self):
        thread = threading.Thread(target=self.handle_queue, daemon=True)
        thread.start()

def speech_to_text(recognizer, audio):
    return recognizer.recognize_google(audio, language='de')

def translate(text) -> str:
    # recognize speech using Google Speech Recognition
    input_language = detect(text)
    ########################
    input_language = 'de'
    ########################
    print(input_language)
    print(text)
    # translate speech to English if detected language is German
    if input_language == "de":
        translation = translator.translate_text(text, target_lang='EN-US')
        print(f"Translated to English: {translation.text}")
        # speak the translated text
        return translation.text
    elif input_language == "en":
        translation = translator.translate_text(text, target_lang='DE')
        print(f"Translated to German: {translation.text}")
        # speak the translated text
        return translation.text
    else:
        print("Unsupported Language")



def text_to_speech(text, language: str="en"):
    global counter
    counter += 1
    audio = gTTS(text, lang=language, slow=False)
    audio.save(f'../audio_buffer/{counter}.mp3')
    global musicPlayer
    musicPlayer.append(f'../audio_buffer/{counter}.mp3')


def handle_audio_input(recognizer, audio):
    global counter
    try:
        text = speech_to_text(recognizer, audio)
        text = translate(text)
        text_to_speech(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service {e}")
    except Exception as e:
        print(e)



# Speech Recognizer
speech_recognizer: sr.Recognizer = sr.Recognizer()
microphone: sr.Microphone = sr.Microphone()

# Deepl Translator
translator = Translator(auth_key=auth_key)

# initialize mixer instance
mixer.init()

# Initialize player
global musicPlayer
musicPlayer = MusicPlayer()
musicPlayer.run()

# use the default microphone as the audio source
with microphone as source:
    print("Speak something...")
    # adjust the ambient noise level
    speech_recognizer.adjust_for_ambient_noise(source)

# listen for audio input from the user
speech_recognizer.pause_threshold = 0.3
speech_recognizer.non_speaking_duration = 0.1
print(f'Pause threshold: {speech_recognizer.pause_threshold}')
print(f'Non speaking duration: {speech_recognizer.non_speaking_duration}')
stop_listening = speech_recognizer.listen_in_background(microphone, handle_audio_input)
# `stop_listening` is now a function that, when called, stops background listening



# calling this function requests that the background listener stop listening
input("Press any Key to quit")
stop_listening(wait_for_stop=False)

#while True:

 #       audio: AudioData = speech_recognizer.listen(source)
 #       handle_audio_input(speech_recognizer, audio, counter)
  #      counter += 1

