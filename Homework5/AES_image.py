"""
Homework Number: 5
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: 02/25/2020
"""
from sys import *
from BitVector import *
AES_modulus = BitVector(bitstring='100011011')

SUBBYTESTABLE = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240,
     173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
     4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59,
     214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170,
     251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33,
     16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34,
     42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228,
     121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180,
     198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
     225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104,
     65, 153, 45, 15, 176, 84, 187, 22]            # for encryption
KEY_SCHEDULE = []
SIZE = 256
SIZEPLAIN = 128

def encrypt(key, v0, image_file, out_file):
    #Key is given to us
    # Create Key Schedule
    KEY_SCHEDULE = keyInit(key)
    first_words = KEY_SCHEDULE[0]

    #Turn File into BitVector by Reading Image File
    image = open(image_file, 'rb')
    imageno = image.readline()
    height_width = image.readline()
    max_pixVal = image.readline()
    image.close()

    #Open File for Encrypted Text
    encryptedText = open(out_file, "wb")
    encryptedText.write(imageno)
    encryptedText.write(height_width)
    encryptedText.write(max_pixVal)
    bv = BitVector(filename=image_file)

    index = -1
    while(bv.more_to_read):

        #Get 128 Bit for Plain Text
        if(index == -1):
            XorAtEnd = bv.read_bits_from_file(SIZEPLAIN-16)
            #print(XorAtEnd.get_bitvector_in_hex())
            XorAtEnd = bv.read_bits_from_file(SIZEPLAIN)
            #print(XorAtEnd.get_bitvector_in_hex())
        else:
            XorAtEnd = bv.read_bits_from_file(SIZEPLAIN)

        #If block is < 128, pad zeroes
        if (len(str(XorAtEnd)) % SIZEPLAIN != 0):
            x = XorAtEnd.length() % SIZE
            XorAtEnd.pad_from_right(SIZEPLAIN-x)
        #THE BITVECTOR IS INTIALIZED BITVECTOR INCREMENT IF NECESSARY
        index += 1
        vX = v0.int_val()
        vX += index
        vX = BitVector(intVal=vX)
        bitvec = vX

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
            #print(statearray.get_bitvector_in_hex())
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

            #XOR The plaintext with the encrypted File
            hexFinal = hexFinal ^ XorAtEnd
            hexFinal.write_to_file(encryptedText)
    encryptedText.close()

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
    for i in range(4):
        for j in range(4):
            hexVector[i][j] = SUBBYTESTABLE[int(hexVector[i][j], 16)]
    return hexVector

def shiftRows(vector, charX):
    shift = 1
    vector = [list(x) for x in zip(vector[0], vector[1], vector[2], vector[3])]
    while(shift < 4):
       vector[shift] = rotateElemList(vector[shift], shift)
       shift+=1
    vector = [list(x) for x in zip(vector[0], vector[1], vector[2], vector[3])]
    return vector

def rotateElemList(listX, shift):
    return listX[shift:] + listX[:shift]

def mixColumns(matrix, charX):
    MIXCOLUMNSE = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    mixColumns = intToBitVector(MIXCOLUMNSE)
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
#Arguments:
# iv: 128-bit initialization vector
# image_file: input .ppm image file name
# out_file: encrypted .ppm image file name
# key_file: String of file name containing encryption key (in ASCII)
#Function Descrption:
# Encrypts image_file using CTR mode AES and writes said file to out_file. No
#required return value.
def ctr_aes_image(iv, image_file,out_file, key_file):
    # Read Key
    READKEY = open(key_file, 'r')
    key = READKEY.read()
    READKEY.close()
    encrypt(key, iv, image_file, out_file)
    return 0