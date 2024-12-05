from tkinter import *
import time
import json

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
    ]


def welcome():
    pass