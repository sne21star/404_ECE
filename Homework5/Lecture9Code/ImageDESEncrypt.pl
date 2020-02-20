#!/usr/bin/env perl

##  ImageDESEcrypt.pl

##  Avi Kak
##  February 12, 2015

##  This script uses the DES algorithm in the ECB mode to encrypt an image
##  to demonstrate shortcomings of the ECB.  It is best to call this script
##  on an edge-enhanced image.

##  Call syntax:
##
##     ImageDESEncrypt.pl  input_image.ppm   output.ppm

use strict;                                                                            #(A)
use warnings;
use Crypt::ECB;                                                                        #(B)
use constant BLOCKSIZE => 64;                                                          #(C)

die "Needs two command-line arguments for in-file and out-file"                        #(D)
    unless @ARGV == 2;                                                                 #(E)

my $crypt = Crypt::ECB->new;                                                           #(F)
# It is important to supply the PADDING_NONE option here.  With the other
# option, PADDING_AUTO, it will padd extra 8 bytes to each block of 8 bytes
# I read and feed into the encryption function.  This padding, presumably
# all zeros, probably makes sense when you supply the entire file to the
# encrypt function all at once.
$crypt->padding(PADDING_NONE);                                                         #(G)

$crypt->cipher('DES') || die $crypt->errstring;                                        #(H)
$crypt->key('hello123');                                                               #(I)

open FROM, shift @ARGV or die "unable to open filename: $!";                           #(J)
open TO, ">" . shift @ARGV or die "unable to open filename: $!";                       #(K)
binmode( FROM );                                                                       #(L)
binmode( TO );                                                                         #(M)

my $encrypted = "";                                                                    #(N)
my $total_bytes_read = 0;                                                              #(O)
$|++;                                                                                  #(P)
while (1) {                                                                            #(Q)
    my $num_of_bytes_read = sysread( FROM, my $buff, BLOCKSIZE/8 );                    #(R)
    $total_bytes_read += $num_of_bytes_read;                                           #(S)
    if ($total_bytes_read < 2048) {                                                    #(T)
        $encrypted .= $buff;                                                           #(U)
        next;                                                                          #(V)
    }
    $buff .= '0' x (BLOCKSIZE/8 - $num_of_bytes_read)             
                           if ($num_of_bytes_read < BLOCKSIZE/8);                      #(W)
    $encrypted .= $crypt->encrypt( $buff );                                            #(X)
    print ". " if $total_bytes_read % 2048 == 0;                                       #(Y)
    last if $num_of_bytes_read < BLOCKSIZE/8;                                          #(Z)
}                            
syswrite( TO, $encrypted );                                                            #(a)
