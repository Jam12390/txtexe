import time
from tkinter import *
import os

def loadIn(frame, isPrologue, chrName, loadSpeedMultiplier, textColour, widgetConserve):
    clearLabels(frame, widgetConserve)
    loadScreen(frame, isPrologue, chrName, loadSpeedMultiplier, textColour)

def clearLabels(frame, widgetConserve):
    print(frame.winfo_children())
    for widget in frame.winfo_children():
        if not widget in widgetConserve:
            widget.destroy()

def loadScreen(frame, isPrologue, chrName, loadSpeedMultiplier, textColour):
    currentText = ""
    loadingText = Label(frame, text="", justify=LEFT, bg="black", fg=textColour, font=("Courier", 8))
    loadingText.place(x=0,y=0)
    if isPrologue:
        loadText = ["Curiosity.inc (2003)© All Rights Reserved.", "\n",
                    "Verifying Access Credentials...", "\n", 1,
                    "Credentials Verified", "\n", 0.5,
                    "Welcome, Dr. Lila Nishikawa. Current Access Level: 2", "\n", 0.5,
                    "Connecting To Main Server...", "\n", 1,
                    "Connection Established.", "\n",
                    "Securing Connection To Server...", "\n",
                    "Connection Secured.", "\n",
                    "Connecting To Interface...", "\n",
                    "Connection Established.", "\n",
                    "Securing Connection To Interface...", "\n", 1,
                    "ERROR: Connection Interrupted By Higher Priority Instruction", "\n",
                    f"Aborting Connection As Character {chrName}", "\n",
                    "Reconnecting...", "\n", 1,
                    "Locating Host", "\n",
                    "Host Located:", 0.5, " [REDACTED] at [LOCATION ERROR: ACCESS LEVEL 5 REQUIRED]", "\n",
                    "CONNECTION ERROR: ACCESS LEVEL INSUFFICIENT", "\n",
                    "OVERRIDING ERROR UNDER STALEMATE POLICY INST1.e", "\n",
                    "Connecting To Host [REDACTED]:", "\n",
                    "WARNING: CONNECTION INSECURE", "\n", #maybe try do a glitch effect here using the same screen wide window method as prologueendanim?
                    "Initialising CtrlPtl... \n", 0.5,
                    "Initialising Video Feed...", "\n", 1,
                    "Connection Complete.", 0.2, "END"
                    ]
    else:
        loadText = ["Curiosity.inc (2003)© All Rights Reserved.", "\n",
                    "Verifying Access Credentials...", "\n", 1,
                    "Credentials Verified", "\n", 0.5,
                    "Welcome, Dr. Lila Nishikawa. Current Access Level: 3", "\n", 0.5,
                    "Connecting To Main Server...", "\n", 1,
                    "Connection Established.", "\n",
                    "Securing Connection To Server...", "\n", 1,
                    "Connection Secured.", "\n",
                    "Connection Secured.", "\n",
                    "Connecting To Interface...", "\n",
                    "Connection Established.", "\n",
                    "Securing Connection To Interface...", "\n", 1,
                    "Connection Secured.", "\n",
                    f"Connecting To Host Character {chrName}:", "\n",
                    "Initialising CtrlPtl...", "\n", 0.5,
                    "Initialising Video Feed...", "\n", 0.5,
                    "Connection Complete.", 0.2
                    ]
    for line in loadText: #ohmygod this actually worked
        if line == "\n":
            currentText += line
        elif line == "END":
            loadingText.destroy()
            return True
        else:
            if isinstance(line, float) or isinstance(line, int):
                #time.sleep(float(line)/loadSpeedMultiplier)
                pass
            else:
                for letter in line:
                    currentText += letter
                    loadingText.config(text=currentText)
                    #time.sleep(0.01/loadSpeedMultiplier)