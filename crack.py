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


def generateKey():
    key = {}
    newAlphabet = alphabet[:] #create a new copy of the alphabet
    shuffle(newAlphabet) #shuffle the new copy
    for x in range(0, len(alphabet)):
        key[alphabet[x]] = newAlphabet[x] 
    return key

def shiftCaesar(message, shift):
    ## Takes a message and shifts it as if it was put through a Caesar cipher
    ## Use a positive shift for encryption, negative shift for decryption
    newMsg = ""
    message = message.lower()
    for x in message:
        if not x.isalpha():
            newMsg += x
            continue
        index = alphabet.index(x)
        newMsg += alphabet[(index + shift) % 26]
    return newMsg

# def splitWords(message):
#     newMsg = ""
#     while message != "":
#         for x in range(0, len(message)):
#             if message[0:x] in wordList:
#                 newMsg += message[0:x] + " "
#                 message = message[x:]
#                 break
#             if x == len(message) - 1:
#                 newMsg += message
#                 message = ""
#                 break
#     return newMsg

def splitWords(message):
    for x in range(len(message), 0, -1):
        if message[0:x] in wordList:
            result = message[0:x] + " " + splitWords(message[x:])
            if set(result.split(" ")).issubset(wordList):
                return result
    return message

def printSorted(freqMap):
    print(sorted(freqMap.items(), key=lambda x: x[1], reverse=True))

class Key():

    def __init__(self, forwardKey):
        self.forwardKey = forwardKey #Take the key as constructor args
        self.__flipkey()
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz")

    def __flipkey(self):
        backwardKey = {}
        for k, v in self.forwardKey.items(): #Create a hashmap with the values and keys swapped
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

    def mutate(self):
        newKey = self.forwardKey
        num1 = randint(0, 25)
        num2 = randint(0, 25)
        temp = ""
        temp = newKey[self.alphabet[num1]]
        newKey[self.alphabet[num1]] = newKey[self.alphabet[num2]]
        newKey[self.alphabet[num2]] = temp
        return Key(newKey)

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

# exit()

# print(scorer.scoreText("Hello my name is josh"))


# exit()


# bestScore = -1
# score = -1
# key = Key(generateKey())

# while True:
#     prevScore = score
#     for x in range(0, 1000):
#         newKey = key.mutate()
#         result = key.decrypt(msg)
#         newScore = scorer.scoreText(result)
#         if newScore > score:
#             score = newScore
#             key = newKey
#             break
#     if score > bestScore:
#         bestScore = score
#         print(key)
#         print(result)
#         print(newScore)

topKey = {}
key = Key(generateKey())
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
        key = Key(generateKey())
        score = float("-inf")

