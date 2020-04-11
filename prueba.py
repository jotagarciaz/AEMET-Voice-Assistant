# python 3.6.0 

from urllib import request
import nltk



url = "http://www.aemet.es/es/eltiempo/prediccion/municipios/santander-id39075"
response = request.urlopen(url)
raw = response.read().decode(encoding='cp1252')

tokens = nltk.word_tokenize(raw)

aux = raw[raw.find("Temperatura mínima y máxima "):]
aux = aux[aux.find("texto_rojo\">"):]
aux = aux[11:-1]
aux = aux[:aux.find("&nbsp;")]


aux = aux[1:]

print("The top temperature for the current day:",str(aux))