"""
Homework Number: 5
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: 02/25/2020
"""
#I AM USING PYTHON3
#!/usr/bin/env python3
from sys import *
from BitVector import *
'''
Computer Timing : 597 seconds ~ 9 minutes and 57 seconds
'''
KEY_SCHEDULE = []
class Const(object):
    SIZE = 256
    SIZEPLAIN = 128
    FOUR = 4
    EIGHT = 8
    AES_MODULUS = BitVector(bitstring='100011011')
    BV_ONE = BitVector(intVal=1, size=8)
    BV_TWO = BitVector(intVal=2, size=8)
    BV_THREE = BitVector(intVal=3, size=8)
    SUBBYTESTABLE = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201,
                              125, 250, 89, 71, 240,
                              173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229,
                              241, 113, 216, 49, 21,
                              4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27,
                              110, 90, 160, 82, 59,
                              214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76,
                              88, 207, 208, 239, 170,
                              251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56,
                              245, 188, 182, 218, 33,
                              16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
                              96, 129, 79, 220, 34,
                              42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194,
                              211, 172, 98, 145, 149, 228,
                              121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120,
                              37, 46, 28, 166, 180,
                              198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87,
                              185, 134, 193, 29, 158,
                              225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137,
                              13, 191, 230, 66, 104,
                              65, 153, 45, 15, 176, 84, 187, 22]

def encrypt(key, v0, image_file, out_file):
    # Create Key Schedule
    KEY_SCHEDULE = keyInit(key)
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
    #read header
    bv.read_bits_from_file(Const.SIZEPLAIN - 16)
    while(bv.more_to_read):
        #Get 128 Bit for Plain Text and Ignore the header
        XorAtEnd = bv.read_bits_from_file(Const.SIZEPLAIN)

        #If block is < 128, pad zeroes
        if (len(str(XorAtEnd)) % Const.SIZEPLAIN != 0):
            XorAtEnd.pad_from_right(Const.SIZEPLAIN-(XorAtEnd.length() % Const.SIZE))

        #THE BITVECTOR IS INTIALIZED BITVECTOR INCREMENT IF NECESSARY
        index += 1
        vX = v0.int_val()
        vX += index
        vX = BitVector(intVal=vX)
        bitvec = vX

        # First Add Round Key
        #firstwordsHex = BitVector(hexstring = first_words)
        bitvec = bitvec ^ KEY_SCHEDULE[0]
        numRounds = 1

        while(numRounds < 14):
            #Turn Bit vector into State Array
            statearray = matrixArray(bitvec)

            # SubBytes
            statearray = substitution(statearray)

            # ShiftRows
            statearray = shiftRows(statearray)

            # Mix Columns  --> Not on last round
            statearray = mixColumns(statearray)
            hexFinal = bitToHex(statearray)

            # Add Round Keys
            bitvec = hexFinal ^ KEY_SCHEDULE[numRounds]
            numRounds += 1
        #Turn Bit vector into State Array
        statearray = matrixArray(bitvec)

        # SubBytes
        statearray = substitution(statearray)

        # ShiftRows
        statearray = shiftRows(statearray)

        hexFinal = bitToHex(statearray)

        #Add RoundKey
        hexFinal = hexFinal ^ KEY_SCHEDULE[numRounds]

        #XOR The plaintext with the encrypted File
        hexFinal = hexFinal ^ XorAtEnd
        hexFinal.write_to_file(encryptedText)
    encryptedText.close()

def bitToHex(matrix):
    returnMatrix = BitVector(size=0)
    for i in range(4):
        for j in range(4):
            returnMatrix += matrix[i][j]
    return returnMatrix

def matrixArray(bitvec):
    bitvecHex = list(bitvec.get_bitvector_in_hex())
    statearray = [[0 for x in range(4)] for x in range(4)]
    index = 0
    for i in range(4):
        for j in range(4):
            statearray[i][j] = bitvecHex[index] + bitvecHex[index+1]
            index += 2
    return statearray

def substitution(hexVector):
    for i in range(4):
        for j in range(4):
            hexVector[i][j] = BitVector(intVal=Const.SUBBYTESTABLE[int(hexVector[i][j], 16)], size = 8)
    return hexVector

def shiftRows(vector):
    shift = 1
    vector = [list(x) for x in zip(vector[0], vector[1], vector[2], vector[3])]
    while(shift < 4):
       vector[shift] = vector[shift][shift:] + vector[shift][:shift]
       shift+=1
    vector = [list(x) for x in zip(vector[0], vector[1], vector[2], vector[3])]
    return vector

def mixColumns(matrix):
                  #[[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    mixColumns = [[Const.BV_TWO, Const.BV_THREE, Const.BV_ONE, Const.BV_ONE], [Const.BV_ONE, Const.BV_TWO, Const.BV_THREE, Const.BV_ONE], [Const.BV_ONE, Const.BV_ONE, Const.BV_TWO, Const.BV_THREE], [Const.BV_THREE, Const.BV_ONE, Const.BV_ONE, Const.BV_TWO]]
    matrix = [list(x) for x in zip(matrix[0], matrix[1], matrix[2], matrix[3])]
    endMatrix = [[0 for x in range(4)] for x in range(4)]
    for i in range(4):
        for j in range(4):
            bitvec0 = (mixColumns[i][0]).gf_multiply_modular(matrix[0][j], Const.AES_MODULUS, 8)
            bitvec1 = (mixColumns[i][1]).gf_multiply_modular(matrix[1][j], Const.AES_MODULUS, 8)
            bitvec2 = (mixColumns[i][2]).gf_multiply_modular(matrix[2][j], Const.AES_MODULUS, 8)
            bitvec3 = (mixColumns[i][3]).gf_multiply_modular(matrix[3][j], Const.AES_MODULUS, 8)
            endMatrix[i][j] = bitvec0 ^ bitvec1 ^ bitvec2 ^ bitvec3
    endMatrix = [list(x) for x in zip(endMatrix[0], endMatrix[1], endMatrix[2], endMatrix[3])]
    return endMatrix

def keyInit(key):
    key_words = []
    key = key.strip()
    key += '0' * (Const.SIZE // Const.EIGHT - len(key)) if len(key) < Const.SIZE // Const.EIGHT else key[:Const.SIZE // Const.EIGHT]
    key_bv = BitVector(textstring=key)
    key_words = gen_key_schedule_256(key_bv)

    key_schedule = []

    enumkey_word = enumerate(key_words)
    for word_index, word in enumkey_word:
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i * Const.EIGHT:i * Const.EIGHT + Const.EIGHT].intValue())
        key_schedule.append(keyword_in_ints)
    num_rounds = 14
    round_keys = [None for i in range(num_rounds + 1)]
    for i in range(num_rounds + 1):
        round_keys[i] = (key_words[i * 4] + key_words[i * 4 + 1] + key_words[i * 4 + 2] + key_words[i * 4 + 3])
    return round_keys

def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << Const.EIGHT
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[Const.EIGHT*i:Const.EIGHT*i+Const.EIGHT].intValue()], size = Const.EIGHT)
    newword[:Const.EIGHT] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(Const.BV_TWO, Const.AES_MODULUS, Const.EIGHT)
    return newword, round_constant
def gen_key_schedule_256(key_bv):
    byte_sub_table = Const.SUBBYTESTABLE
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = Const.BV_ONE
    for i in range(Const.EIGHT):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(Const.EIGHT,60):
        if i%Const.EIGHT == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-Const.EIGHT] ^ kwd
        elif (i - (i//Const.EIGHT)*Const.EIGHT) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//Const.EIGHT)*Const.EIGHT) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal =
                                 byte_sub_table[key_words[i-1][Const.EIGHT*j:Const.EIGHT*j+Const.EIGHT].intValue()], size = Const.EIGHT)
            key_words[i] ^= key_words[i-Const.EIGHT]
        elif ((i - (i//Const.EIGHT)*Const.EIGHT) > 4) and ((i - (i//Const.EIGHT)*Const.EIGHT) < Const.EIGHT):
            key_words[i] = key_words[i-Const.EIGHT] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words
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
