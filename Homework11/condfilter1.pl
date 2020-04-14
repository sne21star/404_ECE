#!/usr/bin/perl -w
use strict;

=description

  condfilter1.pl

  An example of a simple condition-line filter for procmail by Avi Kak

  This script demonstrates a very simple condition-line filter that either
  succeeds or fails.  It is meant to flag email with zero ascii text in the
  body of the e-mail.  Although legitimate email may also be just HTML
  encoded (and therefore may not have an ascii text part), spam is more
  likely to be characterized by that property.  Spam writer use HTML tags
  to break up words to make it more challenging for the words to be trapped
  by spam filters.  

  A multi-part MIME email is typically characterized by:

  1.  The body of the spam mail contains the following sort of boundary
      lines between the different parts:

      Content-Type: multipart/alternative;
          boundary="----=_NextPart_000_0B27_B38DAF56.204BD5AC"

  2.  The ascii text part, if present, will begin and end with a boundary
      as shown above.  Here is a more precise presentation of the ascii
      part of the e-mail will begin:

          ------=_NextPart_000_0B27_B38DAF56.204BD5AC
          Content-Type: text/plain
          Content-Transfer-Encoding: 8bit

      Note the boundary label attached to the string "_NextPart".

  3.  After that, there could be an HTML-encoded part that would also begin
      and end with this sort of a boundary label.

          ------=_NextPart_000_0B27_B38DAF56.204BD5AC
          Content-Type: text/html
          Content-Transfer-Encoding: base64

      Note the presence of "html" in the value for "Content-Type".

  This condition-line filter assumes that a spammer will not put any words
  in the "text/plan" part of the multi-part message.  So the idea is to
  first extract the boundary string, go from there to the occurrence of the
  boundary string at the beginning of the first part in the "_NextPart"
  string; go from there to the first line containing the string
  "Content-Type: text/plain"; and to then start pushing the ascii message
  lines into the array @body_text.  We continue doing so until we hit the
  next occurrence of the boundary string.  If the resulting array
  @body_text is empty, we know that the e-mail is probably spam.

=cut

my @text_body = ();
my $boundary;
my $ascii_text_flag = 0;
my $content_multipart = 0;

open LOG, ">> /home/rvl4/a/kak/Mail/log_condfilter1";

#  Change default for output from STDOUT to LOG.  Since this is a condition
#  line filter, its actual output is not of any use to procmail.  Procmail
#  only needs to know whether the program exits with status 0 or a non-zero
#  status.

select LOG;      

print "\n\n";                   # separator for new log entry

while ( <STDIN> ) {
#    print " >> $_";
    chomp;

    if ( /^From:/ ) {
        print "$_\n";
        next;
    }
    if ( /^Date:/ ) {
        print "$_\n";
        next;
    }
    if ( /content-type: multipart\/alternative/i ) {
        $content_multipart = 1;
        next;
    }
    if ( $content_multipart && /boundary=\W+(\w+\.?\w*)/ ) {
        $boundary = $1;
        next;
    }
    if ( $boundary && /Content-Type: text\/plain/ ) {
        $ascii_text_flag = 1;
        next;
    }
    next if $ascii_text_flag == 0;
    next if /^Content-T/;
    next if /^[ \t]+charset="/;
    last if /$boundary/;

    push(@text_body, $_) unless $_ eq "";
}

print "Total number of lines examined: $.\n";

if ($ascii_text_flag == 1 && @text_body == 0) {
    print "Exited with status 0 because no ascii message body.\n";
    print "This e-mail will go to junkMail.\n";
    exit(0);
} else {
    my $n = @text_body;
    print "Multipart type ascii message is: @text_body\n";
    print "num of elements in text: $n\n";
    print "Exited with non-zero status because there is ascii content.\n";
    print "This e-mail will stay in processing stream of procmail.\n";
    exit(1);
}
