import RemoveBlank

banList = []

def loadBans():
    banList.clear()
    with open('bans.txt') as myFile:
        for line in myFile:
            banList.append(line.rstrip().lower())

def addBan(name):
    banList.append(name.rstrip().lower())
    saveBans()

def removeBan(name):
    if name.rstrip().lower() in banList:
        banList.remove(name.rstrip().lower())
        saveBans()

def saveBans():
    with open('bans.txt', 'w') as f:
        for item in banList:
            f.write("%s\n" % item)