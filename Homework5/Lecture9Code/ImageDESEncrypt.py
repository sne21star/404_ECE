#!/usr/bin/env python

##  ImageDESEcrypt.py

##  Avi Kak
##  February 11, 2016

##  This script uses the DES algorithm in the ECB mode to encrypt an image
##  to demonstrate shortcomings of the ECB.  It is best to call this script
##  on an edge-enhanced image.

##  Call syntax:
##
##     ImageDESEncrypt.py  input_image.ppm   output.ppm


import sys
from Crypto.Cipher import DES                                                          #(A)

if len(sys.argv) is not 3:                                                             #(B)
    sys.exit('''Needs two command-line arguments, one for '''
             '''the source image file and the other for the '''
             '''encrypted output file''')

BLOCKSIZE = 64                                                                         #(C)
        
cipher = DES.new(b'hello123', DES.MODE_ECB)                                            #(D)

FROM = open(sys.argv[1], 'rb')                                                         #(E)
TO = open(sys.argv[2], 'wb')                                                           #(F)

end_of_file = None                                                                     #(G)
total_bytes_read = 0                                                                   #(H)
while True:                                                                            #(I)
    bytestring = ''                                                                    #(J)
    for i in range(BLOCKSIZE // 8):                                                    #(K)
        byte = FROM.read(1)                                                            #(L)
        if byte == '':                                                                 #(M)
            end_of_file = True                                                         #(N)
            break                                                                      #(O)
        else:
            total_bytes_read += 1                                                      #(P)
            bytestring += byte                                                         #(Q)
    if end_of_file:                                                                    #(R)
        bytestring += '0' * (8 - total_bytes_read % 8)                                 #(S)
    cipherout = cipher.encrypt(bytestring) if total_bytes_read >= 2048 else bytestring #(T)
    TO.write(cipherout)                                                                #(U)
    if end_of_file: break                                                              #(V)
    if total_bytes_read %2048 == 0:                                                    #(W)
        print ".",                                                                     #(Y)
        sys.stdout.flush()                                                             #(Z)
TO.close()    

