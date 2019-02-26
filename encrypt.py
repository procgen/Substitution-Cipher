from key import Key

def removeWhitespace(msg): 
    msg = msg.replace(" ", "")
    newMsg = ""
    for x in msg:
        if x.isalpha() or x == " ":
            newMsg += x
    msg = newMsg
    newMsg = ""
    for x in range(len(msg)):
        newMsg += msg[x]
        if (x % 5) == 4:
            newMsg += " "
    msg = newMsg
    return msg

print("Enter message to encrypt: ")
msg = input()

msg = removeWhitespace(msg)
key = Key()

cipherText = key.encrypt(msg)

print("Cipher text: %s" % cipherText)
print("Key: %s" % key)