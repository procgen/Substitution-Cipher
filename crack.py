# Author: Joshua Lorenzen
# For CECS 378
# Prof. Anthony Giacalone
# 3/6/2019
# The Following is a genetic algorithm designed to solve substitution ciphers
# It works by generating a population of "Keys", measuring their fitness and
# deciding which ones should mate or survive to the next generation.
# The fitness of a key is scored by counting the frequency of english quadgrams
# The program outputs each key that beats the 'fitness high score' so the 
# key closest to the english result will be printed most recently in the output


from math import log10
from key import Key, alphabet
from random import choices, shuffle
from analysis import findVowels
from os import path
import json


print("This program uses a genetic algorithm to solve substitution ciphers")
print("It will automatically end if no progress is made after a certain number of iterations.")

msg = ""
# Read the message to be decrypted if it exists
if path.exists("./message.txt"):
    file = open("./message.txt")
    msg = file.read()
    file.close()
else: # Otherwise ask for a message as input
    msg = input("Enter message to be decrypted (no newlines): ")
# Strip everything non alphabetic from the message
for x in msg:
    if not x.isalpha():
        msg = msg.replace(x, "")

def randomVowelMap(msg): 
    # Function that returns a partially generated key that assumes 
    # certain letters are vowels
    key = {}
    vowels = ['a', 'e', 'i', 'o', 'u', 't']
    likelyVowels = findVowels(msg)[0:6] #Get the mapped letters that are likely to be vowels
    shuffle(vowels)
    shuffle(likelyVowels)
    for x in range(0, len(likelyVowels)):
        key[vowels[x]] = likelyVowels[x] #create a partial key using the vowels and their likely mappings
    return key

def shiftCaesar(message, shift):
    # Takes a message and shifts it as if it was put through a Caesar cipher
    # Use a positive shift number for encryption, negative shift for decryption
    newMsg = ""
    message = message.lower()
    for x in message:
        if not x.isalpha(): #Skip non alphabetic characters
            newMsg += x
            continue
        index = alphabet.index(x) #Find what 'number' represents this letter
        newMsg += alphabet[(index + shift) % 26] #Replace the letter with a shifted one
    return newMsg

def printSorted(freqMap): 
    # Sorts the keys of the dict alphabetically and displays to the user
    print(sorted(freqMap.items(), key=lambda x: x[1], reverse=True))

class LangScore():
    # Scores english text based on a given quadgram frequency file
    # Returns a score below zero, where a greater number means more likely to be
    # english text

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

#Load the english quadgrams for scoring
# scorer = LangScore("quadcount.txt")
# scorer = LangScore("quadcountCOPIED.txt")
scorer = LangScore("quadcountEdited.txt")

bestScore = scorer.scoreText(msg)
bestMsg = msg
bestShift = 0

# Test the 25 possible Caesar shift combinations and find the closest result to 
# english. This is done before the genetic algorithm begins to speed up decryption 
# of simple Caesar ciphers.
for x in range(1, 25):
    newMsg = shiftCaesar(msg, -x)
    newScore = scorer.scoreText(newMsg)
    if newScore > bestScore:
        bestScore = newScore
        bestMsg = newMsg
        bestShift = x

#Print the closest result to english
print("Key: Caesar Cipher, Shift: %s" % bestShift)
print("Decrypted message: %s" % bestMsg)
print("Message score: %.3f" % bestScore)
print("-" * 50)


def genetic():
    # The main genetic algorithm is within this function
    global bestScore
    POP_SIZE = 50 # Constant that defines size of key population
    elites = [] # Used to store high scoring local maxima
    failClock = 0 # Keep track if we are making any progress at all
    while failClock < 10:
        population = [] #Generate a new population
        for x in range(POP_SIZE):
            newKey = Key(randomVowelMap(msg)) # Every new key is seeded with
                                            # vowels guessed into place
            newKey.calcScore(scorer, msg) #Calculcate initial score
            population.append(newKey)

        populationCounter = 0 # Keeps track of which population generation it is
        populationClock = 0 # Used to generate a new population if stagnation occurs
        metBest = False # If we should keep the best score this population finds
        popBestScore = float("-inf") # Initialize to lowest number possible
        print(". ", end=" ", flush=True) 
        while populationClock < 50:
            population = sorted(population, reverse=True) # Sort so the fittest
                                                        # key is in the front
            if population[0].score > bestScore: 
            # If the fittest key hit a high score
                bestScore = population[0].score
                topKey = population[0]
                #Print out all the information regarding this decryption
                print("Key: %s" % population[0])
                print("Decrypted Message: %s" % population[0].decrypt(msg))
                print("Message score: %.3f" % population[0].score)
                print("-" * 50)
                metBest = True
            #If we are improving (in this ancestry), reset the clock
            if population[0].score > popBestScore:
                populationClock = 0
                popBestScore = population[0].score

            weights = list(range(len(population), 0, -1)) 
            # Weight that prefers values towards the beginning of a list
            mates = choices(population, weights, k=POP_SIZE)
            # Choose first mate for each new member of population
            if populationClock > 30:
                counter = 0 # if the population is failing to improve mix in 
                            # some old high scores into the mating pool
                for x in elites:
                    mates[counter] = x
                    counter += 1

            newPopulation = [] # create each member of the new population
            for x in mates:
                child = population[0].mate(choices(population,weights, k=1)[0], scorer, msg) 
                child.calcScore(scorer, msg)           
                newPopulation.append(child)
            population = newPopulation
            populationClock += 1
        failClock += 1
        # When this population fails to improve, consider adding its fittest member to this list
        if metBest:
            elites.append(population[0])
            elites = elites[-10:]
            failClock = 0 # we have made progress with this generation so reset clock
        if failClock > 6:
            elites = []
    print("Timed out")

# Begin algorithm
genetic()