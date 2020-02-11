"""
Homework Number: 4
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: 02/18/2020
"""
# !/usr/bin/env python
# !/usr/bin/env python -W ignore:tostring:DeprecationWarning
#python AES.py -e message.txt key.txt encrypted.txt
#python AES.py -d encrypted.txt key.txt decrypted.txt
from sys import *
from BitVector import *
AES_modulus = BitVector(bitstring='100011011')

subBYTESTABLE = []                                      # for encryption
invSUBBYTESTABLE = []                                               # for decryption
KEY_SCHEDULE = []
SIZE = 256
SUBBYTESTABLE = []
INVSUBBYTESTABLE = []
def encrypt():
    #Read Key
    READKEY = open(sys.argv[3], 'r')
    key = READKEY.read()
    READKEY.close()

    # Create Key Schedule
    print("encrypt")
    KEY_SCHEDULE = keyInit(key)
    printKeySchedule(KEY_SCHEDULE)

    #Turn File into BitVector
    bv = BitVector(filename=sys.argv[2])

    #Open File for Encrypted Text
    encryptedText = open(sys.argv[4], "w")

    # For loop for 10 rounds
    # SubBytes
    # ShiftRows
    # Mix Columns  --> Not on last round
    # Add Round Keys

    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(SIZE)
        if (len(str(bitvec)) % SIZE != 0):
            x = bitvec.length() % SIZE
            bitvec.pad_from_left(SIZE-x)
        if (len(str(bitvec)) > 0):
            pass
        numRounds = 10
        while(numRounds > 1):
            numRounds -= 1
            pass

        if(numRounds == 1):
            pass

    encryptedText.close()
    pass

def createMatrix(list_Before, n):
    listBox = [0]*n
    lenLB = int(len(list_Before) / n)
    for row in range(0,lenLB):
        listBox[row] = list_Before[row*n:n*(row+1)]
    return listBox
def printKeySchedule(key_schedule):
    index = 0
    for word in key_schedule:
        print("word " + str(index) + "   " + str(word))
        if((index+1) % 4 == 0):
            print("\n")
        index+=1

def keyInit(key):
    key_words = []
    key = key.strip()
    key += '0' * (SIZE // 8 - len(key)) if len(key) < SIZE // 8 else key[:SIZE // 8]
    key_bv = BitVector(textstring=key)
    key_words = gen_key_schedule_256(key_bv)

    key_schedule = []

    enumkey_word = enumerate(key_words)
    for word_index, word in enumkey_word:
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i * 8:i * 8 + 8].intValue())
        #print("word %d:  %s" % (word_index, str(keyword_in_ints)))
        key_schedule.append(keyword_in_ints)
    #print(key_schedule)
    num_rounds = 14
    round_keys = [None for i in range(num_rounds + 1)]
    for i in range(num_rounds + 1):
        round_keys[i] = (key_words[i * 4] + key_words[i * 4 + 1] + key_words[i * 4 + 2] + key_words[i * 4 + 3]).get_bitvector_in_hex()

    return key_schedule

def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant
def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal =
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8]
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable

def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBYTESTABLE.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSUBBYTESTABLE.append(int(b))

def decrypt():
    print("decrypt")
    pass

def main():
    charInput = sys.argv[1]

    # Generate Table for Encryption and Decryption
    genTables()
    #print("SBox for Encryption:")
    q = createMatrix(subBYTESTABLE, 16)
    SUBBYTESTABLE = q
    #print(SUBBYTESTABLE)
    #print("SBox for Decryption:")
    q = createMatrix(invSUBBYTESTABLE, 16)
    INVSUBBYTESTABLE = q
    #print(INVSUBBYTESTABLE)


    if (charInput == '-e'):
        encrypt()
    elif (charInput == '-d'):
        decrypt()
    else:
        print("Either -e or -d")
    pass


if __name__ == "__main__":
    main()