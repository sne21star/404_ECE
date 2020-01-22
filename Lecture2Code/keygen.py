from cryptBreak import *
allBit = tuple(range(0, 2**16))
allBit = [25202]*100
def keygen(): # generates a key to try
    for keyTry in allBit: #iterates through the set of keys
        plain = cryptBreak('encrypted.txt', keyTry)
        if "Mark Twain" in plain: #tests decoded message for correctness
            print("Encryption Broken!")
            print("Key: ",keyTry)
            print("Message: ",plain)
            FILEOUT = open('decrypted.txt', 'w')  # (d)
            FILEOUT.write(plain)  # (e)
            FILEOUT.close()
            break
keygen()
