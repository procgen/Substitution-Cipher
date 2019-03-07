from key import Key, alphabet

def removeWhitespace(msg): 
    # Removes everything that isn't an alphabetic character
    # Then spaces everything out in groups of 5
    msg = msg.replace(" ", "")
    newMsg = ""
    for x in msg:
        if x.isalpha() or x == " ":
            newMsg += x
    msg = newMsg
    newMsg = ""
    # Space everything in groups of 5
    for x in range(len(msg)):
        newMsg += msg[x]
        if (x % 5) == 4:
            newMsg += " "
    msg = newMsg
    return msg

def enterKey():
    # Accepts a key from the user and returns it
    key = {}
    userKey = ""
    while True:
        print("Enter letters in the order of how you'd like them mapped in the key")
        print("Example if you want Caesar shift of 1: zabcdefghijklmnopqrstuvwxy")
        print("abcdefghijklmnopqrstuvwxyz")
        userKey = input()
        if len(userKey) == 26:
            break
        else:
            print("You messed up somewhere. Try again")
    for x in range(len(alphabet)):
        key[alphabet[x]] = userKey[x]
    return Key(key)


#Basic menu that gives the user options
choice = 0
while True:
    print("Enter the number of what you'd like to do")
    print("\t1. Encrypt a message with given key")
    print("\t2. Decrypt a message with given key")
    print("\t3. Encrypt a message with a random key")
    
    choice = int(input())

    if choice == 1 or choice == 2 or choice == 3:
        break;
    else:
        print("You messed up. Try again")

if choice == 3:
    key = Key() # randomly generate a key
else:
    key = enterKey()

print("Enter message: ")
msg = input()

if choice == 2:
    plainText = key.decrypt(msg)
    print("Plaintext: %s" % plainText)
else:
    msg = removeWhitespace(msg)
    cipherText = key.encrypt(msg)
    print("Ciphertext: %s" % cipherText)

print("Key: %s" % key) # Print the key we used in case it was generated randomly

