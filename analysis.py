
def findVowels(msg):
    # Implementation of Sukhotin's algorithm
    # Tries to classify characters as vowels and return a list of them
    # Used to guess at where vowels are to get a head start at decrypting
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
    # Counts the number of times each letters occurs in the text
    # and returns it in a dictionary
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
    # Counts the number of times two letters appear next to eachother
    # in the text and returns the stats in a dictionary
    freqMap = {}
    for i in range(0, len(msg) - 1):
        if (msg[i], msg[i + 1]) in freqMap:
            freqMap[msg[i], msg[i + 1]] += 1
        else:
            freqMap[msg[i], msg[i + 1]] = 1
    return freqMap


def doubleLetterAnalysis(msg):
    # Not used but finds the number of times a letter appears twice
    # next to itself and returns in a dictionary
    freqMap = {}
    for i in range(0, len(msg) - 1):
        if msg[i] == msg[i + 1]:
            x = msg[i]
            if x in freqMap:
                freqMap[x] = freqMap[x] + 1
            else:
                freqMap[x] = 1
    return freqMap


def printSorted(freqMap):
    # Prints frequency data out for testing
    print(sorted(freqMap.items(), key=lambda x: x[1], reverse=True))

