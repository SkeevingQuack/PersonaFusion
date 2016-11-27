from urllib import request
import pickle

from bs4 import BeautifulSoup

class Persona:
    wiki = "http://spwiki.net/persona5/wikis/{}.html"

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

        self.alt_names = '?'

        self.arcana = '?'
        self.arcana_number = '?'
        self.lvl = '?'

        self.stats = '?'
        self.resistances = '?'
        self.skills = '?'


    def __str__(self):
        return self.name

class Stats:
    def __init__(self, strength, magic, endurance, agility, luck):
        self.strength = strength
        self.magic = magic
        self.endurance = endurance
        self.agility = agility
        self.luck = luck

class Resistances:
    def __init__(self, physical, ranged, fire, ice, electric, wind, psy, nuclear, light, curse):
        self.physical = physical
        self.ranged = ranged
        self.fire = fire
        self.ice = ice
        self.electric = electric
        self.wind = wind
        self.psy = psy
        self.nuclear = nuclear
        self.light = light
        self.curse = curse

class PersonaSkill:
    def __init__(self, name, attribute, lvl):
        self.name = name
        self.attribute = attribute
        self.lvl = lvl
