// ex.c

// This example is used in Section 21.4 of Lecture 21 to illustrate 
// the concepts of stack frames on the call stack.

#include <stdio.h>

int main() {
    int x = foo( 10 );
    printf( "the value of x = %d\n", x );
    return 0;
}
int foo( int i ) {
    int ii = i + i;
    int iii = bar( ii );
    int iiii = 2 * iii;
    return iiii;
}
int bar( int j ) {
    int jj = j + j;
    return jj;
}
