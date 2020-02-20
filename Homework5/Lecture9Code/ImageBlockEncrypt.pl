#!/usr/bin/env perl

##  ImageBlockEcrypt.pl

##  Avi Kak (February 13, 2015)

##  Each block of bits read from the image file is represented as an instance
##  of the following class:
##
##             Algorithm::BitVector
##
##  that you can download from the CPAN archive at 
##
##  http://search.cpan.org/~avikak/Algorithm-BitVector-1.21/lib/Algorithm/BitVector.pm

##  The block encryption used here is based on a random permutation of the
##  bits in the source file.  For a receiving party to decrypt the
##  information, you will have to send them the key file that is created in
##  line (K).

##  Call syntax:
##
##     ImageBlockEncrypt.pl  input_image.ppm   output.ppm

use strict;
use warnings;
use Algorithm::BitVector;                                                            #(A)
use constant BLOCKSIZE => 64;                                                        #(B)

die "Needs two command-line arguments for in file and out file"                      #(C)
    unless @ARGV == 2;                                                               #(D)
$|++;                                                                                #(E)

my $inputfile = shift;                                                               #(F)
open my $TO, ">" . shift @ARGV or die "unable to open filename: $!";                 #(G)

# Open `keyfile.txt' so that you can write the permutaiton order into the
# file (this serves as our "encryption key"):
open KEYFILE, "> keyfile.txt";                                                       #(H)
my @permute_indices = 0..BLOCKSIZE-1;                                                #(I)
# Now create a random permutation of the bit positions.  We will use this
# method for encryption in this script.  If you had to represent the
# permutations as an encryption key, that would be a very long key indeed.
fisher_yates_shuffle( \@permute_indices );                                           #(J)
print KEYFILE "@permute_indices";                                                    #(K)
close KEYFILE;                                                                       #(L)

# Let's now start scanning the input file and encrypting it by permuting
# the bits in each block:
my $j = 0;
my $bv = Algorithm::BitVector->new( filename => $inputfile );                        #(M)
while ($bv->{more_to_read}) {                                                        #(N)
    print "." if $j % 1000 == 0;                                                     #(O)
    my $bv_read = $bv->read_bits_from_file( BLOCKSIZE );                             #(P)
    if ($j++ < 2048) {                                                               #(Q)
        $bv_read->write_to_file( $TO );                                              #(R)
        next;
    }
    if ($bv_read->length() < BLOCKSIZE) {                                            #(S)
        $bv_read->pad_from_right(BLOCKSIZE - $bv_read->length());                    #(T)
    }
    my $permuted_bitvec = $bv_read->permute(\@permute_indices );                     #(U)
    $permuted_bitvec->write_to_file( $TO );                                          #(V)
}                                                                                    #(W)
$bv->close_file_handle();                                                            #(X)

sub fisher_yates_shuffle {                                                           #(Y)
    my $arr =  shift;                                                                #(Z)
    my $i = @$arr;                                                                   #(a)
    while (--$i) {                                                                   #(b)
        my $j = int rand( $i + 1 );                                                  #(c)
        @$arr[$i, $j] = @$arr[$j, $i];                                               #(d)
    }
}

