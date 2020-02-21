#!/usr/bin/perl -w

##  UsingDevRandom.pl
##  Avi Kak 
##  April 22, 2013

use strict;

open FROM, "/dev/random" or die "unable to open file: $!";
binmode FROM;
for (;;) {
    my $entropy = 0;
    for (;;) {
        $entropy = `cat /proc/sys/kernel/random/entropy_avail`;
#       last if $entropy > 128;
        last if $entropy > 32;
        sleep 1;
    }
    my $pool_size = `cat /proc/sys/kernel/random/poolsize`;
    my $how_many_bytes_read = sysread(FROM, my $bytes, 16);
    print "Number of bytes read: $how_many_bytes_read\n";
    my @bytes  = unpack 'C*', $bytes;
    my $hex = join ' ', map sprintf("%x", $_), @bytes;
    my $output = sprintf "Entropy Available: %-4d    Pool Size: %-4d      Random Bytes in Hex: $hex", 
                 $entropy, $pool_size;
    print "$output\n\n\n";
    sleep 1;
}
