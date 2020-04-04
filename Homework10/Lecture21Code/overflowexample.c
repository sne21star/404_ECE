
// overflowexample.c

#include <stdio.h>

void proc(char* str, int a, int b)
{
  char buf[50];
  strcpy(buf, str);
}

int main(int argc, char* argv[])
{
  if(argc > 1)
    proc(argv[1], 1, 2);
  printf("%s\n", argv[1]);
  return 0;
}
