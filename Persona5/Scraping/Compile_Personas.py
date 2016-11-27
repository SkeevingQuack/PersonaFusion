from urllib import request, error
from bs4 import BeautifulSoup
from time import sleep
import pickle
import csv

import persona
import translate

def main():
    sluglist = []
    with open("slugs.csv", newline='', encoding='utf-8') as slugfile:
        slugreader = csv.reader(slugfile, skipinitialspace=True)
        for row in slugreader:
            sluglist.append(tuple(row))

    personas = []
    for row in sluglist:
        current_persona = persona.Persona(*row)

        if current_persona.slug == '?':
            personas.append(current_persona)
            continue

        address = current_persona.wiki.format(current_persona.slug)
        print("{}, opening {}".format(current_persona, address))
        try:
            page = request.urlopen(address)
        except error.URLError as err:
            msg = "Page for {} was unable to be retrieved:".format(row)
            errlog("{}\n{}".format(err, msg))
            personas.append(current_persona)
            continue

        soup = BeautifulSoup(page, "html.parser")

        current = soup.find(id='content_1_0')
        current_persona.alt_names = [list(current.strings)[0].strip()]

        current = current.parent
        tables = current.find_all(class_='ie5')

        try:
            current = tables[0].table
        except IndexError:
            errlog("{}'s page contains no tables".format(current_persona))
            personas.append(current_persona)
            continue
        heads = current.thead.find_all('td')
        bodies = current.tbody.find_all('td')
        basics_match(heads, bodies, current_persona)

        try:
            current = tables[1].table
        except IndexError:
            errlog("{}'s page contains but one table".format(current_persona))
            personas.append(current_persona)
            continue
        heads = current.thead.find_all('td')
        bodies = current.tbody.find_all('td')
        resistances_match(heads, bodies, current_persona)

        try:
            current = tables[2].table
        except IndexError:
            errlog("{}'s page contains but two table".format(current_persona))
            personas.append(current_persona)
            continue
        heads = current.thead.find_all('td')
        body_rows = current.tbody.find_all('tr')
        skills_match(heads, body_rows, current_persona)

        personas.append(current_persona)
        sleep(2) # sleep 2 seconds as a rate-limit

    with open('personas.pickle', mode='wb') as picklefile:
        pickle.dump(personas, picklefile)


def errlog(msg):
    print(msg)
    with open('errors.log', mode='a', encoding='utf-8') as file:
        file.write("-- {}\n".format(msg))

def strip_td(td):
    try:
        return td.string.strip()
    except AttributeError:
        return td.string

def basics_match(heads, bodies, sona):
    heads = list(map(strip_td, heads))
    bodies = list(map(strip_td, bodies))
    sona.stats = persona.Stats()

    for index, head in enumerate(heads):
        try:
            if not bodies[index]:
                pass
            elif head == "Lv":
                sona.lvl = translate.number(bodies[index])
            elif (head == "アルカナ" or head == "種族"):
                sona.arcana = translate.arcana(bodies[index])
            elif head == "シャドウ名":
                pass
            elif head == "力":
                sona.stats.strength = translate.number(bodies[index])
            elif head == "魔":
                sona.stats.magic = translate.number(bodies[index])
            elif head == "耐":
                sona.stats.endurance = translate.number(bodies[index])
            elif head == "速":
                sona.stats.agility = translate.number(bodies[index])
            elif head == "運":
                sona.stats.luck = translate.number(bodies[index])
            else:
                loc = "While scraping basics for {}:".format(sona)
                msg = "header '{}' was not recognized.".format(head)
                errlog("{}\n{}".format(loc, msg))
        except translate.UnknownPhraseError as err:
            loc = "While scraping basics for {}:".format(sona)
            msg = "translate couldn't find a {1} match for {0}."
            errlog("{}\n{}".format(loc, msg.format(*err.args)))

    if '?' in sona.stats.__dict__.values():
        sona.stats = '?'

def resistances_match(heads, bodies, sona):
    heads = list(map(strip_td, heads))
    bodies = list(map(strip_td, bodies))
    sona.resistances = persona.Resistances()

    for index, head in enumerate(heads):
        try:
            if not bodies[index]:
                pass
            elif head == "物":
                sona.resistances.physical = translate.resistance(bodies[index])
            elif head == "銃":
                sona.resistances.ranged = translate.resistance(bodies[index])
            elif head == "火":
                sona.resistances.fire = translate.resistance(bodies[index])
            elif head == "氷":
                sona.resistances.ice = translate.resistance(bodies[index])
            elif head == "電":
                sona.resistances.electric = translate.resistance(bodies[index])
            elif head == "風":
                sona.resistances.wind = translate.resistance(bodies[index])
            elif head == "念":
                sona.resistances.psy = translate.resistance(bodies[index])
            elif head == "核":
                sona.resistances.nuclear = translate.resistance(bodies[index])
            elif head == "祝":
                sona.resistances.light = translate.resistance(bodies[index])
            elif head == "呪":
                sona.resistances.curse = translate.resistance(bodies[index])
            else:
                loc = "While scraping resistances for {}:".format(sona)
                msg = "header '{}' was not recognized.".format(head)
                errlog("{}\n{}".format(loc, msg))
        except translate.UnknownPhraseError as err:
            loc = "While scraping resistances for {}:".format(sona)
            msg = "translate couldn't find a {1} match for {0}."
            errlog("{}\n{}".format(loc, msg.format(*err.args)))

    values = sona.resistances.__dict__.values()
    if '?' in values and not all(x == '?' for x in values):
        for attribute, value in sona.resistances.__dict__.items():
            if value == '?':
                setattr(sona, attribute, '-')

def skills_match(heads, rows, sona):
    if len(rows) < 2:
        return

    heads = list(map(strip_td, heads))
    headlist = {}
    for index, head in enumerate(heads):
        if head == "スキル名":
            headlist['name'] = index
        elif head == "属性":
            headlist['attribute'] = index
        elif "SP" in head:
            headlist['cost'] = index
        elif head == "対象":
            headlist['target'] = index
        elif "Lv" in head:
            headlist['lvl'] = index
        elif head == "効果":
            pass
        else:
            loc = "While scraping skills for {}:".format(sona)
            msg = "header '{}' was not recognized.".format(head)
            errlog("{}\n{}".format(loc, msg))

    sona.skills = []

    for row in rows:
        current = persona.PersonaSkill()
        row = list(map(strip_td, row.find_all('td')))
        for label, column in headlist.items():
            try:
                if not row[column]:
                    pass
                elif label == "name":
                    current.name = row[column]
                elif label == "attribute":
                    current.attribute = translate.attribute(row[column])
                elif label == "cost":
                    current.cost = translate.cost(row[column])
                elif label == "target":
                    current.target = translate.target(row[column])
                elif label == "lvl":
                    current.lvl = translate.skill_lvl(row[column])
                else:
                    loc = "For {}'s skills,".format(sona)
                    msg = "{} is somehow in the headlist".format(label)
                    errlog("{} {}".format(loc, msg))
                    return
            except translate.UnknownPhraseError as err:
                loc = "While scraping skills for {}:".format(sona)
                msg = "translate couldn't find a {1} match for {0}."
                errlog("{}\n{}".format(loc, msg.format(*err.args)))
        sona.skills.append(current)


if __name__ == "__main__":
    errlog("-----------------------------------\n\n")
    main()
