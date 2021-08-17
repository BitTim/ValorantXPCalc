from sys import version
from tkinter import *
from tkinter import messagebox
import os
import requests
from . import changelogDiag, downloadDiag, warningDiag, legacy
from vars import *
from tokenString import *
import json
import time
from vextrackLib import settings

root = Tk()
root.withdraw()

def downloadNewVersion(versionString, softwareName, legacyMode, tag):
    os.system("taskkill /f /im " + softwareName + ".exe")

    with open(softwareName + ".exe", 'rb') as f:
        oldExec = f.read()
    
    with open(softwareName + ".exe.bak", 'wb') as f:
        f.write(oldExec)

    if not os.path.exists("VexTrack.png"):
        r = requests.get("https://github.com/" + GITHUB_USER + "/" + GITHUB_REPO + "/releases/download/util/VexTrack.png")
    
        with open("VexTrack.png", "wb") as f:
            f.write(r.content)

    url = "https://github.com/" + GITHUB_USER + "/" + GITHUB_REPO + "/releases/download/" + tag + "/" + softwareName + ".exe"
    r = requests.get(url, stream=True)

    downDiag = downloadDiag.DownloadDiag(root, "Downloading " + softwareName + " " + versionString)
    while downDiag == None: pass

    with open(softwareName + ".exe", 'wb') as f:
        startTime = time.mktime(time.localtime())
        downloaded = 0
        total = int(r.headers.get('content-length'))

        for chunk in r.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
            if chunk:
                downloaded += len(chunk)
                f.write(chunk)
                cTime = time.mktime(time.localtime())

                downDiag.updateValues(downloaded, total, 0 if cTime == startTime else round(downloaded / (cTime - startTime), 2))
    
    failed = False
    with open(softwareName + ".exe", 'r') as f:
        try:
            if f.read() == "Not Found": failed = True
        except:
            failed = False

    if failed:
        messagebox.showerror("Update Failed", "Update of " + softwareName + " failed. Reverting to previous version")

        with open(softwareName + ".exe.bak", "rb") as f:
            oldExec = f.read()
        
        with open(softwareName + ".exe", "wb") as f:
            f.write(oldExec)
        
        ignoreVersion(versionString, softwareName, legacyMode)
    
    downDiag.destroy()
    os.remove(softwareName + ".exe.bak")
    if failed: return

    if not legacyMode:
        content = []
        with open(VERSION_PATH, 'r') as f:
            content = json.loads(f.read())
        
        content[softwareName] = versionString
        with open(VERSION_PATH, 'w') as f:
            f.write(json.dumps(content, indent = 4, separators=(',', ': ')))
    else:
        content = []
        with open(OLD_VERSION_PATH, 'r') as f:
            content = f.readlines()
        
        content[LEGACY_VERSIONS.index(softwareName)] = versionString
        for i in range(0, len(content)):
            if i != len(content) - 1: content[i] += "\n"

        with open(OLD_VERSION_PATH, 'w') as f:
            f.writelines(content)

def restartProgram(softwareName):
    os.startfile(softwareName + ".exe")

def getVersionString(softwareName):
    legacyMode = False
    newVersion = {}
    ignoredVersions = []

    if not os.path.exists(VERSION_PATH):
        if os.path.exists(OLD_VERSION_PATH):
            version = []
            with open(OLD_VERSION_PATH, 'r') as f:
                version = f.readlines()
            
            for i in range(0, len(version)): version[i] = version[i].strip()
            legacyMode = legacy.checkLegacy(version)

            if not legacyMode:
                newVersion = {GITHUB_REPO: version[0], "Updater": version[1]}
                os.remove(OLD_VERSION_PATH)
        else:
            newVersion = {APP_NAME: "v1.0", "Updater": "v1.0"}
        
        print(legacyMode, newVersion)

        if not legacyMode:
            with open(VERSION_PATH, 'w') as f:
                f.write(json.dumps(newVersion, indent = 4, separators=(',', ': ')))

    if legacyMode:
        with open(OLD_VERSION_PATH, 'r') as f:
            versionString = f.readlines()[LEGACY_VERSIONS.index(softwareName)]
    else:
        with open(VERSION_PATH, 'r') as f:
            versionFile = json.loads(f.read())
            versionString = versionFile[softwareName]
            
            if "ignored" in versionFile: ignoredVersions = versionFile["ignored"][softwareName]
    
    return versionString, legacyMode, ignoredVersions

def ignoreVersion(versionString, softwareName, legacyMode):
    if legacyMode: return

    versionFile = None
    with open(VERSION_PATH, 'r') as f:
        versionFile = json.loads(f.read())
    
    if not "ignored" in versionFile:
        versionFile["ignored"] = {APP_NAME: [], "Updater": []}
    
    versionFile["ignored"][softwareName].append(versionString)

    with open(VERSION_PATH, 'w') as f:
        f.write(json.dumps(versionFile, indent = 4, separators=(',', ': ')))

def checkNewVersion(softwareName):
    isNewVersion = False
    legacyMode = False

    setts = settings.loadSettings()

    versionString, legacyMode, ignoredVersions = getVersionString(softwareName)
    versionNumber = versionString.split("v")[1]
    
    response = requests.get("https://api.github.com/repos/" + GITHUB_USER + "/" + GITHUB_REPO + "/releases")
    releases = response.json()

    if "message" in releases:
        response = requests.get("https://api.github.com/repos/" + GITHUB_USER + "/" + GITHUB_REPO + "/releases", headers={"Authorization": TOKEN})
        releases = response.json()

        if "message" in releases:
            messagebox.showerror("Ratelimit reached", "Updater could not fetch new version of " + softwareName + ":\nYou have reached your rate limit. Try again later")
            root.destroy()
            return False

    for r in releases:
        tokenized = r["name"].split()
        if tokenized[0] == softwareName:
            latestVersionString = tokenized[1]
            latestVersionNumber = latestVersionString.split("v")[1]

            if latestVersionString in ignoredVersions: break
            if versionNumber > latestVersionNumber: break

            if versionNumber < latestVersionNumber:
                if r["prerelease"] and setts["ignorePrereleases"] == 1: continue

                res = messagebox.askquestion("Updater", "A new version of " + softwareName + " is available: " + latestVersionString + "\nDo you want to update?")

                if res == "yes":
                    warnings = []
                    changelog = []

                    descRaw = r["body"].split("##")
                    for d in descRaw:
                        splitDRaw = d.split("\r\n")
                        splitD = [x for x in splitDRaw if x != ""]

                        if len(splitD) < 2: continue

                        if "Changelog" in splitD[0]: changelog = splitD[1:]
                        if "Warning" in splitD[0]: warnings = splitD[1:]
                    
                    if r["prerelease"]: warnings.append("- This release is a pre-release")

                    if len(warnings) != 0:
                        warningDiagInstance = warningDiag.WarningDiag(root, "Warnings", warnings)
                        if warningDiagInstance.response == "no":
                            ignoreVersion(latestVersionString, softwareName, legacyMode)
                            break

                    downloadNewVersion(latestVersionString, softwareName, legacyMode, r["tag_name"])
                    changelogDiag.ChangelogDiag(root, "Changelog", changelog)
                    isNewVersion = True
                    restartProgram(softwareName)
                else: ignoreVersion(latestVersionString, softwareName, legacyMode)
                break
    
    root.destroy()
    return isNewVersion