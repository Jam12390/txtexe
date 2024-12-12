class Character():
    def __init__(self, name, health, mana, clas, specialty, advant, weak, strength, intelligence, defense, charisma, awareness, abilities, lvl, xp):
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
        self.awareness = awareness
        self.abilities = abilities #use dictionary of dictionaties here to store name, type, description, damage, disadvantage chance, effect, etc. 
        self.action = ""
        self.level = lvl
        self.xp = xp
        self.defending = False

name = input("enter name")
