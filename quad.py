import json, os.path

def printSorted(freqMap):
    print(sorted(freqMap.items(), key=lambda x: x[1], reverse=True))

def countQuads(filepath):
    quadFreq = {}
    if os.path.exists("./quadcount.txt"):
        data = open("quadcount.txt")
        quadFreq = json.load(data)
        data.close()
    else:
        print("New file created")
        data = open("quadcount.txt", 'w')
        json.dump(quadFreq, data)
        data.close()
    file = open(filepath)
    text = file.read()
    for x in text:
        if not x.isalpha():
            text = text.replace(x, "")
    text = text.upper()

    for x in range(0, len(text) - 4):
        quad = ""
        for y in range(4):
            quad += text[x + y]
        if quad in quadFreq:
            quadFreq[quad] = quadFreq[quad] + 1
        else:
            quadFreq[quad] = 1
    printSorted(quadFreq)

    data = open("quadcount.txt", 'w')
    json.dump(quadFreq, data)

# print("Enter path to file: ")
# test = raw_input()
# print(test)
# countQuads(test)
quadFreq = {}
file = open("english_quadgrams.txt")

for line in file:
    key, value = line.split(" ")
    quadFreq[key] = int(value.replace("\n", ""))


data = open("quadcountCOPIED.txt", 'w')
json.dump(quadFreq, data)
data.close()