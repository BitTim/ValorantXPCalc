from vars import *
from tkinter import messagebox
import os
import json

defaultSettings = {
    "bufferDays": DEFAULT_BUFFER_DAYS,
    "useHistoryColors": DEFAULT_USE_HISTORY_COLORS,
    "ignoreInactiveDays": DEFAULT_IGNORE_INACTIVE_DAYS,
    "winBackground": DEFAULT_WIN_BG_COLOR,
    "winForeground": DEFAULT_WIN_FG_COLOR,
    "lossBackground": DEFAULT_LOSS_BG_COLOR,
    "lossForeground": DEFAULT_LOSS_FG_COLOR,
    "drawBackground": DEFAULT_DRAW_BG_COLOR,
    "drawForeground": DEFAULT_DRAW_FG_COLOR,
    "noneBackground": DEFAULT_NONE_BG_COLOR,
    "noneForeground": DEFAULT_NONE_FG_COLOR,
    "selectedBackground": DEFAULT_SELECTED_BG_COLOR,
    "selectedForeground": DEFAULT_SELECTED_FG_COLOR
}

def initSettings():
    saveSettings(defaultSettings)

def loadSettings():
    if not os.path.exists(SETTINGS_PATH):
        initSettings()
    
    with open(SETTINGS_PATH, "r") as f:
        settings = json.loads(f.read())
    
    sK = list(settings.keys())
    dsK = list(defaultSettings.keys())
    missingSettings = list(set(dsK) - set(sK))
    
    for m in missingSettings:
        settings[m] = defaultSettings[m]
        saveSettings(settings)

    return settings
    
def saveSettings(settings):
    with open(SETTINGS_PATH, "w") as f:
        f.write(json.dumps(settings, indent = 4, separators=(',', ': ')))

def checkValidSettings(settings):
    try:
        int(settings["bufferDays"])
    except:
        messagebox.showerror("Invalid Input", "Buffer Days must be numeric")
        return False
    
    settings["bufferDays"] = int(settings["bufferDays"])
    if settings["bufferDays"] < 0:
        messagebox.showerror("Invalid Input", "Buffer Days can not be negative")
        return False

    return True