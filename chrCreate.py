from tkinter import *
import time
import json
import random

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