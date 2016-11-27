import json

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

        self.itemization = '?'


    def __str__(self):
        return str( (self.name, self.slug) )


class Stats:
    def __init__(self):
        self.strength = '?'
        self.magic = '?'
        self.endurance = '?'
        self.agility = '?'
        self.luck = '?'

class Resistances:
    def __init__(self):
        self.physical = '?'
        self.ranged = '?'
        self.fire = '?'
        self.ice = '?'
        self.electric = '?'
        self.wind = '?'
        self.psy = '?'
        self.nuclear = '?'
        self.light = '?'
        self.curse = '?'

class PersonaSkill:
    def __init__(self):
        self.name = '?'
        self.attribute = '?'
        self.cost = '?'
        self.target = '?'
        self.lvl = '?'

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        result = o.__dict__
        if o.stats != '?':
            stats = result.pop('stats')
            result['stats'] = stats.__dict__
        if o.resistances != '?':
            resistances = result.pop('resistances')
            result['resistances'] = resistances.__dict__
        if o.skills != '?':
            skills = result.pop('skills')
            skills = map(lambda x:x.__dict__, skills)
            result['skills'] = list(skills)

        if o.arcana != '?':
            result['arcana_number'] = arcana_map(result['arcana'])

        return result

def arcana_map(arcana):
    map_dict = {'Fool':0, 'Magician':1, 'Priestess':2, 'Empress':3,
        'Emperor':4, 'Hierophant':5, 'Lovers':6, 'Chariot':7, 'Justice':8,
        'Hermit':9, 'Fortune':10, 'Strength':11, 'Hanged Man':12,
        'Death':13, 'Temperance':14, 'Devil':15, 'Tower':16, 'Star':17,
        'Moon':18, 'Sun':19, 'Judgement':20}
    return map_dict[arcana]
