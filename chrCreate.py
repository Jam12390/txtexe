from tkinter import *
import time
import json
import random

class Character():
    def __init__(self, name, health, mana, clas, specialty, advant, weak, strength, intelligence, defense, charisma, awareness, lvl, xp):
        self.name = name
        self.health = health #oh my god theres so many attributes
        self.totalHealth = health
        self.mana = mana
        self.characterClass = clas #all of the following are initially derived from the class (excluding lvl and xp) and are increased as level increases
        self.specialty = specialty
        self.advantageType = advant
        self.disadvantageType = weak
        self.strength = strength
        self.intelligence = intelligence
        self.defense = defense
        self.charisma = charisma
        self.awareness = awareness
        self.level = lvl
        self.xp = xp
        self.defending = False
    def attack(self, enemy, ability):
        with open("allAbilities.json", "r") as f:
            currentAttack = json.load(f.read())[ability]
        if self.awareness > 20:
            self.refuse()
        else:
            initDmg = currentAttack["damage"]
            print(f"You use {currentAttack["description"]}") #temp code: change this to run a procedure which outputs the description like during loadin.py, you know what i mean
            if currentAttack["type"].lower() == self.advantageType.lower():
                initDmg = round(initDmg*1.2)
            elif currentAttack["type"].lower() == self.disadvantageType.lower(): #adv and disadv types are gotten from class
                initDmg = round(initDmg*0.7)
            if currentAttack["type"].lower() == "physical":
                initDmg = round(initDmg*(1+(0.4*(self.strength/20)))) #increase damage by up to 40% from strength/20(max level) multiplied by 0.4 and added to 1 to get a 0-40% increase
            elif currentAttack["type"].lower() == "magic":
                initDmg = round(initDmg*(1+(0.4*(self.intelligence/20)))) #same with magic but with intelligence instead of strength
            enemy.health -= round(initDmg*1-(0.4*(enemy.defense/20))) #damage dealing works the same with percentage decreases (maybe add weakness types later?)
    def refuse(self):
        print("Your vessel refuses to attack") #use vessel as a term here since this can only be reached later in the game. This is also unfinished as idrk what to do here
    def defend(self):
        print("You defend") #increase defense for a turn, see attack() for effects
        defense += 10
        self.defending = True

class Enemy(Character):
    def __init__(self, name, health, mana, advant, weak, defense, lvl):
        super().__init__(name, health, mana, advant, weak, defense, lvl)
    def decision(self, player):
        options = []
        opponentLow = True if player.health < player.totalHealth*0.25 else False
        if self.health < self.totalHealth/2:
            if self.health < self.totalHealth/4 and not opponentLow:
                options.append(["heal", 9])
                options.append(["statboost", 4])
                options.append(["attack", 2])
            elif self.health < self.totalHealth/4 and opponentLow:
                options.append(["heal", 8])
                options.append(["statboost", 3])
                options.append(["attack", 4]) #todo: continue *trying* to make a semi-decent enemy ai
            elif opponentLow:
                options.append(["heal", 3])
                options.append(["statboost", 2])
                options.append(["attack", 10])
            else:
                options.append(["heal", 1])
                options.append(["statboost", 2])
                options.append(["attack", 12])
        if self.health < self.totalHealth and self.health > self.totalHealth*0.75:
            options.append(["heal", 1])
            options.append(["statboost", 5])
            options.append(["attack", 9])
        elif self.health > self.totalHealth*0.75:
            options.append(["heal", 0])
            options.append(["statboost", 4])
            options.attack(["attack", 11]) #this is extremely basic decision making based on only health currently - will add mana as a weighting later during what spell to cast.
    def attack():
        pass

        


def welcome():
    with open("characters.json", "r") as f:
        data = f.read()
        data = json.load(data)

    if len(data) == 0:
        chrWelcomeText = [
            "No Characters Detected", "\n",
            "CharacterCreator.exe Starting...", "\n", 1,
            "kablam boom bam", "\n",
            "Hello", "\n",
            "Choose It's Name", "\n", "io bound", 1,
            "Choose It's Class", "\n", "io bound", 1,
            "Choose It's Specialty", "\n", "io bound", 1,
            "Choose It's Ability", "\n", "io bound", 1,
        ]
    else:
        chrWelcomeText = [
            "Oh.", "\n", 1,
            "You died.", 1,
            "Usually This Means That You've Lost", "\n", 0.5,
            "However I'll Entertain The Idea Of You Continuing", "\n",
            "You Know The Drill.", "\n", 0.5,
            "kablam boom bam", "\n",
            "Choose It's Name", "\n", "io bound", 1,
            "Choose It's Class", "\n", "io bound", 1,
            "Choose It's Specialty", "\n", "io bound", 1,
            "Choose It's Ability", "\n", "io bound", 1,
        ]