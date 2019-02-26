from math import log10
from key import Key, alphabet
from random import choices
import json

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

# testKey1 = Key()
# testKey2 = Key()

# print(testKey1)
# print(scorer.scoreText(testKey1.decrypt(msg)))
# print(testKey2)
# print(scorer.scoreText(testKey2.decrypt(msg)))
# childKey = testKey1.mate(testKey2, scorer, msg)
# print(childKey)
# print(scorer.scoreText(childKey.decrypt(msg)))

# print(scorer.scoreText("testingtheabilityofmyprogramtodecryptamessage"))

# exit()

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
    POP_SIZE = 50

    while True:
        population = []
        for x in range(POP_SIZE):
            newKey = Key()
            newKey.calcScore(scorer, msg)
            population.append(newKey)

        populationCount = 1
        while populationCount <= 250:
            population = sorted(population, reverse=True)
            if population[0].score > bestScore:
                print("Population #%i" % populationCount)
                bestScore = population[0].score
                topKey = population[0]
                print("Key: %s" % population[0])
                print("Decrypted Message: %s" % splitWords(population[0].decrypt(msg)))
                print("Message score: %.3f" % population[0].score)
                print("-" * 50)
                populationCount = 0

            weights = list(range(len(population), 0, -1))
            mates = choices(population, weights, k=POP_SIZE)
            # for x in range(9):
            #     newKey = Key()
            #     newKey.calcScore(scorer, msg)
            #     mates.append(newKey)

            # print("Best one: ")
            # print(population[0])
            newPopulation = []
            for x in mates:
                child = population[0].mate(choices(population,weights, k=1)[0], scorer, msg) 
                child.calcScore(scorer, msg)           
                newPopulation.append(child)
            population = newPopulation
            populationCount += 1




    

genetic()