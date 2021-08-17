from datetime import *
import json
from vars import *

def cumulativeSum(index, offset, amount):
    value = 0
    for i in range(2, index + 1):
        value += amount * i + offset
    return value

def readData():
    with open(DATA_PATH, "rt") as f:
        data = json.loads(f.read())
    return data

def writeData(data):
    with open(DATA_PATH, "wt") as f:
        f.write(json.dumps(data, indent = 4, separators=(',', ': ')))

def convertDataFormat(data):
    newData = {}
    if "goals" in data: newData["goals"] = data["goals"]

    newData["seasons"] = [{"name": "First Season", "endDate": data["seasonEndDate"], "activeBPLevel": data["activeBPLevel"], "cXP": data["cXP"], "xpHistory": data["history"]}]
    return newData

# ================================
#  Calculate Values
# ================================

def calcDailyValues(completeData, epilogue, seasonIndex, settings):
    data = completeData["seasons"][seasonIndex]
    done = False

    seasonEndDate = datetime.strptime(data["endDate"], "%d.%m.%Y").date()
    dateDelta = seasonEndDate - date.today()
    remainingDays = dateDelta.days

    totalXP = cumulativeSum(NUM_BPLEVELS, LEVEL2_OFFSET, NUM_XP_PER_LEVEL) + epilogue * NUM_EPLOGUE_LEVELS * NUM_EPLOGUE_XP_PER_LEVEL
    
    if data["activeBPLevel"] - 1 <= NUM_BPLEVELS:
        collectedXP = cumulativeSum(data["activeBPLevel"] - 1, LEVEL2_OFFSET, NUM_XP_PER_LEVEL) + data["cXP"]
    else:
        collectedXP = cumulativeSum(NUM_BPLEVELS, LEVEL2_OFFSET, NUM_XP_PER_LEVEL) + data["cXP"] + (data["activeBPLevel"] - NUM_BPLEVELS - 1) * NUM_EPLOGUE_XP_PER_LEVEL
    
    remainingXP = totalXP - collectedXP

    divisor = remainingDays - settings["bufferDays"]
    if divisor >= -settings["bufferDays"] and divisor <= 0: divisor = 1
    elif divisor < -settings["bufferDays"]: done = True

    if done: return -1, -1, -1, -1
   
    dailyXP = round(remainingXP / divisor)

    xpToday = 0
    for t in data["xpHistory"]:
        if date.fromtimestamp(t["time"]) != date.today():
            continue
        xpToday += int(t["amount"])

    dailyXPRemaining = dailyXP - xpToday
    dailyProgress = round(xpToday / dailyXP * 100)

    return dailyProgress, xpToday, dailyXPRemaining, dailyXP

def calcTotalValues(completeData, epilogue, seasonIndex):
    data = completeData["seasons"][seasonIndex]
    totalXP = cumulativeSum(NUM_BPLEVELS, LEVEL2_OFFSET, NUM_XP_PER_LEVEL) + epilogue * NUM_EPLOGUE_LEVELS * NUM_EPLOGUE_XP_PER_LEVEL
    
    if data["activeBPLevel"] - 1 <= NUM_BPLEVELS:
        collectedXP = cumulativeSum(data["activeBPLevel"] - 1, LEVEL2_OFFSET, NUM_XP_PER_LEVEL) + data["cXP"]
    else:
        collectedXP = cumulativeSum(NUM_BPLEVELS, LEVEL2_OFFSET, NUM_XP_PER_LEVEL) + data["cXP"] + (data["activeBPLevel"] - NUM_BPLEVELS - 1) * NUM_EPLOGUE_XP_PER_LEVEL
    
    remainingXP = totalXP - collectedXP
    totalProgress = round(collectedXP / totalXP * 100)

    return totalProgress, collectedXP, remainingXP, totalXP

def calcBattlepassValues(completeData, epilogue, seasonIndex):
    data = completeData["seasons"][seasonIndex]
    
    bpLastUnlocked = data["activeBPLevel"] - 1
    bpTotal = NUM_BPLEVELS + epilogue * NUM_EPLOGUE_LEVELS
    bpRemaining = bpTotal - bpLastUnlocked
    bpProgress = round(bpLastUnlocked / bpTotal * 100)
    bpActive = data["activeBPLevel"]

    return bpProgress, bpLastUnlocked, bpActive, bpRemaining, bpTotal

def calcLevelValues(completeData, epilogue, seasonIndex):
    data = completeData["seasons"][seasonIndex]
    
    levelCollected = data["cXP"]
    if data["activeBPLevel"] - 1 <= NUM_BPLEVELS:
        levelTotal = LEVEL2_OFFSET + NUM_XP_PER_LEVEL * data["activeBPLevel"]
    else:
        levelTotal = NUM_EPLOGUE_XP_PER_LEVEL
    
    levelRemaining = levelTotal - levelCollected
    levelProgress = round(levelCollected / levelTotal * 100)

    return levelProgress, levelCollected, levelRemaining, levelTotal

def calcMiscValues(completeData, yAxisYou, yAxisIdeal, yAxisDailyIdeal, epilogue, seasonIndex, settings):
    data = completeData["seasons"][seasonIndex]
    
    seasonEndDate = datetime.strptime(data["endDate"], "%d.%m.%Y")
    dateDelta = seasonEndDate - datetime.now()
    miscRemainigDays = dateDelta.days

    prevDate = date.fromtimestamp(data["xpHistory"][0]["time"])
    durationDelta = seasonEndDate.date() - prevDate
    duration = durationDelta.days - 1

    miscDeviationDaily = 0

    dailyXP = []
    index = -1

    for h in data["xpHistory"]:
        currDate = date.fromtimestamp(h["time"])
        if currDate == prevDate and index != -1:
            dailyXP[index]["amount"] = dailyXP[index]["amount"] + int(h["amount"])
        else:
            deltaDate = (currDate - prevDate)

            if settings["ignoreInactiveDays"] == 0:
                for i in range(1, deltaDate.days):
                    dailyXP.append({"date": (prevDate + timedelta(days=i)).strftime("%d.%m.%Y"), "amount": 0})
                    index += 1

            dailyXP.append({"date": currDate.strftime("%d.%m.%Y"), "amount": int(h["amount"])})

            prevDate = currDate
            index += 1
    
    miscAverage = 0
    for d in dailyXP:
        miscAverage += d["amount"]

    miscAverage = round(miscAverage / len(dailyXP))

    t = len(yAxisYou) - 1
    dailyXP.sort(key=lambda item: item.get("amount"))

    if miscRemainigDays >= 0 and miscRemainigDays < duration:
        miscDeviationDaily = yAxisYou[t] - yAxisDailyIdeal[1]
    else: miscRemainigDays = 0
    
    miscDeviationIdeal = yAxisYou[t] - yAxisIdeal[t]
    miscStrongestDayDate = dailyXP[len(dailyXP) - 1]["date"]
    miscStrongestDayAmount = dailyXP[len(dailyXP) - 1]["amount"]
    miscWeakestDayDate = dailyXP[0]["date"]
    miscWeakestDayAmount = dailyXP[0]["amount"]

    return miscRemainigDays, miscAverage, miscDeviationIdeal, miscDeviationDaily, miscStrongestDayDate, miscStrongestDayAmount, miscWeakestDayDate, miscWeakestDayAmount

def recalcXP(completeData, seasonIndex):
    data = completeData["seasons"][seasonIndex]
    collectedXP = 0

    for i in range(0, len(data["xpHistory"])):
        collectedXP += int(data["xpHistory"][i]["amount"])
    
    iteration = 2
    while collectedXP > 0:
        if iteration < NUM_BPLEVELS:
            collectedXP -= LEVEL2_OFFSET + iteration * NUM_XP_PER_LEVEL
        elif iteration < NUM_BPLEVELS + NUM_EPLOGUE_LEVELS:
            collectedXP -= NUM_EPLOGUE_XP_PER_LEVEL
        iteration += 1

    iteration -= 1
    data["activeBPLevel"] = iteration

    if iteration < NUM_BPLEVELS:
        collectedXP += LEVEL2_OFFSET + iteration * NUM_XP_PER_LEVEL
    elif iteration < NUM_BPLEVELS + NUM_EPLOGUE_LEVELS:
        collectedXP += NUM_EPLOGUE_XP_PER_LEVEL
    
    data["cXP"] = collectedXP
    return data

def getScoreTag(desc):
    splitDesc = desc.split()
    scoreCandidates = []

    for s in splitDesc:
        if "-" in s:
            scoreCandidates.append(s)
    
    scores = []
    for c in scoreCandidates:
        scoreComponents = c.split("-")
        if len(scoreComponents) != 2: continue

        noNumeric = False
        for comp in scoreComponents:
            if not comp.isnumeric(): noNumeric = True
        
        if noNumeric: continue

        scores.append(scoreComponents)
    
    if len(scores) != 1: return "none"
    if int(scores[0][0]) > int(scores[0][1]): return "win"
    if int(scores[0][0]) < int(scores[0][1]): return "loss"
    if int(scores[0][0]) == int(scores[0][1]): return "draw"

def startNewSeason(name, remainingDays):
    data = readData()
    delta = timedelta(remainingDays)
    seasonEndDate = date.today() + delta
    seasonEndDateStr = seasonEndDate.strftime("%d.%m.%Y")

    data["seasons"].append({"name": name, "activeBPLevel": 2, "cXP": 0, "endDate": seasonEndDateStr, "xpHistory": [{"time": datetime.now().timestamp(), "description": "Initialization", "amount": 0}]})
    writeData(data)