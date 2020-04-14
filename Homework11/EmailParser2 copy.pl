#!/usr/bin/perl -w

### EmailParser.pl
###
### by Avi Kak (kak@purdue.edu)
###
### revised April 3, 2013


=description

To parse an email file, all you have to do is to say

         EmailParser.pl name_of_the_file

The script will deposit the various "parts" of a multipart
email in the 'mimemail' subdirectory of the directory in
which you execute the command.  The email file can even be 
one that has already been processed by the MH mail agent.

You'll be able to run this script only if you have the Perl
module MIME::Parser intalled in your machine.  If you do not
have this module installed and if you do not have root
access to your machine, use the following sequence of steps
to intall the MIME::Parser module from the
http://search.cpan.org/ website in one of your directories:

  perl Makefile.PL prefix=/your/personal/directory/
  make
  make test
  make install

=cut

use strict;
use MIME::Parser;

die "Needs the name of the file in the command line"
    unless @ARGV == 1;

open FILE, shift @ARGV or die "unable to open filename: $!";
my $input = join "", <FILE>;

unless (-e "mimemail") {
    mkdir "mimemail", 0755;
} else {
    # The following step is to just clean up the contents of the
    # mimemail subdirectory where the different parts of the 
    # email being parsed will be deposited:
    print "\nDo you want the current contents of the mimemail directory to be deleted?\n\n" .
          "Enter 'yes' or 'no':  ";
    my $answer = <STDIN>;
    unlink glob "~/mimemail/*" if $answer =~ /yes/;
}

#print "$input\n";
my $mime_parser = MIME::Parser->new( DEBUG => 1);
#$mime_parser->output_dir( "$ENV{HOME}/mimemail" );
$mime_parser->output_dir( "mimemail" );
my $entity = $mime_parser->parse_data( $input );
$entity->dump_skeleton( \*STDERR );
