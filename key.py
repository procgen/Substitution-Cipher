from random import shuffle, randint

#Create a list to help remember the alphabet
alphabet = list("abcdefghijklmnopqrstuvwxyz")

class Key():

    def __init__(self, forwardKey = None):
        if forwardKey == None:
            self.forwardKey = self.__generateKey()
        else:
            self.forwardKey = forwardKey #Take the key as constructor args
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

    def __generateKey(self):
        key = {}
        newAlphabet = alphabet[:] #create a new copy of the alphabet
        shuffle(newAlphabet) #shuffle the new copy
        for x in range(0, len(alphabet)):
            key[alphabet[x]] = newAlphabet[x]  #map old alphabet as keys and shuffled one as values
        return key

    def calcScore(self, scorer, msg):
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
        childKey = Key(self.forwardKey)
        partnerKey = partner.forwardKey
        keys = childKey.forwardKey.keys()
        for k in keys:
            currentScore = scorer.scoreText(childKey.decrypt(msg))
            if childKey.forwardKey[k] == partnerKey[k]:
                continue
            else:
                # print(k, childKey.forwardKey[k], k, partnerKey[k])

                newLetter = partnerKey[k]
                #Check out what mate is mapped to

                oldMap = childKey.backwardKey[newLetter]
                #Find out what child key has as the key for that new letter

                tempMap = childKey.forwardKey.copy()
                #create a temporary key mapping

                tempMap[oldMap] = tempMap[k]

                tempMap[k] = newLetter
                tempKey = Key(tempMap)
                newScore = scorer.scoreText(tempKey.decrypt(msg))

                if newScore >= currentScore: #If we achieved a better score, keep the swap
                    childKey = tempKey
        # childKey.mutate()
        childKey.mutate()
        return childKey

    def __str__(self):
        return str(self.forwardKey)

    def __getitem__(self, key):
        return self