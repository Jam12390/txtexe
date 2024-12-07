from tkinter import *
from pynput.keyboard import Key, Listener
import time
import json
import loadin as ldScreen

currentIndex = 0
currentScenario = "menu"

with open("menus.json", "r") as file:
    menus = json.load(file)

menuOpt = menus["mainmenu"]
inMenu = True

isPrologue = True
chrName = "Test"

with open("menus.json", "r") as f:
    allMenus = json.load(f.read())
    f.close()

def caseInput(key): #any time a ui input is pressed
    global currentIndex
    match (key):
        case (Key.esc):
            if inMenu:
                menuBack() #TODO: add arguments for this so it doesnt fucking break
        case (Key.up):
            if inMenu:
                currentIndex = menuUp(currentIndex)
        case (Key.down):
            if inMenu:
                currentIndex = menuDown(currentIndex)
        case (Key.enter):
            if inMenu:
                selectIndex(currentIndex)
            else:
                submitText()

def menuUp(currentIndex):
    if not currentIndex-1 < 0:
        menuOpt[currentIndex-1] = "> " + menuOpt[currentIndex-1]
        menuOpt[currentIndex] = menuOpt[currentIndex].replace("> ","")
        currentIndex -= 1
        redrawMenu(menu)
        return currentIndex
    else:
        return currentIndex

def menuDown(currentIndex):
    if currentIndex+1 <= len(menuOpt)-1:
        menuOpt[currentIndex+1] = "> " + menuOpt[currentIndex+1]
        menuOpt[currentIndex] = menuOpt[currentIndex].replace("> ","")
        currentIndex += 1
        redrawMenu(menu)
        return currentIndex
    else:
        return currentIndex

def menuBack(menuPresence, parentMenu, menuWidget):
    if menuPresence:
        global menuOpt
        menuOpt = []
        parentMenu = allMenus[parentMenu]
        for option in parentMenu:
            menuOpt.append(option)
        menuOpt[0] = "> " + menuOpt[0]
        redrawMenu(menuWidget)

def enterSubMenu(selectedMenu, menuWidget):
    global menuOpt
    menuOpt = []
    subMenu = json.load(f.read())[selectedMenu]
    for option in subMenu:
        menuOpt.append(option)
    menuOpt[0] = "> " + menuOpt[0]
    redrawMenu(menuWidget)

def redrawMenu(label):
    newText = ""
    for option in range (0,len(menuOpt)):
        if not option == len(menuOpt):
            newText += menuOpt[option] + "\n"
        else:
            newText += menuOpt[option]
    label.config(text=newText)

def selectIndex(currentIndex):
    print(f"You selected {menuOpt[currentIndex]}")
    isSubMenuTrigger = True if option.lower() in allMenus["submenutriggers"] else False #TODO: continue submenu entering logic here
    option = menuOpt[currentIndex].replace("> ", "")
    if option == "Start":
        listener.stop()
        ldScreen.loadIn(rootWindow, isPrologue, chrName) #TODO: add a check for swapping menus in this case entering a submenu

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


areaLabel = ["","","","","","","","",""] #We're going to print the ASCII image as lines because we can do delayed loading + it makes reading it easier this way
dialogueBox = [""] #same with any dialogue
dialogueText = "nothing rn"

cmdEntry = Entry(rootWindow, textvariable=">", width=30)
cmdEntry.pack(pady=20)

menu = Label(justify=LEFT)
menu.pack()
redrawMenu(menu)


listener = Listener(on_press=caseInput)
listener.start()

rootWindow.mainloop()