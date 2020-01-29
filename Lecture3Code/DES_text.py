"""
Homework Number: 2
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: 01/30/2020
"""
# !/usr/bin/env python
# !/usr/bin/env python -W ignore:tostring:DeprecationWarning
### DES_text.py
import codecs
import sys
import BitVector
# from get_encryption_key import *
from generate_round_keys import *
from illustrate_des_substitution import *
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17,18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]
p_box_permutation = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]
SIZE = 64

def encrypt():
    FILEREAD = open(sys.argv[4], 'r')
    key = FILEREAD.read()
    FILEREAD.close()
    keyBit = get_encryption_key(key)
    round_key = generate_round_keys(keyBit)
    bv = BitVector(filename=sys.argv[3])
    text_file = open(sys.argv[5], "w")
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file(SIZE)
        if (len(str(bitvec)) % SIZE != 0):
            x = bitvec.length() % SIZE
            bitvec.pad_from_right(SIZE-x)
        if (len(str(bitvec)) > 0):
            [LE, RE] = bitvec.divide_into_two()
            for keyR in round_key:
                temp = RE
                newRE = RE.permute(expansion_permutation)
                out_xor = newRE ^ keyR
                output = substitute(out_xor)
                round_i = output.permute(p_box_permutation)
                LE = LE ^ round_i
                RE = LE
                LE = temp
        bitX = RE + LE
        myhexstring = bitX.get_bitvector_in_hex()
        text_file.write(myhexstring)
    text_file.close()
    pass


def decrypt():
    FILEREAD = open(sys.argv[4], 'r')
    key = FILEREAD.read()
    FILEREAD.close()
    keyBit = get_encryption_key(key)
    round_key = generate_round_keys(keyBit)
    round_key = round_key[::-1]

    FILEHEX = open(sys.argv[3], 'r')
    hexString = FILEHEX.read()
    bv = BitVector(hexstring=hexString)

    bvList = list(bv)
    FILEHEX.close()

    text_file = open(sys.argv[5], "w")

    secOfBits = bv.length() / SIZE
    index = 0
    index1 = 0
    totalList = []
    while (index < secOfBits):
        bitvec = BitVector(bitlist=bvList[index1:index1 + SIZE])
        [LE, RE] = bitvec.divide_into_two()
        for keyR in round_key:
            temp = RE
            newRE = RE.permute(expansion_permutation)
            out_xor = newRE ^ keyR
            output = substitute(out_xor)
            round_i = output.permute(p_box_permutation)
            LE = round_i ^ LE
            RE = LE
            LE = temp
        bitX = RE + LE
        if(secOfBits - index == 1):
            strX =bitX.get_text_from_bitvector()
            strC = list(strX)
            for k in strC:
                if(k.isprintable()):
                    text_file.write(k)
        else:
            text_file.write(bitX.get_text_from_bitvector())
        index += 1
        index1 += SIZE
    text_file.close()
    pass

def main():
    charX = sys.argv[2]
    if (charX == '-e'):
        encrypt()
    elif (charX == '-d'):
        decrypt()
    else:
        print("Either -e or -d")
    pass


if __name__ == "__main__":
    main()
# Convert Image to Bit vector and get rid of first three lines
