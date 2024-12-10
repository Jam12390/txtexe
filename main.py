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

menuOpt = allMenus["mainmenu"]
currentMenu = "mainmenu"
inMenu = True

isPrologue = True
chrName = "Test"
previousMenus = []

availableColours = ["Green", "White", "Pink", "Blue", "Cyan", "Purple"]
currentColourIndex = 0
currentColour = availableColours[currentColourIndex]

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
titleChoice = 0
titles = ["TXTEXE", "TEXET"]

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
        currentIndex = 0
        menuOpt = []
        parentMenu = allMenus[parentMenu[0]]
        for option in parentMenu:
            menuOpt.append(option)
        menuOpt[0] = "> " + menuOpt[0]
        redrawMenu(menuWidget)
        currentMenu = previousMenus[0]
        previousMenus.pop(0)

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
    isSubMenuTrigger = True if option.lower() in allMenus["submenutriggers"] else False #TODO: continue submenu entering logic here
    if isSubMenuTrigger:
        menuOpt = allMenus[option.lower()]
        enterSubMenu(menu, option.lower())
    else:
        match (currentMenu):
            case ("mainmenu"):
                match (option.lower()):
                    case ("start"):
                        listener.stop()
                        ldScreen.loadIn(rootWindow, isPrologue, chrName) #TODO: add a check for swapping menus in this case entering a submenu
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

rootWindow.mainloop()