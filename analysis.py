
letterFreq = "etaoinshrdlcumwfgypbvkjxqz"
doubleFreq = "lseotfprmcndgibazxuh"
pairFreq = ["th", "er", "on", "an", "re", "he", "in", "ed", "nd", "ha", "at", "en", "es", "of", "or"]

def letterFreqAnalysis(phrase):
    freqMap = {}
    for x in phrase:
        if not x.isalpha():
            continue
        if x in freqMap:
            freqMap[x] = freqMap[x] + 1
        else:
            freqMap[x] = 1
    return freqMap

def doubleLetterAnalysis(phrase):
    freqMap = {}
    for i in range(0, len(phrase) - 1):
        if phrase[i] == phrase[i + 1]:
            x = phrase[i]
            if x in freqMap:
                freqMap[x] = freqMap[x] + 1
            else:
                freqMap[x] = 1
    return freqMap

def pairAnalysis(phrase):
    freqMap = {}
    for i in range(0, len(phrase) - 1):
        x = phrase[i] + phrase[i + 1]
        if x in freqMap:
            freqMap[x] = freqMap[x] + 1
        else:
            freqMap[x] = 1
    return freqMap

def printSorted(freqMap):
    print(sorted(freqMap.items(), key=lambda x: x[1], reverse=True))


file = open("./message.txt")

msg = file.read()

for x in msg:
    if not x.isalpha():
        msg = msg.replace(x, "")

print(msg)

freq = letterFreqAnalysis(msg)
freqDouble = doubleLetterAnalysis(msg)
freqPair = pairAnalysis(msg)

printSorted(freq)
printSorted(freqDouble)
printSorted(freqPair)

freqSorted = sorted(freq.items(), key=lambda x: x[1], reverse=True)

print(freqSorted)

keyFreq = {}

count = 0
for k, v in freqSorted:
    keyFreq[k] = letterFreq[count]
    count = count + 1

print(keyFreq)
print(msg)
newPhrase = ""
for x in msg:
    newPhrase += keyFreq[x]

print(newPhrase)