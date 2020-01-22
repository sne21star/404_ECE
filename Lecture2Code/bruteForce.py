import os.path
from cryptBreak import *
if __name__ == '__main__':
    allPValues = tuple(range(0, 2**16))
    def bruteForce():
        for key in allPValues:
            plain = cryptBreak('encrypted.txt', key)
            if "Mark Twain" in plain:
                print("Encryption Broken!")
                print("Key: ",key)
                print("Message: ",plain)
                if os.path.isfile('decrypted.txt'):
                    FILEOUT = open('decrypted.txt', 'w')  # (d)
                    FILEOUT.write(plain)  # (e)
                    FILEOUT.close()
                else:
                    print("File decrypted.txt does not exist")
                break
