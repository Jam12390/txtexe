from tkinter import *
from pynput.keyboard import Key, Listener
import time
import json
import loadin as ldScreen

currentIndex = 0
currentScenario = "menu"

jsonFile = open("menus.json", "r")
allMenus = json.load(jsonFile)
jsonFile.close()

options = open("options.json", "r")
optionsJson = json.load(options)
options.close()

menuOpt = allMenus["mainmenu"]
currentMenu = "mainmenu"
inMenu = True

isPrologue = True
chrName = "Test"
previousMenus = []

availableColours = ["Green", "White", "Pink", "Blue", "Cyan", "Purple"]
currentColourIndex = int(availableColours.index(optionsJson["textcolour"].capitalize()))
currentColour = availableColours[currentColourIndex]

textSpeedMult = float(optionsJson["textspeed"])

arts = [
    r"""
____________  __         __  ____________   ____________   __         __  ____________
|__________|  \ \       / /  |__________|   |__________|   \ \       / /  |__________|
|__________|   \ \     / /   |__________|   |  |            \ \     / /   |  |        
    |  |        \ \   / /        |  |       |  |_____        \ \   / /    |  |_____   
    |  |         \ \ / /         |  |       |   _____|        \ \ / /     |   _____|  
    |  |         / / \ \         |  |       |  |              / / \ \     |  |        
    |  |        / /   \ \        |  |       |  |             / /   \ \    |  |        
    |  |       / /     \ \       |  |       |  |_______     / /     \ \   |  |_______ 
    |__|      /_/       \_\      |__|       |__________|   /_/       \_\  |__________|
""",
r"""
____________    ____________   __         __  ____________   ____________
|__________|    |__________|   \ \       / /  |__________|   |__________|
|__________|    |  |            \ \     / /   |  |           |__________|
    |  |        |  |_____        \ \   / /    |  |_____          |  |    
    |  |        |   _____|        \ \ / /     |   _____|         |  |    
    |  |        |  |              / / \ \     |  |               |  |    
    |  |        |  |             / /   \ \    |  |               |  |    
    |  |        |  |_______     / /     \ \   |  |_______        |  |    
    |__|        |__________|   /_/       \_\  |__________|       |__|    
"""
]
titles = ["TXTEXE", "TEXET"]
titleChoice = int(titles.index(optionsJson["title"].upper()))

def caseInput(key): #any time a ui input is pressed
    global currentIndex
    global previousMenus
    match (key):
        case (Key.esc):
            if inMenu:
                menuBack(previousMenus, menu) #TODO: add arguments for this so it doesnt fucking break
        case (Key.up):
            if inMenu:
                currentIndex = menuUp(currentIndex)
        case (Key.down):
            if inMenu:
                currentIndex = menuDown(currentIndex)
        case (Key.left):
            if inMenu:
                if str(currentMenu.lower()+":"+menuOpt[currentIndex].split(":")[0].replace("> ", "").lower()+":") in allMenus["arrowkeymenu"]:
                    findArrowMenu(menuOpt[currentIndex].split(":")[0].replace("> ", "").lower()+":", "left")
        case (Key.right):
            if inMenu:
                if str(currentMenu.lower()+":"+menuOpt[currentIndex].split(":")[0].replace("> ", "").lower()+":") in allMenus["arrowkeymenu"]:
                    findArrowMenu(menuOpt[currentIndex].split(":")[0].replace("> ", "").lower()+":", "right")
        case (Key.enter):
            if rootWindow.focus_displayof():
                if inMenu:
                    selectIndex(currentIndex)
                else:
                    submitText()

def findArrowMenu(menu, direction):
    match (menu):
        case("text colour:"):
            textColourSwap(direction)
        case("text speed:"):
            changeTextSpeed(direction)

def changeTextSpeed(direction):
    global textSpeedMult
    if direction.lower() == "left":
        textSpeedMult -= 0.1
        if textSpeedMult < 0.5:
            textSpeedMult = 0.5
    else:
        textSpeedMult += 0.1
        if textSpeedMult > 2:
            textSpeedMult = 2
    textSpeedMult = round(textSpeedMult, 1)
    menuOpt[currentIndex] = menuOpt[currentIndex].split(":")[0] + ":" + " < " + str(textSpeedMult) + " >"
    optionIndex = allMenus[currentMenu].index(str(menuOpt[currentIndex].split(":")[0]+":"+" < "+str(textSpeedMult)+" >"))
    allMenus[currentMenu][optionIndex] = menuOpt[currentIndex].split(":")[0]+":"+" < "+str(textSpeedMult)+" >"
    redrawMenu(menu)

def textColourSwap(direction):
    global currentColourIndex
    if direction.lower() == "left":
        currentColourIndex -= 1
        if currentColourIndex < 0:
            currentColourIndex = len(availableColours)-1
    else:
        currentColourIndex += 1
        if currentColourIndex > len(availableColours)-1:
            currentColourIndex = 0
    currentColour = availableColours[currentColourIndex].lower()
    menu.config(fg=currentColour)
    title.config(fg=currentColour)
    menuOpt[currentIndex] = menuOpt[currentIndex].split(":")[0]+":"+" < "+currentColour.capitalize()+" >"
    optionIndex = allMenus[currentMenu].index(str(menuOpt[currentIndex].split(":")[0]+":"+" < "+currentColour.capitalize()+" >"))
    allMenus[currentMenu][optionIndex] = menuOpt[currentIndex].split(":")[0]+":"+" < "+currentColour.capitalize()+" >"
    redrawMenu(menu)


def menuUp(currentIndex):
    global menuOpt
    if not currentIndex-1 < 0:
        menuOpt[currentIndex-1] = "> " + menuOpt[currentIndex-1]
        menuOpt[currentIndex] = menuOpt[currentIndex].replace("> ","")
        currentIndex -= 1
        redrawMenu(menu)
        return currentIndex
    else:
        return currentIndex

def menuDown(currentIndex):
    global menuOpt
    if currentIndex+1 <= len(menuOpt)-1:
        menuOpt[currentIndex+1] = "> " + menuOpt[currentIndex+1]
        menuOpt[currentIndex] = menuOpt[currentIndex].replace("> ","")
        currentIndex += 1
        redrawMenu(menu)
        return currentIndex
    else:
        return currentIndex

def menuBack(parentMenu, menuWidget):
    if len(parentMenu) > 0:
        global menuOpt
        global currentMenu
        global previousMenus
        global currentIndex
        if currentMenu == "options":
            saveOptions()
        allMenus[currentMenu][currentIndex] = allMenus[currentMenu][currentIndex].replace("> ", "")
        allMenus[currentMenu][0] = "> "+allMenus[currentMenu][0]
        currentIndex = 0
        menuOpt = []
        parentMenu = allMenus[parentMenu[0]]
        for option in parentMenu:
            menuOpt.append(option)
        menuOpt[0] = "> " + menuOpt[0]
        redrawMenu(menuWidget)
        currentMenu = previousMenus[0]
        previousMenus.pop(0)

def loadOptions():
    global allMenus
    global currentColour
    global titles
    global titleChoice
    global textSpeedMult
    annoyingBugFix = []
    count = 0
    for x in allMenus["arrowkeymenu"]:
        splitted = x.split(":")
        annoyingBugFix.append(splitted[0]+": "+splitted[1]+":")
    for item in range(0,len(allMenus["options"])):
        match (count):
            case(0):
                currentItem = "false" # TODO: Change this if i make puretext a thing :l
            case(1):
                currentItem = titles[titleChoice]
            case(2):
                currentItem = currentColour
            case(3):
                currentItem = textSpeedMult
        print(("options:"+allMenus["options"][item].lower().split(": ")[0]+":").replace(">", ""))
        if ("options:"+allMenus["options"][item].lower().split(": ")[0]).replace(">", "") in allMenus["arrowkeymenu"] or ("options:"+allMenus["options"][item].lower().split(": ")[0]).replace(">", "") in annoyingBugFix:
            allMenus["options"][item] += " < "+str(currentItem)+" >"
        else:
            allMenus["options"][item] += " "+str(currentItem)
        count += 1

def saveOptions():
    global optionsJson
    options = open("options.json", "w")
    annoyingBugFix = []
    for x in allMenus["arrowkeymenu"]:
        splitted = x.split(":")
        annoyingBugFix.append(splitted[0]+": "+splitted[1]+":")
    print(annoyingBugFix)
    for option in range(0,len(allMenus["options"])):
        print(("options:"+allMenus["options"][option].lower().split(": ")[0]+":").replace(">", ""))
        if ("options:"+allMenus["options"][option].lower().split(": ")[0]+":").replace(">", "") in allMenus["arrowkeymenu"] or ("options:"+allMenus["options"][option].lower().split(": ")[0]+":").replace(">", "") in annoyingBugFix:
            optionData = allMenus["options"][option].split("< ")[1].lower()
            print(optionData)
            optionData = optionData.replace("< ", "")
            optionData = optionData.replace(" >", "")
        else:
            optionData = allMenus["options"][option].split(": ")[1].lower()
        if isinstance(optionData, int or float):
            optionData = float(optionData)
        elif isinstance(optionData.capitalize(), bool): #just for pure text option saving, others already have casting
            optionData = bool(optionData)
        else:
            optionData = str(optionData)
        optionName = allMenus["options"][option].split(":")[0].lower()
        optionName = optionName.replace(" ", "")
        optionName = optionName.replace(">", "")
        optionsJson[optionName] = optionData
    json.dump(optionsJson, options)

def enterSubMenu(menuWidget, option):
    global currentIndex
    global previousMenus
    global currentMenu
    allMenus[currentMenu][currentIndex] = allMenus[currentMenu][currentIndex].replace("> ", "")
    previousMenus.insert(0,currentMenu)
    currentMenu = option.lower()
    currentIndex = 0
    redrawMenu(menuWidget)

def redrawMenu(label):
    global menuOpt
    newText = ""
    for option in range (0,len(menuOpt)):
        if not option == len(menuOpt):
            newText += menuOpt[option] + "\n"
        else:
            newText += menuOpt[option]
    label.config(text=newText)

def selectIndex(currentIndex):
    global menuOpt
    global titleChoice
    global title
    print(f"You selected {menuOpt[currentIndex]}")
    option = menuOpt[currentIndex].replace("> ", "")
    isSubMenuTrigger = True if option.lower() in allMenus["submenutriggers"] else False
    if isSubMenuTrigger:
        menuOpt = allMenus[option.lower()]
        enterSubMenu(menu, option.lower())
    else:
        match (currentMenu):
            case ("mainmenu"):
                match (option.lower()):
                    case ("start"):
                        listener.stop()
                        ldScreen.loadIn(rootWindow, isPrologue, chrName, textSpeedMult)
                    case ("exit"):
                        rootWindow.quit()
            case ("options"):
                if "title:" in option.lower():
                    title.delete("1.0", "end")
                    allMenus["options"][1] = allMenus["options"][1].replace(titles[titleChoice], "")
                    #menuOpt[1] = menuOpt[1].replace(titles[titleChoice], "")
                    titleChoice += 1
                    if titleChoice > len(arts)-1:
                        titleChoice = 0
                    allMenus["options"][1] += titles[titleChoice]
                    #menuOpt[1] += titles[titleChoice]
                    redrawMenu(menu)
                    title.insert("1.0", arts[titleChoice])


def submitText():
    validAction, action = checkAction(currentScenario)
    if validAction:
        doAction(action)

def checkAction(scenario): #check if action is valid
    pass

def doAction(action): #do whatever action which is inputted
    pass

rootWindow = Tk()
x, y = rootWindow.winfo_screenwidth(), rootWindow.winfo_screenheight()
rootWindow.geometry("500x500")
rootWindow.config(background="black")

areaLabel = ["","","","","","","","",""] #We're going to print the ASCII image as lines because we can do delayed loading + it makes reading it easier this way
dialogueBox = [""] #same with any dialogue
dialogueText = "nothing rn"

cmdEntry = Entry(rootWindow, textvariable=">", width=30)
cmdEntry.place(x=200, y=200)

title = Text(rootWindow, wrap=NONE, font=("Courier", 8), borderwidth=0, bg="black", fg=availableColours[currentColourIndex], width=rootWindow.winfo_screenwidth(), height=rootWindow.winfo_screenheight())
title.insert("1.0", arts[titleChoice])
title.place(x=15, y=10)

menu = Label(justify=LEFT, bg="black", fg=availableColours[currentColourIndex], font=("Courier", 16))
menu.place(x=15,y=160)
redrawMenu(menu)

listener = Listener(on_press=caseInput)
listener.start()

loadOptions()
rootWindow.mainloop()