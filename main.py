import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
from urllib import request
import nltk
import subprocess 
import datetime 
import re


def speak(text):
    tts = gTTS(text=text,lang='es')
    filename = "aux.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    print("escuchando...")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        print("analizando...")
        try:
            said = r.recognize_google(audio,language='es')
            print(said)
        except Exception as e:
            print("Exception: ", str(e))
            playsound.playsound("perdona.mp3")
    
    fname = "aux.mp3"
    if os.path.isfile(fname): 
        os.remove(fname)
    
    print(said)
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

def code(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    f.close()
    subprocess.Popen(["code",file_name])





text = get_audio().lower()

if "hola" in text:
    playsound.playsound("saludo.mp3")

elif "cuál es tu nombre" in text:
    playsound.playsound("nombre.mp3")

elif re.search("^.*(apunta|nota|escribe).*",text):
    speak("¿Qué quieres que escriba?")
    note = get_audio().lower()
    code(note)
    speak("He creado la nota. ")
    

elif re.search(".*(temperatura|tiempo).*",text):
    temperatura = get_top_temperature()
    speak(temperatura)