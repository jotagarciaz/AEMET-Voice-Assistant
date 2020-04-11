import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
from urllib import request
import nltk


def speak(text):
    tts = gTTS(text=text,lang='es')
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio,language='es')
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
            speak("Perdona no te he entendido")
    
    return said

def get_top_temperature():
    url = "http://www.aemet.es/es/eltiempo/prediccion/municipios/santander-id39075"
    response = request.urlopen(url)
    raw = response.read().decode(encoding='cp1252')

    tokens = nltk.word_tokenize(raw)

    aux = raw[raw.find("Temperatura mínima y máxima "):]
    aux = aux[aux.find("texto_rojo\">"):]
    aux = aux[11:-1]
    aux = aux[:aux.find("&nbsp;")]
    aux = aux[1:]

    return "La temperatura máxima para Santander hoy es de "+aux+" grados centigrados."


text = get_audio()

if "hola" in text:
    speak("hola Quini, ¿Qué tal?")

elif "cuál es tu nombre" in text:
    speak("Mi nombre es Rigoberta")

elif "temperatura" or "tiempo" in text:
    speak(get_top_temperature())