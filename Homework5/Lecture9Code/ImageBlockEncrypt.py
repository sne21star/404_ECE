#!/usr/bin/env python

##  ImageBlockEcrypt.py

##  Avi Kak (February 11, 2016)

##  Each block of bits read from the image file is represented as an instance of the
##  Python BitVector class.

##  The block encryption used here is based on a random permutation of the bits in
##  the source file.  For a receiving party to decrypt the information, you will have
##  to send them the key file that is created in line (K).

##  Call syntax:
##
##     ImageBlockEncrypt.py  input_image.ppm   output.ppm

import sys
import random
from BitVector import *                                                              #(A)

if len(sys.argv) is not 3:                                                           #(B)
    sys.exit('''Needs two command-line arguments, one for '''
	     '''the source image file and the other for the '''
	     '''encrypted output file''')
    
BLOCKSIZE = 64                                                                       #(C)
inputfile = sys.argv[1]                                                              #(D)
TO = open(sys.argv[2], 'w')                                                          #(E)

# Open `keyfile.txt' so that you can write the permutaiton order into the
# file (this serves as our "encryption key"):
KEYFILE = open("keyfile.txt", 'w')                                                   #(F)
permuted_indices = range(BLOCKSIZE)                                                  #(G)
# Now create a random permutation of the bit positions.  We will use this
# method for encryption in this script.  If you had to represent the
# permutations as an encryption key, that would be a very long key indeed.
random.shuffle(permuted_indices)                                                     #(H)
KEYFILE.write(str(permuted_indices))                                                 #(I)
KEYFILE.close()                                                                      #(J)

# Let's now start scanning the input file and encrypting it by permuting
# the bits in each block:
j = 0                                                                                #(K)
bv = BitVector( filename = inputfile )                                               #(L)
while bv.more_to_read:                                                               #(M)
    if j %1000 == 0:                                                                 #(N)
        print ".",                                                                   #(O)
        sys.stdout.flush()                                                           #(P)
    bv_read = bv.read_bits_from_file( BLOCKSIZE )                                    #(Q)
    j += 1                                                                           #(R)
    if j < 2048:                                                                     #(S)
        bv_read.write_to_file( TO )                                                  #(T)
        continue                                                                     #(U)
    if bv_read.length() < BLOCKSIZE:                                                 #(V)
        bv_read.pad_from_right(BLOCKSIZE - bv_read.length())                         #(W)
    permuted_bitvec = bv_read.permute( permuted_indices )                            #(X)
    permuted_bitvec.write_to_file( TO )                                              #(Y)
bv.close_file_object();                                                              #(Z)
TO.close()
