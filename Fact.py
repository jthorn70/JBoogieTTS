import RemoveBlank

facts=[]

def loadFacts():
    facts.clear()
    
    with open('facts.txt') as myFile:
        for line in myFile:
            facts.append(line.rstrip())



def addFact(fact):
    facts.append(fact)
    saveFacts()

def removeFact(fact):
    if fact in facts:
        facts.remove(fact.rstrip())
        saveFacts()

def saveFacts():
    with open('facts.txt','w') as f:
        for item in facts:
            f.write("%s\n" % item)