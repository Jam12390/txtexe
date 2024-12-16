from tkinter import *
from tkinter import ttk
from pynput.keyboard import Key, Listener
import time
import json
import loadin as ldScreen
import chrCreate as CC

currentIndex = 0
currentScenario = "menu"

#loading json files
menuFile = open("menus.json", "r")
allMenus = json.load(menuFile)
menuFile.close()

options = open("options.json", "r")
optionsJson = json.load(options)
options.close()

menuOpt = allMenus["mainmenu"] #menuOpt will store all menu options of the current menu and will be updated on any menu change
currentMenu = "mainmenu" #we'll always start at the main menu unless i want pain
inMenu = True #this lets us handle inputs which can have multiple effects which are different inside and outside of menus

isPrologue = True #we'll change this later if and when more chapters are made
chrName = "Test" #temp name for testing (who could've seen that coming)
previousMenus = [] #using an array here in case of future sub-submenus, essentially storing the menu pathway so we can backtrack

availableColours = ["Green", "White", "Pink", "Blue", "Cyan", "Purple"] #we'll cycle through this when changing colours
currentColourIndex = int(availableColours.index(optionsJson["textcolour"].capitalize())) #locating the saved colour stored in options.json and loading the index
currentColour = availableColours[currentColourIndex]

textSpeedMult = float(optionsJson["textspeed"])

#this took way too long
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

titles = ["TXTEXE", "TEXET"] #store the names of the title since we WILL NOT SEARCH FOR ASCII ART JAMES
titleChoice = int(titles.index(optionsJson["title"].upper())) #loading saved title choice from options.json

def caseInput(key): #handling any input recieved from listener
    if rootWindow.focus_displayof() and not rootWindow.focus_displayof() == userEntry: #checking that the window is 1. in focus and 2. the user isn't typing in any entry box
        global currentIndex
        global previousMenus
        match (key):
            case (Key.esc):
                if inMenu:
                    menuBack(previousMenus, menu)
            case (Key.up):
                if inMenu:
                    menuUp()
            case (Key.down):
                if inMenu:
                    menuDown()
            case (Key.left):
                if inMenu:
                    #optionToSearch is purely for readability - it: Gets the current option being selected and splits it into 2 parts, the option name (index 0) and the option choice (index 1),
                    #choosing the option name to search in arrowkeymenu.
                    #We then remove the marker for the line "> " as this isn't present in the json and not replacing it would lead to a logic error
                    optionToSearch = menuOpt[currentIndex].split(":")[0]
                    optionToSearch = optionToSearch.replace("> ", "")
                    #We then create the string to be searched in allMenus in the form parentMenu:menuOption:
                    #an example string would be options:text colour:
                    #We do this to just make sure that any future arrow key menus don't overlap with previously defined ones
                    if str(currentMenu.lower()+":"+optionToSearch.lower()+":") in allMenus["arrowkeymenu"]:
                        findArrowMenu(optionToSearch.lower()+":", "left")
            case (Key.right):
                if inMenu:
                    optionToSearch = menuOpt[currentIndex].split(":")[0]
                    optionToSearch = optionToSearch.replace("> ", "")
                    if str(currentMenu.lower()+":"+optionToSearch.lower()+":") in allMenus["arrowkeymenu"]:
                        findArrowMenu(optionToSearch.lower()+":", "right")
            case (Key.enter):
                if inMenu:
                    selectIndex(currentIndex) #selects the index if the player is in a menu
                else:
                    submitText() #attempts to submit text
    elif key == Key.esc and rootWindow.focus_displayof() == userEntry: #this removes focus from the entryWidget if esc is pressed
        focusRemove.focus_set()

def findArrowMenu(menu, direction):
    match (menu): #calling the appropriate procedure with the direction of movement
        case("text colour:"):
            textColourSwap(direction)
        case("text speed:"):
            changeTextSpeed(direction)

def changeTextSpeed(direction):
    global textSpeedMult
    if direction.lower() == "left":
        textSpeedMult -= 0.1
        if textSpeedMult < 0.5: #ensures that the new text speed isn't below the minimum speed
            textSpeedMult = 0.5
    else:
        textSpeedMult += 0.1 #same if it's too large
        if textSpeedMult > 4:
            textSpeedMult = 4
    textSpeedMult = round(textSpeedMult, 1) #fixes the floating point error caused by this
    menuOpt[currentIndex] = menuOpt[currentIndex].split(":")[0] + ":" + " < " + str(textSpeedMult) + " >" #updating the label at currentIndex to reflect the new chosen option
    allMenus[currentMenu][currentIndex] = menuOpt[currentIndex].split(":")[0]+":"+" < "+str(textSpeedMult)+" >" #Updating the value in allMenus to save the updated value when the menu is exited
    redrawMenu(menu) #update display

def textColourSwap(direction):
    global currentColourIndex
    global currentColour #these need to be global otherwise the colour isn't changed everywhere in the game
    if direction.lower() == "left":
        currentColourIndex -= 1
        if currentColourIndex < 0: #range check - min
            currentColourIndex = len(availableColours)-1 #sets it to the final index of availableColours if the index becomes too low
    else:
        currentColourIndex += 1
        if currentColourIndex > len(availableColours)-1: #range check - max
            currentColourIndex = 0
    currentColour = availableColours[currentColourIndex].lower() #updating currentColour
    #updating all the label colours to reflect new colour choice - NOTE: there may be a more efficient way to do this - groups?
    menu.config(fg=currentColour)
    title.config(fg=currentColour)
    entryIndicator.config(fg=currentColour)
    userEntry.config(fg=currentColour)
    #updating the relevant list items to display the new choice
    newChoice = " < "+currentColour.capitalize()+" >"
    menuOpt[currentIndex] = menuOpt[currentIndex].split(":")[0] + ":" + newChoice
    allMenus[currentMenu][currentIndex] = menuOpt[currentIndex].split(":")[0] + ":" + newChoice #making sure that the menu choice is saved across menus
    redrawMenu(menu) #update display


def menuUp():
    global menuOpt
    global currentIndex
    if not currentIndex-1 < 0: #checking if there is a menu option above
        menuOpt[currentIndex-1] = "> " + menuOpt[currentIndex-1] #updating cursor position
        menuOpt[currentIndex] = menuOpt[currentIndex].replace("> ","")
        currentIndex -= 1
        redrawMenu(menu) #update display

def menuDown():
    global menuOpt
    global currentIndex
    if currentIndex+1 <= len(menuOpt)-1: #checking if the user is not at the end of the menu
        menuOpt[currentIndex+1] = "> " + menuOpt[currentIndex+1] #same as menuUp but in opposite direction
        menuOpt[currentIndex] = menuOpt[currentIndex].replace("> ","")
        currentIndex += 1
        redrawMenu(menu) #update display

def menuBack(parentMenu, menuWidget):
    if len(parentMenu) > 0: #checking if there is a menu to return to
        global menuOpt
        global currentMenu
        global previousMenus
        global currentIndex
        if currentMenu == "options": #save options if exiting options menu
            saveOptions()
        allMenus[currentMenu][currentIndex] = allMenus[currentMenu][currentIndex].replace("> ", "") #resetting cursor position
        allMenus[currentMenu][0] = "> "+allMenus[currentMenu][0]
        currentIndex = 0
        menuOpt = [] #resetting menuOpt to prepare for new options
        parentMenu = allMenus[parentMenu[0]]
        for option in parentMenu:
            menuOpt.append(option) #repopulating the menuOpt list with the parentMenu's options
        menuOpt[0] = "> " + menuOpt[0] #reset cursor
        redrawMenu(menuWidget) #update display
        currentMenu = previousMenus[0]
        previousMenus.pop(0) #remove the menu which has been travelled to

def loadOptions():
    global allMenus #globals to modify variable data outside of procedure
    global currentColour
    global titles
    global titleChoice
    global textSpeedMult
    annoyingBugFix = [] #we'll need this later to fix an annoying bug
    count = 0
    for x in allMenus["arrowkeymenu"]:
        #NOTE: For some ungodly reason the option at the currently selected index will always have an extra space
        #this cannot be replaced therefore we have a separate list with 1 extra space in between parentMenu and optionName to also check
        splitted = x.split(":")
        annoyingBugFix.append(splitted[0]+": "+splitted[1]+":")
    for item in range(0,len(allMenus["options"])):
        match (count): #TODO: please change this to be easily modifiable by potentially dynamically changing variables from a list
            case(0):
                currentItem = "false"
            case(1):
                currentItem = titles[titleChoice]
            case(2):
                currentItem = currentColour
            case(3):
                currentItem = textSpeedMult
        #iterate through all options in order to check if it is part of arrowkeymenu as it will have to be loaded differently
        optionToSearch = "options:" + allMenus["options"][item].lower().split(": ")[0]
        optionToSearch = optionToSearch.replace("> ", "") #remove the cursor if it's there
        if optionToSearch in allMenus["arrowkeymenu"] or optionToSearch in annoyingBugFix:
            allMenus["options"][item] += " < "+str(currentItem)+" >" #arrowkeymenu: load the label with the arrowkeymenu structure: OptionName: < {savedOption} >
        else:
            allMenus["options"][item] += " "+str(currentItem) #not arrowkeymenu: load the label as just optionName: {savedOption}
        count += 1

def saveOptions(): #TODO: if the player is currently in the options menu and chooses to close the game, prompt them that they have unsaved changes
    global optionsJson #to be updated
    options = open("options.json", "w")
    annoyingBugFix = []
    for x in allMenus["arrowkeymenu"]: #populate annoyingBugFix
        splitted = x.split(":")
        annoyingBugFix.append(splitted[0]+": "+splitted[1]+":")
    print(annoyingBugFix)
    for option in range(0,len(allMenus["options"])):
        optionToSearch = "options:" + allMenus["options"][option].lower().split(": ")[0]
        optionToSearch = optionToSearch.replace("> ", "") #remove the cursor if it's there
        if optionToSearch in allMenus["arrowkeymenu"] or optionToSearch in annoyingBugFix:
            optionData = allMenus["options"][option].split("< ")[1].lower() #arrowkeymenu: split the string containing the optionName and optionChoice at "< " in optionName: < optionChoice >, selecting the final index
            print(optionData)
            optionData = optionData.replace("< ", "") #making sure arrows don't remain
            optionData = optionData.replace(" >", "")
        else:
            optionData = allMenus["options"][option].split(": ")[1].lower() #not arrowkeymenu: just split it at ": " in optionName: optionChoice, leaving just optionChoice
        if isinstance(optionData, int or float): #ensuring options are saved correctly
            optionData = float(optionData)
        elif isinstance(optionData.capitalize(), bool):
            optionData = bool(optionData)
        else:
            optionData = str(optionData)
        optionName = allMenus["options"][option].split(":")[0].lower() #isolating optionName
        optionName = optionName.replace(" ", "")
        optionName = optionName.replace(">", "")
        optionsJson[optionName] = optionData #update the relevant option in optionJson
    json.dump(optionsJson, options) #rewrite json to file
    options.close()

def enterSubMenu(menuWidget, option):
    global currentIndex
    global previousMenus
    global currentMenu
    allMenus[currentMenu][currentIndex] = allMenus[currentMenu][currentIndex].replace("> ", "") #remove the cursor at the current position
    previousMenus.insert(0,currentMenu) #add the current menu to previousMenus at position 0 to enable backtracking later
    currentMenu = option.lower() #updating currentMenu to new current menu
    currentIndex = 0 
    redrawMenu(menuWidget) #update display

def redrawMenu(label):
    global menuOpt
    newText = "" #this is what the menu label's text will be updated to
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
    global inMenu
    global character
    global textSpeedMult
    option = menuOpt[currentIndex].replace("> ", "") #remove the cursor
    isSubMenuTrigger = True if option.lower() in allMenus["submenutriggers"] else False
    if isSubMenuTrigger:
        menuOpt = allMenus[option.lower()] #process for entering a submenu
        enterSubMenu(menu, option.lower())
    else:
        match (currentMenu): #the match case here is to find the current menu and choose the relevant option accordingly
            case ("mainmenu"):
                match (option.lower()):
                    case ("start"):
                        listener.stop()
                        inMenu = False
                        userEntry.place(x=20,y=rootWindow.winfo_height()-20) #make the userEntry visible
                        entryIndicator.place(x=5,y=rootWindow.winfo_height()-25)
                        ldScreen.loadIn(rootWindow, isPrologue, chrName, textSpeedMult, textColour=currentColour, widgetConserve=widgetConserve) #loading screen
                        character = CC.welcome(rootWindow=rootWindow, entryObj=userEntry, textSpeedMult=textSpeedMult, textColour=currentColour, userEntry=userEntry, entryIndicator=entryIndicator) #procedure for creating a character
                    case ("exit"):
                        rootWindow.quit()
            case ("options"):
                if "title:" in option.lower():
                    title.delete("1.0", "end")
                    allMenus["options"][1] = allMenus["options"][1].replace(titles[titleChoice], "") #replacing the title choice with the next one
                    titleChoice += 1
                    if titleChoice > len(arts)-1: #range check
                        titleChoice = 0
                    allMenus["options"][1] += titles[titleChoice] #update allmenus to represent new value
                    redrawMenu(menu) #update display
                    title.insert("1.0", arts[titleChoice]) #add new ASCII art


def submitText(): #this is unfinished
    validAction, action = checkAction(currentScenario)
    if validAction:
        doAction(action)

def checkAction(scenario): #check if action is valid - old
    pass

def doAction(action): #do whatever action which is inputted - old
    pass

rootWindow = Tk()
x, y = rootWindow.winfo_screenwidth(), rootWindow.winfo_screenheight()
rootWindow.geometry("1000x500")
rootWindow.config(background="black")

title = Text(rootWindow, wrap=NONE, font=("Courier", 8), borderwidth=0, bg="black", fg=availableColours[currentColourIndex], width=rootWindow.winfo_screenwidth(), height=rootWindow.winfo_screenheight())
title.insert("1.0", arts[titleChoice])
title.place(x=15, y=10)

entryPosx, entryPosy = 20, 480

entryIndicator = Label(rootWindow, font=("Courier", 15), fg=currentColour, bg="black", text="> ")
userEntry = Entry(rootWindow, width=150, bg="black", fg=currentColour, insertwidth=6, insertbackground="white", borderwidth=0, font=("Courier", 10))

focusRemove = Label(text="wow you found me :)", fg="white")
focusRemove.place(x=10000, y=0)

widgetConserve = [entryIndicator, userEntry, focusRemove] #any widget which shouldn't be deleted goes in here

menu = Label(justify=LEFT, bg="black", fg=availableColours[currentColourIndex], font=("Courier", 16))
menu.place(x=15,y=160)
redrawMenu(menu)

listener = Listener(on_press=caseInput)
listener.start()

loadOptions()
rootWindow.mainloop()