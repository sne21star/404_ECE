#!/usr/bin/perl -w
use strict;

=description 

  condfilter2.pl

  Another demonstratoin of a very simple condition-line filter for procmail
  by Avi Kak

  This condition-line filter is meant to be used after condfilter1.pl.  If
  spam escapes condfilter1.pl, then this filter will apply another test to
  the body of a potential spam.

  condfilter1.pl is based on the assumption that the spammer has sent a
  multi-part MIME e-mail that has well defined boundaries for ascii text
  and non-ascii material.  That filter declares an e-mail to be spam if the
  ascii partition of the body is empty.

  Some spammers who send non-ascii spam simply do not have multiple
  partitions with well-defined boundaries.  They can just have an text/html
  message encoded in Base64.  This condition-line filter decodes the the
  base64-encoded text/html content.  If this content is shorter than 1000
  bytes, it declares the e-mail to be potentially spam.

=cut

use MIME::Base64;

my $encoded_string = "";
my $decoded_string = "";

my $content_html_flag = 0;
my $encoding_flag = 0;

open LOG, ">> /home/rvl4/a/kak/Mail/log_condfilter2";

#  Change default for output from STDOUT to LOG.  Since this is a condition
#  line filter, its actual output is not of any use to procmail.  Procmail
#  only needs to know whether the program exits with status 0 or a non-zero
#  status.
select LOG;      

print "\n\n";                   # separator for new log entry

while ( <STDIN> ) {
    chomp;
    if ( /^From:/ ) {
        print "$_\n";
        next;
    }
    if ( /^Date:/ ) {
        print "$_\n";
        next;
    }
    if ( /content-type.*text\/html/i ) {
        $content_html_flag = 1;
        next;
    }
    if ( $content_html_flag && /content.*encoding.*base64/i ) {
        $encoding_flag = 1;
        next;
    }        
    next if $content_html_flag == 0;
    next if /^Content-T/;
    next if /^X-/;
    next if /^\s*$/;
    $encoded_string .= $_;

    last if ( /^s*$/ && ( $encoded_string ne "" ) );
}

if ( $encoding_flag == 0 ) {
    print "Exited with non-zero status because no text/html content.\n";
    print "This e-mail will stay in processing stream.\n";
    exit(1);
} else {
    $decoded_string = decode_base64( $encoded_string );
#    print "Decoded string: $decoded_string\n";
    my $length = length( $decoded_string );
    print "length of the decoded string: $length\n";
    if ( $length < 15000 ) {
        print "Exited with status 0 because of short base64-encoded\n";
        print "content. Potential spam\n";
        print "This e-mail will go to junkMail.\n";
        exit(0);
    } else {
        print "text/html encoded content is large. Possible not spam.\n";
        print "Exited with non-zero status.\n";
        print "This e-mail will stay in the processing stream of procmail.\n";
        exit(1);
    }
}

