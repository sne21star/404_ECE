from cryptBreak import *
'''
from itertools import product
from BitVector import *                                                     #(A)
PassPhrase = "Hopes and dreams of a million years"                          #(C)
from itertools import permutations
BLOCKSIZE = 16
numbytes = BLOCKSIZE//8
chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
allKeys = product(chars, repeat=BLOCKSIZE)
allBit = tuple(range(0,2**16))
PassPhrase = "Hopes and dreams of a million years"

# Create a bitvector from the ciphertext hex string:
FILEIN = open(sys.argv[1])  # (J)
encrypted_bv = BitVector(hexstring=FILEIN.read())  # (K)
bv_iv = BitVector(bitlist=[0] * BLOCKSIZE)  # (F)

for i in range(0, len(PassPhrase) // numbytes):  # (G)
    textstr = PassPhrase[i * numbytes:(i + 1) * numbytes]  # (H)
    bv_iv ^= BitVector(textstring=textstr)  # (I)
'''
allBit = tuple(range(0, 2**16))
allBit = [25202]*100
def keygen(): # generates a key to try
    for keyTry in allBit: #iterates through the set of keys
        plain = cryptBreak(keyTry,sys.argv[1])
        if "Mark Twain" in plain: #tests decoded message for correctness
            print("Encryption Broken!")
            print("Key: ",keyTry)
            print("Message: ",plain)
            FILEOUT = open(sys.argv[2], 'w')  # (d)
            FILEOUT.write(plain)  # (e)
            FILEOUT.close()
            break
keygen()
