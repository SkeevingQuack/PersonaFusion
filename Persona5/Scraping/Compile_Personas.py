from urllib import request
from bs4 import BeautifulSoup
from sys import argv

import pickle

list_location = "personas.txt"

def log(msg):
    with open("errors.log", mode="a") as logfile:
        logfile.write(msg + '\n')

class Persona:
    def __init__(self, name, slug):
        self.name = name
        self.slug = slug

    def __str__(self):
        return self.name

    def init_basics(self, lv, arcana, strength, magic, endurance, agility, luck):
        self.lv = lv
        self.arcana = self.translate(arcana)
        self.strength = strength
        self.magic = magic
        self.endurance = endurance
        self.agility = agility
        self.luck = luck

    def init_types(self, phys, ranged, fire, ice, electric, wind, psy, nuclear, light, curse):
        self.phys = self.translate(phys)
        self.ranged = self.translate(ranged)
        self.fire = self.translate(fire)
        self.ice = self.translate(ice)
        self.electric = self.translate(electric)
        self.wind = self.translate(wind)
        self.psy = self.translate(psy)
        self.nuclear = self.translate(nuclear)
        self.light = self.translate(light)
        self.curse = self.translate(curse)

    def init_skills(self, *skills):
        """(name, lv)"""
        self.skills = []
        for skill in skills:
            self.skills.append(self.translate(skill[0]), self.translate(skill[1]))

    def translate(self, phrase):
        if phrase.isdecimal():
            print("decimal {}".format(phrase))
            return phrase

        elif phrase == "愚者":
            return "Fool"
        elif phrase == "魔術師":
            return "Magician"
        elif phrase == "女教皇":
            return "Priestess"
        elif phrase == "女帝":
            return "Empress"
        elif phrase == "皇帝":
            return "Emperor"
        elif phrase == "法王":
            return "Hierophant"
        elif phrase == "恋愛":
            return "Lovers"
        elif phrase == "戦車":
            return "Chariot"
        elif phrase == "正義":
            return "Justice"
        elif phrase == "隠者":
            return "Hermit"
        elif phrase == "運命":
            return "Fortune"
        elif phrase == "剛毅":
            return "Strength"
        elif phrase == "刑死者":
            return "Hanged Man"
        elif phrase == "死神":
            return "Death"
        elif phrase == "節制":
            return "Temperance"
        elif phrase == "悪魔":
            return "Devil"
        elif phrase == "塔":
            return "Tower"
        elif phrase == "星":
            return "Star"
        elif phrase == "月":
            return "Moon"
        elif phrase == "太陽":
            return "Sun"
        elif phrase == "審判":
            return "Judgement"

        elif phrase == "\u2212":
            return "-"
        elif phrase == "弱":
            return "weak"
        elif phrase == "耐":
            return "strng"
        elif phrase == "無":
            return "null"
        elif phrase == "反":
            return "repel"
        elif phrase == "吸":
            return "absrb"

        elif phrase == "初期":
            return "initial"

        else:
            log("Untranslateable: " + str(phrase))
            return phrase

    def full_persona(self):
        if self.slug == '?':
            return "Name: {}, Slug: ?".format(self.name)

        msg = r"""
/-----------------------------------------------------------\
| Name: {name:<31}| {arcana:<13}| {lv:<4}|
|-----------------------------------------------------------|
|phys |range|fire |ice  |elec |wind |psy  |nuke |light|curse|
|{phys:<5}|{ranged:<5}|{fire:<5}|{ice:<5}|{electric:<5}|{wind:<5}|{psy:<5}|{nuclear:<5}|{light:<5}|{curse:<5}|
|-----------------------------------------------------------|
|  Strength|{strength:>3}| Skill name:                      | SP | LV |
|     Magic|{magic:>3}| {skill1:<33}|{cost1:>3} |{lv1:>3} |
| Endurance|{endurance:>3}| -                                |  - |  - |
|   Agility|{agility:>3}| -                                |  - |  - |
|      Luck|{luck:>3}| -                                |  - |  - |
\-----------------------------------------------------------/
"""
        msg = msg.strip()
        mapping = {'skill1':'-', 'cost1':'-', 'lv1':'-'}
        mapping = {**mapping, **self.__dict__}

        return msg.format_map(mapping)

    def scrape_spwiki(self):
        address = "http://spwiki.net/persona5/wikis/" + str(self.slug) + ".html"
        page = request.urlopen(address)
        soup = BeautifulSoup(page, 'html.parser')

        tables = soup.find_all('table')

        table = tables[0]
        if table.tr.td.contents[0] == "Lv":
            row = table.find_all('tr')[1]
            try:
                contents = list(map(lambda x:x.contents[0], row.find_all('td')))
            except IndexError:
                return
            try:
                self.init_basics(*contents)
            except TypeError:
                self.init_basics(*contents[:2],*contents[3:8])
        else:
            log("Expected Lv, found " + table.tr.td.contents[0])

        table = tables[1]
        if table.tr.td.contents[0] == "物":
            row = table.find_all('tr')[1]
            self.init_types(*map(lambda x:x.contents[0], row.find_all('td')))
        else:
            log("Expected 物, found " + table.tr.td.contents[0])

        """
        table = tables[2]
        correct_table = False
        skills = []
        for row in table.find_all('tr'):
            if correct_table:
                skills.append( (row.td.contents[0], row.find_all('td')[5].contents[0]) )
            elif row.td.contents[0] == "スキル名":
                correct_table = True
            else:
                log("Expected スキル名, found " + table.td.contents[0])
        #TODO: skills
        """


sluglist = []
unknownlist = []
with open('slugs.csv', mode='r') as slugfile:
    for line in slugfile:
        pair = line.split(',')
        pair = (pair[0].strip(' "'), pair[1].strip(' "\n'))
        try:
            pair = (pair[0], int(pair[1]))
            sluglist.append(pair)
        except ValueError:
            unknownlist.append(pair)

personas = []

for line in sluglist + unknownlis:t
    personas.append(Persona(*line))

"""
open('personas.txt', mode='w').close()

for line in sluglist:
    print(line)
    current = Persona(*line)
    current.scrape_spwiki()
    personas.append(current)
    with open('personas.txt', mode='a') as f:
        try:
            f.write(current.full_persona() + '\n\n')
        except KeyError:
            f.write("Name: {}, Slug: {}\n\n".format(current.name, current.slug))

for line in unknownlist:
    print(line)
    current = Persona(*line)
    personas.append(current)
    with open('personas.txt', mode='a') as f:
        f.write(current.full_persona() + '\n\n')
"""


f = open('personas.pickle', mode='wb')
pickle.dump(personas, f)
f.close()

