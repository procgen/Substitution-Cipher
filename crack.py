from random import shuffle

def generateKey():
    key = {}
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    newAlphabet = alphabet[:] #create a new copy of the alphabet
    shuffle(newAlphabet) #shuffle the new copy
    for x in range(0, len(alphabet)):
        key[alphabet[x]] = newAlphabet[x] 
    print(key)
    return key


class Key():

    def __init__(self, forwardKey):
        self.forwardKey = forwardKey
        backwardKey = {}
        for k, v in forwardKey.items():
            backwardKey[v] = k
        self.backwardKey = backwardKey

    def __translate(self, message, key):
        newMessage = ""
        message = message.lower()
        for x in message:
            if x.isalpha():
                newMessage += key[x]
            else:
                newMessage += x
        return newMessage

    def encrypt(self, message):
        return self.__translate(message, self.forwardKey)

    def decrypt(self, message):
        return self.__translate(message, self.backwardKey)

key = Key(generateKey())
message = key.encrypt("Test message.")
print(message)
print(key.decrypt(message))

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


# file = open("./message.txt")

# msg = file.read()

# for x in msg:
#     if not x.isalpha():
#         msg = msg.replace(x, "")

# print(msg)

# freq = letterFreqAnalysis(msg)
# freqDouble = doubleLetterAnalysis(msg)
# freqPair = pairAnalysis(msg)

# printSorted(freq)
# printSorted(freqDouble)
# printSorted(freqPair)

# freqSorted = sorted(freq.items(), key=lambda x: x[1], reverse=True)

# print(freqSorted)

# keyFreq = {}

# count = 0
# for k, v in freqSorted:
#     keyFreq[k] = letterFreq[count]
#     count = count + 1

# print(keyFreq)
# print(msg)
# newPhrase = ""
# for x in msg:
#     newPhrase += keyFreq[x]

# print(newPhrase)