#include <stdio.h>
#include <stdlib.h>

void logint(int i) {
  printf("test: %i\n", i);
}

void alloc_one() {
  malloc(1);
}
