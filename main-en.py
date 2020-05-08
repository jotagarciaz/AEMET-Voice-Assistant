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
    speak(f"My name is {assistant_name}. ", name_file="nombre")
    speak(f"Sorry {user_name}, I dind't understand it.", name_file="perdona")
    speak(f"Hello {user_name} How are you?", name_file="saludo")
    speak(f"Good bye.",name_file="fin")

def speak(text,name_file="aux"):
    tts = gTTS(text=text,lang='en')
    tts.save(f"{name_file}.mp3")
    if name_file == "aux":
        playsound.playsound("aux.mp3")

def get_audio():
    print(f"{assistant_name} hearing...")
    
    said = ""
    with sr.Microphone() as source:
        audio = r.listen(source)
        print("analysing...")
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

    return "The maximum temperature in Santander today will be "+aux+" degrees Celsius."

def code(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    f.close()
    subprocess.Popen(["code",file_name])

r = sr.Recognizer()
r.energy_threshold = 4000
r.dynamic_energy_threshold = True
init()

print(f"Say '{assistant_name}' to start.")
while True:
    text = get_audio()
    if assistant_name.lower() == text:
        print("How can I help you?")
        text = get_audio()
        if "hello" in text:
            playsound.playsound("saludo.mp3")

        elif "what is your name" in text:
            playsound.playsound("nombre.mp3")

        elif re.search("time",text):
            speak(f"it is {datetime.datetime.now().strftime('%H:%M:%S')}")

        elif re.match("^.*(text|note|write).*",text):
            speak(f"{user_name}, what do you want me to write?")
            note = get_audio().lower()
            code(note)
            speak("I've writen the note")

        elif re.match(".*(temperature|weather).*",text):
            temperatura = get_top_temperature()
            speak(temperatura)
        
        elif re.search("(thanks|end|that's all|thank you)",text):
            playsound.playsound("fin.mp3")
            break

