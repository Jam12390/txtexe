from tkinter import *
import time
import json
import characterClasses as chrClass


def welcome(rootWindow, entryObj, textSpeedMult, textColour, userEntry, entryIndicator):
    name = "Jam"

    def acceptInput(event=None):
        nonlocal waiting
        if waiting:
            nonlocal entryStrVar
            entryStrVar.set(entryObj.get())
            waiting = False
            entryObj.delete(0, END)

    def redrawWidgets(event=None):
        windowCanvas.configure(height=rootWindow.winfo_height() - 50)
        userEntry.place(x=20, y=rootWindow.winfo_height() - 20)
        entryIndicator.place(x=5, y=rootWindow.winfo_height() - 25)

    chrWelcomeText = [
        "Ah, a new subject.", "\n", 2,
        "Welcome to the game.", "\n", 0.5,
        "I am the Overseer of this world", "\n", 1,
        "I will be the one to record the outcome of this", "..", " experiment.", "\n", 0.5, #15
        "Before you inevitably ask like your predecessors, you do not need to or will ever know what the experiment is.", "\n", 3,
        "Moving on, seeing as I have introduced myself, I see it fit for you to do the same.", "\n", 2,
        "So subject, What is your name?", "\n", "io bound", #25
        # If a name is provided
        # If no name is provided
        "I believe you forgot to put your name,", "\n", 0.5,
        "I will give you the benefit of the doubt and allow you to put your name again.", "\n", "io bound",
        # If no name is provided again
        "...", "\n", 2,
        "Subject, a name is required to proceed with the experiment.", "\n", "io bound",
        # If no name is provided for a third time
        "If you do not wish to give yourself a name,", "\n", 2,
        "Then I will.", "\n", 1,
        "Welcome, SBJ51.", "\n", 1,
        "This does not bode well for the rest of the experiment,", "\n", 3.2,
        "However, we must move on,", "\n", 0.1,
        # Skip this line if a name was not provided at all
        ", welcome.", "\n", 1,
        "Now that you've introduced yourself,", "\n", 0.5, #58 first, 60 end
        "Let's move onto creating your vessel, or as you call them, 'characters'.", "\n", 0.5,
        "So without further ado,", "\n", 1.5,
        "kablam boom bam", "\n",
        "Choose It's Name", "\n", "io bound",
        #if no name was provided for both. defiance = 1
        "Subject.", "\n", 3,
        "I am reaching the limit of my patience", "\n", 2,
        "I cannot and will not choose for you.", "\n", 2,
        "If you cannot obey basic instructions, it is pointless to continue the experiment.", "\n", 2,
        "Therefore", "\n", 1,
        "Give", "\n", 2,
        "Your character", "\n", 2,
        "A name", "\n", "io bound",
        #if no name is provided a second time
        "eoD", ".", #98
        #if no name is provided here but was before. defiance = 0
        "If you really cannot think of a name", "\n", 1,
        "Then I will choose for you only on this occasion", "\n", 2,
        "James seems like a fitting name", "\n", 2,
        "Moving on,", "\n", 1.5,
        #else continue as normal
        ", an acceptable name.", "\n", 1,
        "Choose it's class", "\n", "output classes", "io bound",#109 start, 112 end
        #if nothing is chosen (2nd time) defiance = 1
        ", please make your character.", "\n", 2,
        "It is integral to the experiment", "\n", 1,
        "Choose a class.", "\n", "output classes", "io bound",
        #if nothing is chosen again (2nd time) defiance = 1, will go up to 2
        "Do you insist on being difficult?", "\n", 3,
        "I do not know what you get from this.", "\n", 2,
        "However I will warn you now to stop,", "\n", 1.5,
        "As you will not like what comes next if you continue to be defiant.", "\n", 2,
        "I will choose for you again", "\n", 1,
        "Your character will be a wizard." "\n", 1,
        "End of.", "\n", 1, "eoD", ".", #143
        #if nothing is chosen (1st time) defiance = 0
        "Did you forget to put something?", "\n", 1,
        "Or did you misspell?", "\n", 1,
        "Here, try again", "\n", "output classes", "io bound",
        #if nothing is chosen again (1st time) defiance up to 1
        "Alright, I will tolerate your refusal this time, but only this time", "\n", 2,
        "Your character will be a wizard.", "\n", 1, "eoD", ".",
        #move on again
        "[replace with class text]", "\n", 2,
        "Choose It's Specialty", "\n", "output subclasses", "io bound", #161 start, 164 end
        #defiance = 2
        "eoD", ".", #go to defiance ending
        #defiance = 1
        "Are you enjoying this?", "\n", 1,
        "Fine.", "\n", 1.5,
        "I will choose one more time for you.", "\n", 2,
        "Do not test my patience again.", "\n", 1,
        f"You will be a (theres defo a subclass here).", "\n", 1, "eoD", ".",#TODO: make sure the subclasses list is populated before testing, will crash otherwise {subClasses[clas][0]}
        #defiance = 0 and nothing put
        "You forgot to put something.", "\n", 1,
        "Please choose.", "\n", "output subclasses", "io bound",
        #defiance = 0 and something put
        "That's not one of the choices.", "\n", 1,
        "Or maybe you misspelled.", "\n", 0.5, #190
        "Anyway, please choose an available class", "output subclasses", "\n", "io bound",
        #something not put again and defiance = 0
        "Seeing as you cannot choose,", "\n", 1,
        "I will choose for you.", "\n", 2,
        f"You will be a (just put something here later)", "\n", 1, "eoD", ".", #201 {subClasses[clas][0]}
        #continue as normal
        ", fair enough.", "\n", 1.5,
        "Choose It's Ability", "\n", "output abilities", "io bound", #202 start, 203 end
        #defiance = 2
        ", of all the subjects I have had,", "\n", 1,
        "None have tested my patience as much as you are doing now.", "\n", 1.5,
        "If you do not want to choose,", "\n", 1,
        "Then you will recieve nothing.", "\n", 2, "eoD", ".", #player gets no ability
        #defiance = 1 - nothing put
        "Since we're at the end of this and my patience,", "\n", 0.5,
        f"You get (this doesnt work yet) as your ability.", "\n", 0.5, "eoD", ".", #{abilities[clas][0]}
        #defiance = 0 and nothing put
        "You forgot to choose,", "\n", 0.5,
        "Try again", "\n", "output abilities", "io bound",
        #defiance = 0 and incorrect ability put
        "That's not an ability.", "\n", 1,
        "Please choose an ability which you see here.", "\n", "output abilities", "io bound", "ability",
        #not chosen again
        "Why'd you- nevermind.", "\n", 0.5,
        "I don't see a point in you being indecisive so I will choose for you.", "\n", 2,
        f"Your ability is .", "\n", 0.5, "eoD", ".", #{abilities[clas][0]}
        #continue as normal
        "endChr", #227 - jesus fking christ
        ", your starter ability.", "\n", 1,
        "endChr",
        "Here's your character:", "\n", 0.5,
        f"pretend theres something here :(", "\n", 1, #incomplete but :l {playerCharacter.health} NEVERMIND IT DOESNT WORK WHY
        "Before you leave.", "\n", 2,
        "Please do take my world seriously,", "\n", 3,
        "Your actions here will have consequences.", "\n", 3,
        "And although I am merciful,", "\n", 1,
        "I do not tolerate subjects who attempt to tamper with my work.", "\n", 4,
        "Do with that information what you will.", "\n", 4,
        "Goodbye for now, ", "\n", 1,
        "And remember,", "\n", 1,
        "I'm always watching."
    ]

    name = "Jam"

    windowCanvas = Canvas(rootWindow)
    scrollBar = Scrollbar(rootWindow, orient="vertical", command=windowCanvas.yview)
    scrollArea = Frame(windowCanvas)
    scrollArea.bind(
        "<Configure>",
        lambda e: windowCanvas.configure(scrollregion=windowCanvas.bbox("all")),
    )

    windowCanvas.create_window((0, 0), window=scrollArea, anchor="nw")
    windowCanvas.configure(
        yscrollcommand=scrollBar.set,
        bg="black",
        height=rootWindow.winfo_height() - 50,
        width=rootWindow.winfo_screenwidth(),
        borderwidth=0,
        highlightthickness=0,
        relief="ridge",
    )

    rootWindow.bind("<Configure>", redrawWidgets)

    waiting = False
    entryStrVar = StringVar()

    objectIndexes = findPromptIndexes(chrWelcomeText=chrWelcomeText, name=name)
    attributeCount = 0

    defiance = 0
    userNameRefuse = 0
    nameRefuse = 0
    classRefuse = 0
    subClassRefuse = 0
    abilityRefuse = 0

    optionFile = open("characterOptions.json", "r")
    chrOptions = json.load(optionFile)
    optionFile.close()

    userName = ""
    name = ""
    clas = ""
    subClass = ""
    ability = ""

    dialogueIndex = 0

    dialogueLabel = Text(
        scrollArea,
        #justify=LEFT,
        bg="black",
        fg=textColour,
        font=("Courier", 8),
        borderwidth=0,
        width=rootWindow.winfo_width()
    )
    dialogueLabel.pack()
    currentText = ""

    windowCanvas.place(x=0, y=0)
    scrollBar.pack(side="right", fill="y")

    entryObj.bind("<Return>", acceptInput)

    for line in range(0, len(chrWelcomeText)):
        chosenOption = False
        if not dialogueIndex >= len(chrWelcomeText):
            if chrWelcomeText[dialogueIndex] == "\n" and not chosenOption:
                currentText += chrWelcomeText[dialogueIndex]
                dialogueLabel.insert("end", chrWelcomeText[dialogueIndex])
                chosenOption = True

            if (
                str(chrWelcomeText[dialogueIndex]).split(" ")[0] == "output"
                and not chosenOption
            ):
                chosenOption = True
                outputText = (
                    "Available " + chrWelcomeText[dialogueIndex].split(" ")[1] + ": "
                )
                match (chrWelcomeText[dialogueIndex].split(" ")[1]):
                    case "classes":
                        outputList = chrOptions["classes"]
                    case "subclasses":
                        outputList = chrOptions["subclasses"][clas]
                    case "abilities":
                        outputList = chrOptions["abilities"][clas]

                if not isinstance(outputList, dict):
                    for option in outputList:
                        print(option)
                        outputText += option.capitalize() + ", "
                else:
                    for ability in outputList:
                        print(ability)
                        outputText += ability.capitalize() + ","
                outputText += "\n"
                currentText += outputText
                dialogueLabel.insert("end", outputText)

            if chrWelcomeText[dialogueIndex] == ".":
                chosenOption = True  # placeholder item to fix other bug
                pass

            if chrWelcomeText[dialogueIndex] == "eoD" and not chosenOption:
                chosenOption = True
                dialogueIndex = objectIndexes["normalroute"][attributeCount] - 1

            if chrWelcomeText[dialogueIndex] == "io bound" and not chosenOption:
                chosenOption = True
                waiting = True
                entryObj.delete(0, END)
                entryObj.focus_set()
                root = entryObj.winfo_toplevel()
                root.wait_variable(entryStrVar)
                entryData = entryStrVar.get()

                match (attributeCount):
                    case 0:  # username
                        if len(entryData) != 0:
                            userName = entryData
                            attributeCount += 1
                            chrWelcomeText[
                                objectIndexes["normalroute"][attributeCount]
                            ] = (
                                userName.capitalize()
                                + chrWelcomeText[
                                    objectIndexes["normalroute"][attributeCount]
                                ]
                            )
                            dialogueIndex = (
                                objectIndexes["normalroute"][attributeCount] - 1
                            )
                            chrWelcomeText[
                                chrWelcomeText.index(", please make your character.")
                            ] = (name.capitalize() + ", please make your character.")
                            chrWelcomeText[
                                chrWelcomeText.index(
                                    ", of all the subjects I have had,"
                                )
                            ] = (
                                name.capitalize() + ", of all the subjects I have had,"
                            )
                            chrWelcomeText[
                                chrWelcomeText.index("Goodbye for now, ")
                            ] = ("Goodbye for now, " + name.capitalize() + ".")
                        else:
                            if userNameRefuse == 0:
                                dialogueIndex = (
                                    objectIndexes["defianceroute"][attributeCount] - 1
                                )
                            userNameRefuse += 1  # starts defiance for userName
                            if userNameRefuse == 3:
                                userName = "SBJ51"
                                attributeCount += 1
                                defiance += 1
                                chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount]
                                    ] = ""
                                chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount] + 1
                                    ] = ""
                                chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount] + 2
                                    ] = ""
                                chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount] + 3
                                    ] = "Now that you have a name,"
                                chrWelcomeText[
                                    chrWelcomeText.index(
                                        ", please make your character."
                                    )
                                ] = (
                                    name.capitalize() + ", please make your character."
                                )
                                chrWelcomeText[
                                    chrWelcomeText.index(
                                        ", of all the subjects I have had,"
                                    )
                                ] = (
                                    name.capitalize()
                                    + ", of all the subjects I have had,"
                                )
                                chrWelcomeText[
                                    chrWelcomeText.index("Goodbye for now, ")
                                ] = ("Goodbye for now, " + name.capitalize() + ".")
                                
                    case 1:  # chrname
                        if len(entryData) != 0:
                            name = entryData
                            attributeCount += 1
                            chrWelcomeText[
                                objectIndexes["normalroute"][attributeCount]
                            ] = (
                                name.capitalize()
                                + chrWelcomeText[
                                    objectIndexes["normalroute"][attributeCount]
                                ]
                            )
                            dialogueIndex = (
                                objectIndexes["normalroute"][attributeCount] - 1
                            )
                        else:
                            match (defiance):
                                case 1:
                                    nameRefuse += 1
                                    if nameRefuse == 2:
                                        gotoDefianceEnding(dialogueLabel=dialogueLabel)
                                        defiance += 1
                                case 0:
                                    dialogueIndex = (
                                        objectIndexes["defianceroute"][2] - 1
                                    )
                                    name = "James"
                                    defiance += 1
                                    attributeCount += 1
                                    chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount]
                                    ] = ""
                                    chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount] + 1
                                    ] = ""
                                    chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount] + 2
                                    ] = ""
                    case 2:  # class
                        if entryData.lower() in chrOptions["classes"]:
                            clas = entryData.lower()
                            attributeCount += 1
                            dialogueIndex = (
                                objectIndexes["normalroute"][attributeCount] - 1
                            )
                            match (clas):
                                case "warrior":
                                    chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount]
                                    ] = f"Warrior, the most basic choice. I hope you are a bit more interesting than the others, {name.capitalize()}"
                                case "barbarian":
                                    chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount]
                                    ] = f"Barbarian, I assume you're impatient {name.capitalize()}."
                                case "wizard":
                                    chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount]
                                    ] = f"Wizard. I hope you enjoy reading, {name.capitalize()}."
                                case _:
                                    chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount]
                                    ] = f"{clas.capitalize()}, an acceptable choice."
                        else:
                            match (defiance):
                                case 1:
                                    if classRefuse == 0:
                                        dialogueIndex = (
                                            objectIndexes["defianceroute"][3] - 1
                                        )
                                    classRefuse += 1
                                    if classRefuse == 2:
                                        defiance += 1
                                        clas = "wizard"
                                        attributeCount += 1
                                        chrWelcomeText[
                                            objectIndexes["normalroute"][attributeCount]
                                        ] = ""
                                        chrWelcomeText[
                                            objectIndexes["normalroute"][attributeCount]
                                            + 1
                                        ] = ""
                                        chrWelcomeText[
                                            objectIndexes["normalroute"][attributeCount]
                                            + 2
                                        ] = ""
                                case 0:
                                    if classRefuse == 0:
                                        dialogueIndex = (
                                            objectIndexes["defianceroute"][4] - 1
                                        )
                                    classRefuse += 1
                                    if classRefuse == 2:
                                        defiance += 1
                                        clas = "wizard"
                                        print(chrWelcomeText[
                                            objectIndexes["normalroute"][attributeCount]
                                        ])
                                        attributeCount += 1
                                        chrWelcomeText[
                                            objectIndexes["normalroute"][attributeCount]
                                        ] = ""
                                        chrWelcomeText[
                                            objectIndexes["normalroute"][attributeCount]
                                            + 1
                                        ] = ""
                                        chrWelcomeText[
                                            objectIndexes["normalroute"][attributeCount]
                                            + 2
                                        ] = ""
                    case 3:  # subclass
                        if entryData.lower() in chrOptions["subclasses"][clas]:
                            subClass = entryData.lower()
                            attributeCount += 1
                            chrWelcomeText[
                                objectIndexes["normalroute"][attributeCount]
                            ] = (
                                subClass.capitalize()
                                + chrWelcomeText[
                                    objectIndexes["normalroute"][attributeCount]
                                ]
                            )
                            dialogueIndex = (
                                objectIndexes["normalroute"][attributeCount] - 1
                            )
                        else:
                            match (defiance):
                                case 2:
                                    defiance += 1
                                    gotoDefianceEnding(dialogueLabel=dialogueLabel)
                                case 1:
                                    if subClassRefuse == 0:
                                        dialogueIndex = (
                                            objectIndexes["defianceroute"][5] - 1
                                        )
                                    subClassRefuse += 1
                                    subClass = chrOptions["subclasses"][clas.lower()][0]
                                    chrWelcomeText[
                                        objectIndexes["normalroute"][attributeCount]
                                    ] = (
                                        subClass.capitalize()
                                        + chrWelcomeText[
                                            objectIndexes["normalroute"][attributeCount]
                                        ]
                                    )
                                    attributeCount += 1
                                    defiance += 1
                                    chrWelcomeText[objectIndexes["normalroute"][attributeCount]] = ""
                                    chrWelcomeText[objectIndexes["normalroute"][attributeCount]+1] = "" #something went wrong here, just run the code up to this point
                                    chrWelcomeText[objectIndexes["normalroute"][attributeCount]+2] = ""
                                case 0:
                                    if subClassRefuse == 0:
                                        if len(entryData) == 0:
                                            dialogueIndex = (
                                                objectIndexes["defianceroute"][6] - 1
                                            )
                                        else:
                                            dialogueIndex = (
                                                objectIndexes["defianceroute"][7] - 1
                                            )
                                    subClassRefuse += 1
                                    if subClassRefuse == 2:
                                        dialogueIndex = (
                                            objectIndexes["defianceroute"][8] - 1
                                        )
                                        attributeCount += 1
                                        subClass = chrOptions["subclasses"][
                                            clas.lower()
                                        ][0]
                                        chrWelcomeText[
                                            objectIndexes["normalroute"][attributeCount]
                                        ] = (
                                            subClass.capitalize()
                                            + chrWelcomeText[
                                                objectIndexes["normalroute"][
                                                    attributeCount
                                                ]
                                            ]
                                        )
                                        defiance += 1
                    case 4:  # abilities AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                        if entryData.lower() in chrOptions["abilities"][clas]:
                            ability = entryData.lower()
                            attributeCount += 1
                            chrWelcomeText[
                                objectIndexes["normalroute"][attributeCount]
                            ] = (
                                ability.capitalize()
                                + chrWelcomeText[
                                    objectIndexes["normalroute"][attributeCount]
                                ]
                            )
                            dialogueIndex = (
                                objectIndexes["normalroute"][attributeCount] - 1
                            )
                        else:
                            match (defiance):  # same here
                                case 2:
                                    dialogueIndex = (
                                        objectIndexes["defianceroute"][9] - 1
                                    )
                                    ability = ""
                                    defiance += 1
                                    attributeCount += 1
                                case 1:
                                    dialogueIndex = (
                                        objectIndexes["defianceroute"][10] - 1
                                    )
                                    ability = chrOptions["abilities"][clas.lower()][0]
                                    defiance += 1
                                    attributeCount += 1
                                case 0:
                                    if abilityRefuse == 0:
                                        if len(entryData) == 0:
                                            dialogueIndex = (
                                                objectIndexes["defianceroute"][11] - 1
                                            )
                                        else:
                                            dialogueIndex = (
                                                objectIndexes["defianceroute"][12] - 1
                                            )
                                    abilityRefuse += 1
                                    if abilityRefuse == 2:
                                        dialogueIndex = (
                                            objectIndexes["defianceroute"][13] - 1
                                        )
                                        ability = chrOptions["abilities"][clas.lower()][
                                            0
                                        ]
                                        defiance += 1
                                        attributeCount += 1
            if isinstance(chrWelcomeText[dialogueIndex], int) or isinstance(
                chrWelcomeText[dialogueIndex], float
            ):
                chosenOption = True
                time.sleep(float(chrWelcomeText[dialogueIndex]) / textSpeedMult)

            if ".." in str(chrWelcomeText[dialogueIndex]):
                chosenOption = True
                for dot in chrWelcomeText[dialogueIndex]:
                    currentText += dot
                    dialogueLabel.insert("end", dot)
                    time.sleep(0.75)

            if chrWelcomeText[dialogueIndex] == "endChr" and not chosenOption:
                chosenOption = True
                print(
                    f"username: {userName}\nname: {name}\nclass: {clas}\nsubclass: {subClass}\nability: {ability}"
                )
                playerCharacter = createCharacter(
                    name=name, clas=clas, subClass=subClass, ability=ability
                )
                print("breakpoint here to check character values")

            if not chosenOption:
                chosenOption = True
                for letter in range(0, len(chrWelcomeText[dialogueIndex])):
                    if chrWelcomeText[dialogueIndex][letter] == "," and letter != len(
                        chrWelcomeText[dialogueIndex]
                    ):
                        waitTime = 0.5
                    else:
                        waitTime = 0.01
                    currentText += chrWelcomeText[dialogueIndex][letter]
                    dialogueLabel.insert("end", chrWelcomeText[dialogueIndex][letter])
                    time.sleep(waitTime / textSpeedMult)
            dialogueIndex += 1
            windowCanvas.yview_moveto(1)


def gotoDefianceEnding(dialogueLabel):
    dialogueLabel.config(text="angy")
    input("this works :D")


def findPromptIndexes(chrWelcomeText, name):
    objects = {
        "normalroute": [
            "So subject, What is your name?",
            ", welcome.",
            ", an acceptable name.",
            "[replace with class text]",
            ", fair enough.",
            ", your starter ability.",
        ],
        "defianceroute": [
            # NOTE: Each of these is the start of each pathway, since each defiance path is sequential, we don't need the other indexes for the continuations
            # until later paths because there are separate dialogue options for if something was put or nothing was put
            "I believe you forgot to put your name,",  # refusing to enter username
            "Subject.",  # defiance = 1 and refusal to enter character name
            "If you really cannot think of a name",  # defiance = 0 and refusal to enter character name
            ", please make your character.",  # defiance = 1 and refusal to enter class
            "Did you forget to put something?",  # defiance = 0 and refusal to enter class
            "Are you enjoying this?",  # defiance = 1 and refusal to enter subclass
            "You forgot to put something.",  # defiance = 0, not entered subclass and nothing put
            "That's not one of the choices.",  # defiance = 0, not entered correct subclass but something put
            "Seeing as you cannot choose,",  # defiance = 0 and invalid subclass entered again
            ", of all the subjects I have had,",  # defiance = 2 and nothing put for ability
            "Since we're at the end of this and my patience,",  # defiance = 1 and nothing put for ability
            "You forgot to choose,",  # defiance = 0 and nothing put for ability
            "That's not an ability.",  # defiance = 0 and something put for ability
            "Why'd you- nevermind.",  # defiance = 0 and invalid ability entered again
        ],
    }
    objectIndexes = {"normalroute": [], "defianceroute": []}
    for item in objects["normalroute"]:
        objectIndexes["normalroute"].append(chrWelcomeText.index(item))
    for item in objects["defianceroute"]:
        objectIndexes["defianceroute"].append(chrWelcomeText.index(item))
    return objectIndexes


def getAttributes(clas, subClass):
    match (clas.lower()):
        case "warrior":
            health, strength, intelligence, defense, charisma = 100, 12, 8, 10, 11
            weak = "none"
            advant = "physical"
        case "barbarian":
            health, strength, intelligence, defense, charisma = 150, 15, 6, 7, 2
            weak = "magic"
            advant = "physical"
        case "wizard":
            health, strength, intelligence, defense, charisma = 80, 8, 15, 6, 5
            weak = "physical"
            advant = "magic"
    match (subClass.lower()):
        case "paladin":
            health += 10
            defense += 1
        case "knight":
            health += 20
            defense += 2
            strength -= 1
            charisma += 1
            intelligence -= 1
        case "berserker":
            health += 25
            strength += 3
            intelligence = 0
            charisma -= 1
            defense -= 3
        case "tank":
            health += 40
            charisma -= 1
            defense += 5
        case "mage":
            intelligence += 1
            charisma -= 1
            strength -= 1
        case "evil wizard":
            strength += 2
            intelligence += 1
            charisma -= 3
            defense -= 2
        case _:
            pass
    mana = round(100 * (intelligence / 10))
    return health, mana, strength, intelligence, defense, charisma, weak, advant


def createCharacter(name, clas, subClass, ability):
    health, mana, strength, intelligence, defense, charisma, weak, advant = (
        getAttributes(clas, subClass)
    )
    return chrClass.Character(
        name=name,
        health=health,
        clas=clas,
        subClass=subClass,
        mana=mana,
        advant=advant,
        weak=weak,
        strength=strength,
        intelligence=intelligence,
        defense=defense,
        charisma=charisma,
        abilities=[ability],
        lvl=1,
        xp=0,
    )
