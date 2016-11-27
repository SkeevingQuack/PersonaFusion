import json
import pickle

from persona import Persona
import persona

with open('Personas.pickle', mode='rb') as picklefile:
    personas = pickle.load(picklefile)
with open('personas.json', mode='w', encoding='utf-8') as jsonfile:
    json.dump(personas, jsonfile, ensure_ascii=False,
        indent=4, cls=persona.JSONEncoder)
