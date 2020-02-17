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

SUBBYTESTABLE = []                                      # for encryption
INVSUBBYTESTABLE = []                                               # for decryption
KEY_SCHEDULE = []
SIZE = 256
SIZEPLAIN = 128


def encrypt():
    #Read Key
    READKEY = open(sys.argv[3], 'r')
    key = READKEY.read()
    READKEY.close()

    # Create Key Schedule
    print("encrypt")
    KEY_SCHEDULE = keyInit(key)
    first_words = KEY_SCHEDULE[0]

    #Turn File into BitVector
    bv = BitVector(filename=sys.argv[2])

    #Open File for Encrypted Text
    encryptedText = open(sys.argv[4], "w")

    while(bv.more_to_read):
        #Get 128 Bit for Plain Text
        bitvec = bv.read_bits_from_file(SIZEPLAIN)

        #If block is < 128, pad zeroes
        if (len(str(bitvec)) % SIZEPLAIN != 0):
            x = bitvec.length() % SIZE
            bitvec.pad_from_right(SIZEPLAIN-x)
        # First Add Round Key
        firstwordsHex = BitVector(hexstring = first_words)
        bitvec = bitvec ^ firstwordsHex
        numRounds = 1
        while(numRounds < 14):
            #Turn Bit vector into State Array
            statearray = matrixArray(bitvec)

            # SubBytes
            statearray = substitution(statearray, 'E')

            # ShiftRows
            statearray = shiftRows(statearray, 'E')
            statearray = intToBitVector(statearray)

            # Mix Columns  --> Not on last round
            statearray = mixColumns(statearray, 'E')
            p = bitToHex(statearray)

            # Add Round Keys
            next_word = KEY_SCHEDULE[numRounds]
            statearray = roundKeys(p, next_word)
            print(statearray)
            bitvec = statearray#BitVector(hexstring= statearray)
            if (len(str(bitvec)) % SIZEPLAIN != 0):
                x = bitvec.length() % SIZE
                bitvec.pad_from_left(SIZEPLAIN - x)
            numRounds += 1
        if(numRounds == 14):
            #Turn Bit vector into State Array
            statearray = matrixArray(bitvec)

            # SubBytes
            statearray = substitution(statearray, 'E')

            # ShiftRows
            statearray = shiftRows(statearray, 'E')
            statearray = intToBitVector(statearray)

            hexFinal = ""
            for x in statearray:
                for y in x:
                    hexFinal += y.get_bitvector_in_hex()
            #Add RoundKey
            next_word = KEY_SCHEDULE[numRounds]
            hexFinal = roundKeys(hexFinal, next_word)
            print(hexFinal.get_bitvector_in_hex())
            encryptedText.write(hexFinal.get_bitvector_in_hex())
    encryptedText.close()
    pass


def decrypt():
    print("decrypt")
    # Read Key
    READKEY = open(sys.argv[3], 'r')
    key = READKEY.read()
    printKeySchedule(key)
    READKEY.close()

    # Create Key Schedule
    KEY_SCHEDULE = keyInit(key)
    KEY_SCHEDULE = KEY_SCHEDULE[::-1]
    #printKeySchedule(KEY_SCHEDULE)
    # Turn File into BitVector
    HEXFILE = open(sys.argv[2], 'r')
    hexString = HEXFILE.read()
    bv = BitVector(hexstring = hexString)
    BITVECTORTEXT = open("bitVector.txt", "wb")
    bv.write_to_file(BITVECTORTEXT)
    BITVECTORTEXT.close()
    bv = BitVector(filename="bitVector.txt")
    # Open File for Encrypted Text
    decryptedText = open(sys.argv[4], "w")

    while (bv.more_to_read):
        # Get 128 Bit for Plain Text
        bitvec = bv.read_bits_from_file(SIZEPLAIN)
        # If block is < 128, pad zeroes
        if (len(str(bitvec)) % SIZEPLAIN != 0):
            x = bitvec.length() % SIZEPLAIN
            bitvec.pad_from_right(SIZEPLAIN - x)
        print("before round key")
        print(bitvec.get_bitvector_in_hex())

        # First Add Round Key
        first_words = KEY_SCHEDULE[0]
        firstwordsHex = BitVector(hexstring=first_words)
        bitvec = bitvec ^ firstwordsHex
        numRounds = 1
        while (numRounds < 14):
            # Turn Bit vector into State Array
            if(numRounds == 1):
                statearray = matrixArray(bitvec)
            print("stateArray")
            print(statearray)

            # ShiftRows - WORKING
            statearray = InverseshiftRows(statearray)
            print("Shift Row")
            print(statearray)
            statearray = hextobit(statearray)

            # SubBytes - WORKING
            statearray = substitution(statearray, 'D')
            print("subbytes")
            statearray = [list(x) for x in zip(statearray[0], statearray[1], statearray[2], statearray[3])]
            print(statearray)
            statearray = intToHex(statearray)
            print(statearray)

            # Add Round Keys - WORKING
            NW = KEY_SCHEDULE[numRounds]
            print("round key")
            print(NW)
            hexFinalL = ""
            if(numRounds == 1):
                for i in range(4):
                    for j in range(4):
                        hexFinalL += statearray[j][i]
            else:
                for i in range(4):
                    for j in range(4):
                        if(len(str(statearray[j][i])) == 1):
                                statearray[j][i] = '0' + statearray[j][i]
                        print(statearray[j][i])
                        hexFinalL += statearray[j][i]
            print(hexFinalL)
            hexFinalL = BitVector(hexstring=hexFinalL)
            next_word = BitVector(hexstring=NW)
            statearray = hexFinalL ^ next_word
            print("inverse round key")
            print(statearray.get_bitvector_in_hex())

            # Mix Columns  --> Not on last round
            statearray = matrixArray(statearray)
            statearray = hextobit(statearray)
            statearray = mixColumns(statearray, 'D')
            print("Mix Columns")
            print(statearray[0][0].get_bitvector_in_hex())
            print(statearray[3][3].get_bitvector_in_hex())
            #statearray = [list(x) for x in zip(statearray[0], statearray[1], statearray[2], statearray[3])]
            #Put into bitvector and start process again
            statearray = bitToHex(statearray)
            numRounds += 1

        if (numRounds == 14):
            #statearray = matrixArray(bitvec)
            print("stateArray")
            print(statearray)

            # ShiftRows
            statearray = InverseshiftRows(statearray)
            print("Shift Row")
            print(statearray)
            statearray = hextobit(statearray)

            # SubBytes
            #statearray = BitVector(hexstring= "b7af2f6ffcaf7c7bf2cafefcad63f09c")
            #statearray = matrixArray(statearray)
            #statearray = hextobit(statearray)
            statearray = substitution(statearray, 'D')
            print("subbytes")
            statearray = intToHex(statearray)
            print(statearray)

            # Add Round Keys
            NW = KEY_SCHEDULE[numRounds]
            print("round key")
            print(NW)
            hexFinalL = ""
            for i in range(4):
                for j in range(4):
                    if (len(str(statearray[i][j])) == 1):
                        statearray[i][j] = '0' + statearray[i][j]
                    print(statearray[i][j])
                    hexFinalL += statearray[i][j]
            print(hexFinalL)
            hexFinalL = BitVector(hexstring=hexFinalL)
            next_word = BitVector(hexstring=NW)
            hexFinal = hexFinalL ^ next_word
            #Send text to file
            print(hexFinal.get_bitvector_in_hex())
            print(hexFinal.get_bitvector_in_ascii())
            hexFinal = hexFinal.get_text_from_bitvector()
            if(ord(hexFinal[len(hexFinal)-1]) == 0):
                hexFinal = hexFinal[:-1]
            decryptedText.write(hexFinal)

    decryptedText.close()

def intToBitVector(matrix):
    for i in range(4):
        for j in range(4):
            matrix[i][j] = BitVector(intVal = matrix[i][j], size = 8)
    return matrix

def hextobit(matrix):
    for i in range(4):
        for j in range(4):
            matrix[i][j] = BitVector(hexstring = matrix[i][j])
    return matrix

def bitToInt(matrix):
    for i in range(4):
        for j in range(4):
            matrix[i][j] = int(matrix[i][j])
    return matrix

def bitToHex(matrix):
    returnMatrix = [[0 for x in range(4)] for x in range(4)]
    for i in range(4):
        for j in range(4):
            returnMatrix[i][j] = matrix[i][j].get_bitvector_in_hex()
    return returnMatrix

def intToHex(matrix):
    for i in range(4):
        for j in range(4):
            matrix[i][j] = format(matrix[i][j], 'x')
            if(len(str(matrix[i][j])) == 1):
                matrix[i][j] = '0' + matrix[i][j]
    return matrix

def matrixArray(bitvec):
    bitvecHex = bitvec.get_bitvector_in_hex()
    n = 2
    bitvecHex = [bitvecHex[i:i + n] for i in range(0, len(bitvecHex), n)]
    statearray = [[0 for x in range(4)] for x in range(4)]
    index = 0
    for i in range(4):
        for j in range(4):
            statearray[i][j] = bitvecHex[index]
            index += 1
    return statearray

def substitution(hexVector, charX):
    if(charX == 'E'):
        for i in range(4):
            for j in range(4):
                hexVector[i][j] = SUBBYTESTABLE[int(hexVector[i][j], 16)]
    else:
        for i in range(4):
            for j in range(4):
                hexVector[i][j] = INVSUBBYTESTABLE[hexVector[i][j].int_val()]
    return hexVector

def shiftRows(vector, charX):
    shift = 1
    vector = [list(x) for x in zip(vector[0], vector[1], vector[2], vector[3])]
    while(shift < 4):
       if(charX == 'D'):
           vector[shift] = rotateElemList(vector[shift], -shift)
       else:
           vector[shift] = rotateElemList(vector[shift], shift)
       shift+=1
    vector = [list(x) for x in zip(vector[0], vector[1], vector[2], vector[3])]
    return vector

def InverseshiftRows(vector):
    shift = 1
    vector = [list(x) for x in zip(vector[0], vector[1], vector[2], vector[3])]
    while(shift < 4):
       vector[shift] = rotateElemList(vector[shift], -shift)
       shift+=1
    vector = [list(x) for x in zip(vector[0], vector[1], vector[2], vector[3])]
    return vector

def rotateElemList(listX, shift):
    return listX[shift:] + listX[:shift]

def mixColumns(matrix, charX):
    MIXCOLUMNSE = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    MIXCOLUMNSD = [[0x0E, 0x0B, 0x0D, 0x09],[0x09, 0x0E, 0x0B, 0x0D],[0x0D, 0x09,0x0E ,0x0B],[0x0B, 0x0D, 0x09, 0x0E]]
    if(charX == 'E'):
        mixColumns = intToBitVector(MIXCOLUMNSE)
    else:
        mixColumns = intToBitVector(MIXCOLUMNSD)
    matrix = [list(x) for x in zip(matrix[0], matrix[1], matrix[2], matrix[3])]
    endMatrix = [[0 for x in range(4)] for x in range(4)]
    for i in range(4):
        for j in range(4):
            int0 = mixColumns[i][0]
            int1 = mixColumns[i][1]
            int2 = mixColumns[i][2]
            int3 = mixColumns[i][3]
            bitvec0 = int0.gf_multiply_modular(matrix[0][j], AES_modulus, 8)
            bitvec1 = int1.gf_multiply_modular(matrix[1][j], AES_modulus, 8)
            bitvec2 = int2.gf_multiply_modular(matrix[2][j], AES_modulus, 8)
            bitvec3 = int3.gf_multiply_modular(matrix[3][j], AES_modulus, 8)
            bitvec0 ^= bitvec1
            bitvec0 ^= bitvec2
            bitvec0 ^= bitvec3
            endMatrix[i][j] = bitvec0
    endMatrix = [list(x) for x in zip(endMatrix[0], endMatrix[1], endMatrix[2], endMatrix[3])]
    return endMatrix

def InversemixColumns(matrix):
    MIXCOLUMNSD = [[0x0E, 0x0B, 0x0D, 0x09],[0x09, 0x0E, 0x0B, 0x0D],[0x0D, 0x09,0x0E ,0x0B],[0x0B, 0x0D, 0x09, 0x0E]]
    mixColumns = intToBitVector(MIXCOLUMNSD)
    endMatrix = BitVector(size = 0)
    for i in range(4):
        for j in range(4):
            int0 = mixColumns[i][0]
            int1 = mixColumns[i][1]
            int2 = mixColumns[i][2]
            int3 = mixColumns[i][3]
            bitvec0 = int0.gf_multiply_modular(matrix[0][j], AES_modulus, 8)
            bitvec1 = int1.gf_multiply_modular(matrix[1][j], AES_modulus, 8)
            bitvec2 = int2.gf_multiply_modular(matrix[2][j], AES_modulus, 8)
            bitvec3 = int3.gf_multiply_modular(matrix[3][j], AES_modulus, 8)
            endMatrix += (bitvec0 ^ bitvec1 ^ bitvec2 ^ bitvec3)
    return endMatrix

def roundKeys(p, next_words):
    hexFinal = ""
    for x in p:
        for y in x:
            hexFinal += y
    hexFinal = BitVector(hexstring=hexFinal)
    if (len(str(hexFinal)) % SIZEPLAIN != 0):
        x = hexFinal.length() % SIZEPLAIN
        hexFinal.pad_from_left(SIZEPLAIN - x)
    next_word = BitVector(hexstring=next_words)
    hexFinal = hexFinal ^ next_word
    return hexFinal

def InverseroundKeys(p, next_words):
    hexFinal = ""
    for x in p:
        for y in x:
            hexFinal += y
    print(hexFinal)
    hexFinal = BitVector(hexstring=hexFinal)
    if (len(str(hexFinal)) % SIZEPLAIN != 0):
        x = hexFinal.length() % SIZEPLAIN
        hexFinal.pad_from_left(SIZEPLAIN - x)
    next_word = BitVector(hexstring=next_words)
    hexFinal = hexFinal ^ next_word
    return hexFinal

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
    return round_keys

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
        SUBBYTESTABLE.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        INVSUBBYTESTABLE.append(int(b))

def main():
    charInput = sys.argv[1]

    # Generate Table for Encryption and Decryption
    genTables()
    #print(SUBBYTESTABLE)
    if (charInput == '-e'):
        encrypt()
        pass
    elif (charInput == '-d'):
        decrypt()
    else:
        print("Either -e or -d")
    pass


if __name__ == "__main__":
    main()