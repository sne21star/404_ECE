"""
Homework Number: 2
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: 01/30/2020
"""
#!/usr/bin/env python
#!/usr/bin/env python -W ignore::DeprecationWarning
### hw2_starter.py
import codecs
import sys
import io
import numpy
import BitVector
#from get_encryption_key import *
from math import *
from generate_round_keys import *
from illustrate_des_substitution import *

expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]
SIZE = 64
def encrypt():

    FILEREAD = open(sys.argv[3], 'r')
    key = FILEREAD.read()
    FILEREAD.close()

    image = open(sys.argv[2], 'rb')
    imageno = image.readline()
    height = image.readline()
    width = image.readline()
    bv = BitVector(filename=sys.argv[2])
    image.close()

    keyBit = get_encryption_key(key)
    round_key = generate_round_keys(keyBit)

    text_file = open(sys.argv[4], "wb")
    text_file.write(imageno)
    text_file.write(height)
    text_file.write(width)
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file(SIZE)
        if (len(str(bitvec)) % SIZE != 0):
            x = bitvec.length() % 64
            bitvec.pad_from_right(SIZE - x)
            print(bitvec)
            print(bitvec.length())
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
        bitX.write_to_file(text_file)
    text_file.close()
    pass

def main():
    encrypt()
    pass

if __name__ == "__main__":
    main()
#Convert Image to Bit vector and get rid of first three lines