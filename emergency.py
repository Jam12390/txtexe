import json

class Character():
    def __init__(self, name, health, mana, clas, specialty, advant, weak, strength, intelligence, defense, charisma, abilities, lvl, xp):
        self.name = name
        self.health = health #oh my god theres so many attributes
        self.totalHealth = health
        self.mana = mana
        self.totalMana = mana
        self.characterClass = clas #all of the following are initially derived from the class (excluding lvl and xp) and are increased as level increases
        self.specialty = specialty
        self.advantageType = advant
        self.disadvantageType = weak
        self.disadvantageTurns = 0
        self.strength = strength
        self.intelligence = intelligence
        self.defense = defense
        self.charisma = charisma
        self.abilities = abilities #use dictionary of dictionaties here to store name, type, description, damage, disadvantage chance, effect, etc. 
        self.action = ""
        self.level = lvl
        self.xp = xp
        self.defending = False

def getAttributes(clas, subClass):
    match(clas.lower()):
        case("warrior"):
            health, strength, intelligence, defense, charisma = 100, 12, 8, 10, 11
            weak = "none"
            advant = "physical"
        case("barbarian"):
            health, strength, intelligence, defense, charisma = 150, 15, 6, 7, 2
            weak = "magic"
            advant = "physical"
        case("wizard"):
            health, strength, intelligence, defense, charisma = 80, 8, 15, 6, 5
            weak = "physical"
            advant = "magic"
    match(subClass.lower()):
        case("paladin"):
            health += 10
            defense += 1
        case("knight"):
            health += 20
            defense += 2
            strength -= 1
            charisma += 1
            intelligence -= 1
        case("berserker"):
            health += 25
            strength += 3
            intelligence = 0
            charisma -= 1
            defense -= 3
        case("thief"):
            health -= 10
            charisma += 2
            defense -= 1
        case("mage"):
            intelligence += 1
            charisma -= 1
            strength -= 1
        case("evil wizard"):
            strength += 2
            intelligence += 1
            charisma -= 3
            defense -= 2
        case(_):
            pass
    mana = round(100*(intelligence/10))
    return health, mana, strength, intelligence, defense, charisma, weak, advant

def createCharacter(name, clas, subClass, ability):
    health, mana, strength, intelligence, defense, charisma, weak, advant = getAttributes(clas, subClass)
    return Character(name=name, health=health, clas=clas, specialty=subClass, mana=mana, advant=advant, weak=weak, strength=strength, intelligence=intelligence, defense=defense, charisma=charisma, abilities=[ability], lvl=1, xp=0)

options = open("characterOptions.json", "r")
chrOptions = json.load(options)
options.close()

name = input("Enter name\n")
clas = ""

while not clas.lower() in chrOptions["classes"]:
    print("Available classes")
    for item in range(0,len(chrOptions["classes"])):
        print(item, chrOptions["classes"][item])
    clas = input("Enter class\n")

subClass = ""

while not subClass.lower() in chrOptions["subclasses"][clas.lower()]:
    print("Available classes")
    for item in range(0,len(chrOptions["subclasses"][clas.lower()])):
        print(item, chrOptions["subclasses"][clas.lower()][item])
    subClass = input("Enter subclass\n")

player = createCharacter(name=name, clas=clas, subClass=subClass, ability="Block")
print(
    f"Name: {player.name}\n"
    f"Health: {player.totalHealth}\n",
    f"Mana: {player.totalMana}\n",
    f"Class: {player.characterClass}, Subclass: {player.specialty}\n",
    f"Strength: {player.strength}, Defense: {player.defense}\n",
    f"Intelligence: {player.intelligence}\n",
    f"Charisma: {player.charisma}."
)