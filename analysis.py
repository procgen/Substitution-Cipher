
letterFreq = "etaoinshrdlcumwfgypbvkjxqz"
doubleFreq = "lseotfprmcndgibazxuh"
pairFreq = ["th", "er", "on", "an", "re", "he", "in", "ed", "nd", "ha", "at", "en", "es", "of", "or"]


def findVowels(msg):
    freqs = letterFreqAnalysis(msg)
    sdFreqs = sdAnalysis(msg)

 
    maxFreq = max(freqs, key=freqs.get)
    # maxFreq = sorted(freqs.items(), key= lambda x : x[1], reverse=True)[0][0]

    vowels = []

    while(freqs[maxFreq] > 0):

        vowels.append(maxFreq)

        nextMaxFreq = 'a'

        for k, v in freqs.items():
            if k != maxFreq:
                if (k, maxFreq) in sdFreqs:
                    sdFreq = sdFreqs[k, maxFreq]
                else:
                    sdFreq = 0
                freqs[k] -= 2 * sdFreq            
            else:
                freqs[k] = 0

            if (freqs[nextMaxFreq] < freqs[k]):
                nextMaxFreq = k

        maxFreq = nextMaxFreq

    return vowels


def letterFreqAnalysis(msg):
    freqMap = {}
    for x in msg:
        if not x.isalpha():
            continue
        if x in freqMap:
            freqMap[x] = freqMap[x] + 1
        else:
            freqMap[x] = 1
    return freqMap

def sdAnalysis(msg):
    freqMap = {}
    for i in range(0, len(msg) - 1):
        if (msg[i], msg[i + 1]) in freqMap:
            freqMap[msg[i], msg[i + 1]] += 1
        else:
            freqMap[msg[i], msg[i + 1]] = 1
    return freqMap


def doubleLetterAnalysis(msg):
    freqMap = {}
    for i in range(0, len(msg) - 1):
        if msg[i] == msg[i + 1]:
            x = msg[i]
            if x in freqMap:
                freqMap[x] = freqMap[x] + 1
            else:
                freqMap[x] = 1
    return freqMap

def pairAnalysis(msg):
    freqMap = {}
    for i in range(0, len(msg) - 1):
        x = msg[i] + msg[i + 1]
        if x in freqMap:
            freqMap[x] = freqMap[x] + 1
        else:
            freqMap[x] = 1
    return freqMap

def printSorted(freqMap):
    print(sorted(freqMap.items(), key=lambda x: x[1], reverse=True))


# # file = open("./message.txt")
# file = open("./english_words.txt")

# msg = file.read()

# for x in msg:
#     if not x.isalpha():
#         msg = msg.replace(x, "")

# findVowels(msg)


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
# newmsg = ""
# for x in msg:
#     newmsg += keyFreq[x]

# print(newmsg)