from random import shuffle, randint
from math import log10
import json

#Create a list to help remember the alphabet
alphabet = list("abcdefghijklmnopqrstuvwxyz")

#Read the message to be decrypted
file = open("./message.txt")
msg = file.read()
for x in msg:
    if not x.isalpha():
        msg = msg.replace(x, "")
file.close()

#Initialize a list with a ton of english words
file = open("./english_words.txt")
wordList = []
for line in file:
    wordList.append(line.rstrip())
file.close()


def shiftCaesar(message, shift):
    ## Takes a message and shifts it as if it was put through a Caesar cipher
    ## Use a positive shift for encryption, negative shift for decryption
    newMsg = ""
    message = message.lower()
    for x in message:
        if not x.isalpha(): #Skip non alphabetic characters
            newMsg += x
            continue
        index = alphabet.index(x) #Find what 'number' represents this letter
        newMsg += alphabet[(index + shift) % 26] #Replace the letter with a shifted one
    return newMsg

def splitWords(message): #Attempts to split up a phrase by english words
    for x in range(len(message), 0, -1): #Work backwards to find solutions with larger words first
        if message[0:x] in wordList: #Go through message until a working word is found
            result = message[0:x] + " " + splitWords(message[x:]) #recursively find results until one works
            if set(result.split(" ")).issubset(wordList):
                return result #Only return split if every other piece of the message is split into a word
    return message

def printSorted(freqMap): #Sorts the keys of the dict for display to the user
    print(sorted(freqMap.items(), key=lambda x: x[1], reverse=True))

class Key():

    def __init__(self, forwardKey = None):
        if forwardKey == None:
            self.forwardKey = self.__generateKey()
        else:
            self.forwardKey = forwardKey #Take the key as constructor args
        self.__flipkey()
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz")

    def __flipkey(self):
        backwardKey = {}
        for k, v in self.forwardKey.items(): #Create a hashmap with the values and keys swapped
            backwardKey[v] = k
        self.backwardKey = backwardKey

    def __translate(self, message, key):
        newMessage = "" #run every letter through the appropriate dict mapping
        message = message.lower() #this converts each letter like a substitution cipher
        for x in message:
            if x.isalpha(): #Skip non alphabetic characters
                newMessage += key[x]
            else:
                newMessage += x
        return newMessage

    def __generateKey(self):
        key = {}
        newAlphabet = alphabet[:] #create a new copy of the alphabet
        shuffle(newAlphabet) #shuffle the new copy
        for x in range(0, len(alphabet)):
            key[alphabet[x]] = newAlphabet[x]  #map old alphabet as keys and shuffled one as values
        return key


    def encrypt(self, message):
        return self.__translate(message, self.forwardKey)

    def decrypt(self, message):
        return self.__translate(message, self.backwardKey)

    def mutate(self):
        newKey = self.forwardKey
        num1 = randint(0, 25) #Generate two random numbers
        num2 = randint(0, 25)
        temp = ""
        temp = newKey[self.alphabet[num1]] #Swap the mapping located at those two indices
        newKey[self.alphabet[num1]] = newKey[self.alphabet[num2]]
        newKey[self.alphabet[num2]] = temp
        return Key(newKey) #reutn the resulting mutated key

    def mate(self, partner, scorer, msg):
        childKey = Key(self.forwardKey)
        partnerKey = partner.forwardKey
        for k in childKey.keys():
            currentScore = scorer.scoreText(childKey.decrypt(msg))
            if childKey.forwardKey[k] == partnerKey[k]:
                continue
            else:
                newLetter = partnerKey[k]
                oldMap = childKey.backwardKey[newLetter]
                tempMap = childKey.forwardKey
                tempMap[oldMap] = tempMap[k]
                tempMap[k] = newLetter
                tempKey = Key(tempMap)
                newScore = scorer.scoreText(tempKey.decrypt(msg))
                if newScore >= currentScore: #If we achieved a better score, keep the swap
                    childKey = tempKey
        childKey.mutate()
        return childKey




    def __str__(self):
        return str(self.forwardKey)

class LangScore():

    def __init__(self, filepath):
        data = open(filepath)
        quadFreq = json.load(data)
        data.close()
        self.N = sum(quadFreq.values())
        self.quadData = {}
        for k, v in quadFreq.items():
            self.quadData[k] = log10(float(v) / float(self.N))
        self.floor = log10(0.01/self.N)
        print("Scorer initialized")

    def scoreText(self, text):
        score = 0
        for x in range(0, len(text) - 4):
            if text[x:x+4].upper() in self.quadData:
                score += self.quadData[text[x:x+4].upper()]
            else:
                score += self.floor
        return score

#Load the english NGRAMS for scoring
# scorer = LangScore("quadcount.txt")
scorer = LangScore("quadcountCOPIED.txt")

bestScore = scorer.scoreText(msg)
bestMsg = msg
bestShift = 0

#Test the 25 possible Caesar shift combinations and find the closest result to english
for x in range(1, 25):
    newMsg = shiftCaesar(msg, -x)
    newScore = scorer.scoreText(newMsg)
    if newScore > bestScore:
        bestScore = newScore
        bestMsg = newMsg
        bestShift = x

#Print the closest result to english
print("Key: Caesar Cipher, Shift: %s" % bestShift)
print("Decrypted message: %s" % splitWords(bestMsg))
print("Message score: %.3f" % bestScore)
print("-" * 50)



def hillClimb():
    global bestScore

    topKey = {}
    # key = Key(generateKey())
    key = Key()
    score = bestScore

    while True:

        improved = False
        for x in range(1000):
            newKey = key.mutate()
            result = key.decrypt(msg)
            newScore = scorer.scoreText(result)
            if newScore > score:
                score = newScore
                key = newKey
                improved = True
                break
        if not improved:
            if score > bestScore:
                bestScore = score
                topKey = key
                print("Key: %s" % key)
                print("Decrypted Message: %s" % splitWords(key.decrypt(msg)))
                print("Message score: %.3f" % score)
                print("-" * 50)
            # key = Key(generateKey())
            key = Key()
            score = float("-inf")

def genetic():

    global bestScore



hillClimb()