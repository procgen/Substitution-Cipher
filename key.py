# Author: Joshua Lorenzen
# For CECS 378
# Prof. Anthony Giacalone
# 3/6/2019
# This class represents a substitution cipher key 
# It is capable of encrypting and decrypting phrases using that key
# The class also provides functions for use within a genetic algorithm


from random import shuffle, randint

#Create a list to help remember the alphabet
alphabet = list("abcdefghijklmnopqrstuvwxyz")

class Key():

    def __init__(self, forwardKey = {}):
        self.forwardKey = self.__generateKey(forwardKey) #Fill in missing letters in key
        self.__flipkey()
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz")
        self.score = float("-inf")

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    def __eq__(self, other):
        return self.score == other.score

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other

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

    def __generateKey(self, key={}):
        # This private message allows a key to have some values predetermined with the rest randomized
        inputs = list(set(alphabet) - set(key.keys())) #get all unassigned keys 

        values = list(set(alphabet) - set(key.values()))
        #get all unassigned values
        shuffle(values) #shuffle the unassigned values
        for x in range(0, len(inputs)): #for every key, give it an associated value
            key[inputs[x]] = values[x]  #map key alphabet as keys and shuffled one as values
        return key

    def calcScore(self, scorer, msg):
        # Set internal score for use in genetic algorithm
        self.score = scorer.scoreText(self.decrypt(msg))

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
        # Combines two keys together prefering values that increase the score, then mutates at the end
        # Creates a key that is hopefully better than the two that created it with enough variation
        # To ensure progress is made
        childKey = Key(self.forwardKey) # start with a copy of this key
        partnerKey = partner.forwardKey
        keys = childKey.forwardKey.keys()
        for k in keys:
            currentScore = scorer.scoreText(childKey.decrypt(msg)) # See what our score currently is
            if childKey.forwardKey[k] == partnerKey[k]: # if we are already the same just skip
                continue
            else:
                newLetter = partnerKey[k]
                # Check out what mate is mapped to

                oldMap = childKey.backwardKey[newLetter]
                # Find out what child key has as the key for that new letter

                tempMap = childKey.forwardKey.copy()
                # create a temporary key mapping

                # perform the swap
                tempMap[oldMap] = tempMap[k]
                tempMap[k] = newLetter
                tempKey = Key(tempMap)
                newScore = scorer.scoreText(tempKey.decrypt(msg))
                # Find our score with the swap

                if newScore >= currentScore: #If we achieved a better score, keep the swap
                    childKey = tempKey
        childKey.mutate()
        return childKey

    def __str__(self):
        return str(self.forwardKey)