from tkinter import *
import time
import json
import random
import characterClasses as chrClass
from pynput.keyboard import *

name = ""
clas = ""
subClass = ""
ability = ""
userName = ""
entryText = ""

playerCharacter = None

def welcome(rootWindow, entryObj):
    def submitText(key):
        if key == Key.enter:
            print("pain and suffering")
            getValue()

    listener = Listener(on_press=submitText)
    with open("characters.json", "r") as f:
        chrData = json.load(f)
        f.close()
    
    with open("characterOptions.json", "r") as f:
        chrOptions = json.load(f)
        f.close()

    global userName
    global name
    global clas
    global subClass
    global ability
    global entryText
    global playerCharacter

    dialogueIndex = 0

    dialogueLabel = Label(rootWindow, text="")
    dialogueLabel.pack()

    currentText = ""
    nameRefuse = 0
    defiance = 0
    subClasses = chrOptions["subclasses"]
    abilities = chrOptions["abilities"]

    attributeCount = 0

    if len(chrData) == 0:
        chrWelcomeText = [
                        "Ah, a new subject.", "\n", 2,
                        "Welcome to the game.", "\n", 0.5,
                        "I am the Overseer of this world", "\n", 1,
                        "I will be the one to record the outcome of this", "..", "experiment.", "\n", 0.5, #15
                        "Before you inevitably ask like your predecessors, you do not need to or will ever know what the experiment is.", "\n", 3,
                        "Moving on, seeing as I have introduced myself, I see it fit for you to do the same.", "\n", 2,
                        "So subject, What is your name?", "\n", "io bound", "username", #25
                        # If a name is provided
                        f"{name.capitalize()}, welcome.", "\n", 1,
                        # If no name is provided
                        "I believe you forgot to put your name,", "\n", 0.5,
                        "I will give you the benefit of the doubt and allow you to put your name again.", "\n", "io bound", "username",
                        # If no name is provided again
                        "...", "\n", 2,
                        "Subject, a name is required to proceed with the experiment.", "\n", "io bound", "username",
                        # If no name is provided for a third time
                        "If you do not wish to give yourself a name,", "\n", 2,
                        "Then I will.", "\n", 1,
                        "Welcome, SBJ51.", "\n", 1,
                        "This does not bode well for the rest of the experiment,", "\n", 3.2,
                        "However, we must move on,", "\n", 0.1,
                        # Skip this line if a name was not provided at all
                        "Now that you've introduced yourself,", "\n", 0.5, #58 first, 60 end
                        "Let's move onto creating your vessel, or as you call them, 'characters'.", "\n", 0.5,
                        "So without further ado,", "\n", 1.5,
                        "kablam boom bam", "\n",
                        "Choose Its Name", "\n", "io bound", "name",
                        #if no name was provided for both. defiance = 1
                        "Subject.", "\n", 3,
                        "I am reaching the limit of my patience", "\n", 2,
                        "I cannot and will not choose for you.", "\n", 2,
                        "If you cannot obey basic instructions, it is pointless to continue the experiment.", "\n", 2,
                        "Therefore", "\n", 1,
                        "Give", "\n", 2,
                        "Your character", "\n", 2,
                        "A name", "\n", "io bound", "name",
                        #if no name is provided a second time
                        "eoD", #98
                        #if no name is provided here but was before. defiance = 0
                        "If you really cannot think of a name", "\n", 1,
                        "Then I will choose for you only on this occasion", "\n", 2,
                        "James seems like a fitting name", "\n", 2, "eoD",
                        #else continue as normal
                        "Choose Its Class", "\n", "io bound", "class",#109 start, 112 end
                        #if nothing is chosen (2nd time) defiance = 1
                        f"{name}, please make your character.", "\n", 2,
                        "It is integral to the experiment", "\n", 1,
                        "Choose a class.", "\n", "io bound", "class",
                        #if nothing is chosen again (2nd time) defiance = 1, will go up to 2
                        "Do you insist on being difficult?", "\n", 3,
                        "I do not know what you get from this.", "\n", 2,
                        "However I will warn you now to stop," "\n", 1.5,
                        "As you will not like what comes next if you continue to be defiant.", "\n", 2,
                        "I will choose for you again", "\n", 1,
                        "Your character will be a wizard." "\n", 1,
                        "End of.", "\n", 1, "eoD", #143
                        #if nothing is chosen (1st time) defiance = 0
                        "Did you forget to put something?", "\n", 1,
                        "Or did you misspell?", "\n", 1,
                        "Here, try again", "\n", "io bound", "class",
                        #if nothing is chosen again (1st time) defiance up to 1
                        "Alright, I will tolerate your refusal this time, but only this time", "\n", 2,
                        "Your character will be a wizard.", "\n", 1, "eoD",
                        #move on again
                        "Choose Its Specialty", "\n", "io bound", "subclass", #161 start, 164 end
                        #defiance = 2
                        "eoD", #go to defiance ending
                        #defiance = 1
                        "And you refuse to choose again.", "\n", 1,
                        "I will choose one more time for you.", "\n", 2,
                        "Do not test my patience again.", "\n", 1,
                        f"You will be a .", "\n", 1, #TODO: make sure the subclasses list is populated before testing, will crash otherwise {subClasses[clas][0]}
                        #defiance = 0 and nothing put
                        "You forgot to put something.", "\n", 1,
                        "Please choose.", "\n", "io bound", "subclass",
                        #defiance = 0 and something put
                        "That's not one of the choices.", "\n", 1,
                        "Or maybe you misspelled.", "\n", 0.5, #190
                        "Anyway, please choose an available class", "\n", "io bound", "subclass",
                        #something not put again and defiance = 0
                        "I will choose for you then.", "\n", 2,
                        f"You will be a ", "\n", 1, "eoD", #201 {subClasses[clas][0]}
                        #continue as normal
                        "Choose Its Ability", "\n", "io bound", "ability", #202 start, 203 end
                        #defiance = 2
                        "eoD",
                        #defiance = 1
                        "Since we're at the end of this and my patience,", "\n", 0.5,
                        f"You get  as your ability.", "\n", 0.5, #{abilities[clas][0]}
                        #defiance = 0
                        "That's not an ability.", "\n", 1,
                        "Please choose an ability which you see here.", "\n", "io bound", "ability",
                        #not chosen again
                        "Why'd you- nevermind.", "\n", 0.5,
                        "I don't see a point in you being indecisive so I will choose for you.", "\n", 2,
                        f"Your ability is .", "\n", 0.5, #{abilities[clas][0]}
                        #continue as normal
                        "endChr", #227 - jesus fking christ
                        "Here's your character:", "\n", 0.5,
                        f"pretend theres something here :(", "\n", 1, #incomplete but :l {playerCharacter.health} NEVERMIND IT DOESNT WORK WHY
                        "Before you leave.", "\n", 2,
                        "Please do take my world seriously,", "\n", 3,
                        "Your actions here will have consequences.", "\n", 3,
                        "And although I am merciful,", "\n", 1,
                        "I do not tolerate subjects who attempt to tamper with my work.", "\n", 4,
                        "Do with that information what you will.", "\n", 4,
                        f"Goodbye for now, {name}.", "\n", 1,
                        "And remember,", "\n", 1,
                        "I'm always watching.", "END"
                        ]
        for line in range(0,len(chrWelcomeText)):
            try:
                chrWelcomeText[dialogueIndex] = float(chrWelcomeText[dialogueIndex])
                isFloat = True
            except:
                isFloat = False
            if dialogueIndex == len(chrWelcomeText):
                line = len(chrWelcomeText)
            if chrWelcomeText[dialogueIndex] == "\n":
                currentText += chrWelcomeText[dialogueIndex]
                dialogueLabel.config(text=currentText)
            elif isFloat:
                time.sleep(chrWelcomeText[dialogueIndex])
            elif chrWelcomeText[dialogueIndex] == "eoD":
                defiance += 1
            elif chrWelcomeText[dialogueIndex] == "endChr":
                playerCharacter = createCharacter(name, clas, subClass, ability)
            elif chrWelcomeText[dialogueIndex] == "io bound":
                def handleInput():
                    global entryText
                    entryText = getEntry.get().strip()
                def getValue():
                    global entryText
                    print("do you even fucking work")
                    entryText = entryObj.get() #TODO: WHY WONT THIS FUCKING WORK
                    print("Entry text")
                getEntry = StringVar()
                getEntry.trace_add("write", handleInput)
                entryObj.delete(0, END)
                entryObj.focus_set()
                print("how")
                listener.start()

                root = entryObj.winfo_toplevel()
                root.wait_variable(entryText)
                if attributeCount == 0:
                    if len(entryText) > 0:
                        userName = entryText
                    else:
                        userName = entryText #TODO: add defiance route here and everywhere else here
                    attributeCount += 1
                    dialogueIndex = 57
                elif attributeCount == 1:
                    if len(entryText) > 0:
                        name = entryText
                    else:
                        name = entryText #TODO: add defiance route here and everywhere else here
                    attributeCount += 1
                    dialogueIndex = 108
                elif attributeCount == 2:
                    if len(entryText) > 0 and entryText.lower() in chrOptions["classes"]:
                        clas = entryText
                    else:
                        clas = entryText #TODO: add defiance route here and everywhere else here
                    attributeCount += 1
                    dialogueIndex = 160
                elif attributeCount == 3:
                    if len(entryText) > 0 and entryText.lower() in chrOptions[clas.lower()]:
                        subClass = entryText
                    else:
                        subClass = entryText #TODO: add defiance route here and everywhere else here
                    attributeCount += 1
                elif attributeCount == 4:
                    if len(entryText) > 0 and entryText in chrOptions[clas.lower()]:
                        ability = entryText
                    else:
                        ability = entryText #TODO: add defiance route here and everywhere else here
                    attributeCount += 1
                    dialogueIndex = 201
            elif ".." in str(chrWelcomeText[dialogueIndex]):
                for dot in chrWelcomeText[dialogueIndex]:
                    currentText += dot
                    time.sleep(1)
            elif chrWelcomeText[dialogueIndex] == "END":
                print(playerCharacter.health)
                return playerCharacter
            else:
                for letter in range(0,len(chrWelcomeText[dialogueIndex])):
                    currentText += chrWelcomeText[dialogueIndex][letter]
                    dialogueLabel.config(text=currentText)
                    if chrWelcomeText[dialogueIndex][letter] == "," and letter != len(chrWelcomeText[dialogueIndex]):
                        time.sleep(0.5)
                    else:
                        time.sleep(0.01)
            dialogueIndex += 1

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
    return chrClass.Character(name=name, health=health, mana=mana, advant=advant, weak=weak, strength=strength, intelligence=intelligence, defense=defense, charisma=charisma, awareness=0, abilities=[ability], lvl=1, xp=0)