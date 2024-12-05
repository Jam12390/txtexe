import time
from tkinter import *

def loadIn(frame, isPrologue, chrName):
    clearLabels(frame)
    loadScreen(frame, isPrologue, chrName)

def clearLabels(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def loadScreen(frame, isPrologue, chrName):
    currentText = ""
    loadingText = Label(frame, justify=LEFT)
    loadingText.pack()
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
                    "Connection Complete.", 0.2
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
        print(line)
        if line == "\n":
            currentText += line
        else:
            if isinstance(line, float) or isinstance(line, int):
                time.sleep(float(line))
            else:
                for letter in line:
                    currentText += letter
                    loadingText.config(text=currentText)
                    time.sleep(0.01)