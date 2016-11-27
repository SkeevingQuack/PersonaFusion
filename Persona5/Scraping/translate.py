

class UnknownPhraseError(Exception):
    def __init__(self, phrase, kind):
        self.phrase = phrase
        self.kind = kind

blank_markers = [
    "\uff0d", # long dash
    "\u2212", # dash
    "\u002d", # hyphen
    "\u30fc", # chouonpu
    "\u2010", # hyphen
    "\u2013", # dash
    "\u2014", # em dash
]

def arcana(phrase):
    if phrase == "愚者":
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

    else:
        raise UnknownPhraseError(phrase, "arcana")

def resistance(phrase):
    if phrase == "弱":
        return "weak"
    elif phrase == "耐":
        return "resist"
    elif phrase == "無":
        return "null"
    elif phrase == "反":
        return "repel"
    elif phrase == "吸":
        return "absorb"

    elif phrase in blank_markers:
        return "-"

    else:
        raise UnknownPhraseError(phrase, "resistance")

def attribute(phrase):
    if phrase == "物理":
        return "physical"
    elif phrase == "銃撃" or phrase == "銃":
        return "ranged"
    elif phrase == "火炎" or phrase == "火":
        return "fire"
    elif phrase == "氷結" or phrase == "氷" or phrase == "雷":
        return "ice"
    elif phrase == "電撃" or phrase == "電":
        return "electric"
    elif phrase == "疾風" or phrase == "疾":
        return "wind"
    elif phrase == "念動" or phrase == "念":
        return "psy"
    elif phrase == "核熱":
        return "nuclear"
    elif phrase == "祝福":
        return "light"
    elif phrase == "呪怨":
        return "curse"
    elif phrase == "万能":
        return "almighty"
    elif phrase == "補助":
        return "support"
    elif phrase == "自動":
        return "passive"
    elif phrase == "異常" or phrase == "バステ":
        return "ailment"
    elif phrase == "回復":
        return "healing"

    else:
        raise UnknownPhraseError(phrase, "attribute")

def cost(phrase):
    if phrase.isdecimal():
        return "{} SP".format(phrase)
    elif "HP%" == phrase:
        return "?% HP"
    elif '%' in phrase:
        try:
            return "{}% HP".format(int(phrase.strip(" %HP")))
        except ValueError:
            raise UnknownPhraseError(phrase, "cost")
    elif 'HP' in phrase:
        try:
            return "{} HP".format(int(phrase.strip(" HP")))
        except ValueError:
            raise UnknownPhraseError(phrase, "cost")
    elif phrase in blank_markers:
        return "-"

    else:
        raise UnknownPhraseError(phrase, "cost")

def target(phrase):
    if phrase == "敵1体" or phrase == "敵一体":
        return "one enemy"
    elif phrase == "味方1体" or phrase == "味方一体":
        return "one ally"
    elif phrase == "敵全体":
        # Orobas 的全体
        return "all enemies"
    elif phrase == "味方全体":
        return "all allies"
    elif phrase == "自身" or phrase == "自分" or phrase == "ペルソナ自身":
        return "self"
    elif phrase == "敵味方全体":
        return "all"

    else:
        raise UnknownPhraseError(phrase, "target")

def skill_lvl(phrase):
    if phrase.isdecimal():
        return phrase
    elif phrase == "初期" or phrase == "初" or\
            phrase == "所期" or phrase in blank_markers:
        return "innate"

    else:
        raise UnknownPhraseError(phrase, "skill lvl")

def number(phrase):
    if phrase.isdecimal():
        return phrase

    else:
        raise UnknownPhraseError(phrase, "number")
