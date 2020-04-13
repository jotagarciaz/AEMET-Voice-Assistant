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
import json


assistant_name = ""
user_name = ""

def init():
    fname = "initial_config.json"
    fname_old = "actual_config.json"
    global assistant_name
    global user_name

    if os.path.isfile(fname): 
        obj = []
        data = []
        with open(fname, 'r') as myfile:
            data = myfile.read()
            obj = json.loads(data)
            assistant_name = str(obj['assistant_name'])
            user_name = str(obj['user_name'])

        
        if os.path.isfile(fname_old):
            with open(fname_old, 'r') as myfile_old:
                data_old = myfile_old.read()
                obj_old = json.loads(data_old)
                myfile_old.close()

            if obj != obj_old:
                 with open(fname_old,'w') as json_file:
                    print("Se han encontrado cambios de configuración")
                    json.dump(obj,json_file)
                    recording_defaults()
                    json_file.close()
    
        else:
            with open(fname_old,'w') as json_file:
                print("No había configuración anterior.")
                json.dump(obj,json_file)
                recording_defaults()
                json_file.close()


def recording_defaults():
    print("Grabando las frases más utilizadas.")
    speak(f"Mi nombe es {assistant_name}. ", name_file="nombre")
    speak(f"Perdona {user_name}, no te he entendido.", name_file="perdona")
    speak(f"Hola {user_name} ¿Qué tal?", name_file="saludo")

def speak(text,name_file="aux"):
    tts = gTTS(text=text,lang='es')
    tts.save(f"{name_file}.mp3")

def get_audio():
    print(f"{assistant_name} escuchando...")
    r = sr.Recognizer()
    said = ""
    with sr.Microphone() as source:
        audio = r.listen(source)
        print("analizando...")
        try:
            said = r.recognize_google(audio,language='es')
        except Exception as e:
            print("Exception: ", str(e))
            playsound.playsound("perdona.mp3")
    
    fname = "aux.mp3"
    if os.path.isfile(fname): 
        os.remove(fname)
    
    print(said)
    return said.lower()

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


init()
text = get_audio()

"""while True:
    text = get_audio()
    if assistant_name.lower() == text:
        print("¿Cómo te puedo ayudar?")
        text = get_audio()
        if "hola" in text:
            playsound.playsound("saludo.mp3")

        elif "cuál es tu nombre" in text:
            playsound.playsound("nombre.mp3")

        elif re.search("^.*(apunta|nota|escribe).*",text):
            speak(f"{user_name}, ¿Qué quieres que escriba?")
            note = get_audio().lower()
            code(note)
            speak("He creado la nota.")
        
        elif re.search(".*(temperatura|tiempo).*",text):
            temperatura = get_top_temperature()
            speak(temperatura)"""



print("¿Cómo te puedo ayudar?")
text = get_audio()
if "hola" in text:
    playsound.playsound("saludo.mp3")

elif "cuál es tu nombre" in text:
    playsound.playsound("nombre.mp3")

elif re.search("^.*(apunta|nota|escribe).*",text):
    speak(f"{user_name}, ¿Qué quieres que escriba?")
    note = get_audio().lower()
    code(note)
    speak("He creado la nota.")

elif re.search(".*(temperatura|tiempo).*",text):
    temperatura = get_top_temperature()
    speak(temperatura)