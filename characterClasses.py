import random
import json

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
    def __init__(self, name, health, mana, advant, weak, defense, abilities, lvl):
        super().__init__(name, health, mana, advant, weak, defense, abilities, lvl)
        self.disadvantageTurns = 0
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
        elif self.health < self.totalHealth and self.health > self.totalHealth*0.75:
            options.append(["heal", 1])
            options.append(["statboost", 5])
            options.append(["attack", 9])
        elif self.health > self.totalHealth*0.75:
            options.append(["heal", 0])
            options.append(["statboost", 4])
            options.append(["attack", 11]) #this is extremely basic decision making based on only health currently - will add mana as a weighting later during what spell to cast.
        if player.disadvantageTurns > 0:
            options[2][1] += 3
            options[0][1] -= 2
            options[1][1] -= 1
            if options[0][1] < 0:
                options[0][1] = 0
            if options[1][1] < 0:
                options[1][1] = 0
        self.getMainDecision(options)

    def getMainDecision(self, options):
        decision = random.randint(0,(options[0][1]+options[1][1]+options[2][1]))
        while isinstance(decision, int):
            if decision <= options[0][1]:
                present, abilities = self.checkAbilityPresence(type="heal")
                if present:
                    decision = "heal"
                else:
                    options[0][1] = 0
            elif decision <= options[0][1]+options[1][1]:
                present, abilities = self.checkAbilityPresence(type="statboost")
                if present:
                    decision = "statboost"
                else:
                    options[1][1] = 0
            elif decision <= options[0][1]+options[1][1]+options[2][1]:
                present, abilities = self.checkAbilityPresence(type="attack")
                if present:
                    decision = "attack"
                else:
                    options[2][1] = 0
            if isinstance(decision, int):
                decision = random.randint(0,(options[0][1]+options[1][1]+options[2][1]))
        self.action = self.chooseSubDecision(abilities)

    def chooseSubDecision(self, availableAbilities):
        dmgSorted = []
        magicCount = 0
        for i in availableAbilities:
            if i["type"] == "magic":
                magicCount += 1
        if magicCount > 0:
            typeProb = [
                round(
                    (1-(1-self.mana/self.totalMana))*100 #physical probability
                ),
                round(
                    (1-(self.mana/self.totalMana))*100 #magic probability
                )
            ]
        else:
            typeProb = [1,0]
        attackType = random.randint(0,(typeProb[0]+typeProb[1]))
        if attackType <= typeProb[0]:
            attackType = "physical"
        else:
            attackType = "magic"
        for ability in availableAbilities:
            if ability["type"] == attackType:
                dmgSorted += ability
        dmgSorted = sorted(dmgSorted, key=lambda x: x["damage"])
        if attackType == "magic":
            for ability in dmgSorted:
                if self.mana >= ability["manacost"] and ability["type"] == "magic":
                    finalDecision = ability
        else:
            finalDecision = dmgSorted[0]
        return finalDecision

    def checkAbilityPresence(self, type):
        foundAbilities = {}
        for ability in self.abilities: #a dictionary of dictionaries, will most likely contain name: name, description, type, dmg, mana cost
            if ability["type"].lower() == type.lower():
                foundAbilities[ability["name"]] = ability
        if len(foundAbilities) > 0:
            return True, foundAbilities
        else:
            return False, foundAbilities
    def attack(self, player):
        finalDecision = self.decision(player=player)
        initDmg = finalDecision["damage"]
        self.mana -= finalDecision["manacost"]
        if self.disadvantageTurns > 0:
            disadvantageRoll = random.randint(0,20)
            miss = True if disadvantageRoll == 0 else False
            self.disadvantageTurns -= 1
            if disadvantageRoll != 0 and disadvantageRoll < 11:
                initDmg = round(initDmg*0.6)
            elif disadvantageRoll < 16:
                initDmg = round(initDmg*0.8)
            elif disadvantageRoll < 20:
                initDmg = round(initDmg*0.9)
            elif disadvantageRoll == 20:
                initDmg = initDmg
            elif miss:
                initDmg = 0
        if self.advantageType == finalDecision["type"]:
            initDmg = round(initDmg*1.5)
        print(f"{self.name} uses {finalDecision["name"]}")
        if not miss:
            print(f"{player.name} was damaged for {initDmg}")
            player.health -= initDmg
        else:
            print("The attack misses")
        if finalDecision["disadvantageturns"] > 0:
            disadvantageEffect = random.randint(0,100)
            if disadvantageEffect <= finalDecision["disadvantageProbability"]:
                print(f"{player.name} was disadvantaged for {finalDecision["disadvantageturns"]} turns")
                player.disadvantageTurns += finalDecision["disadvantageturns"]