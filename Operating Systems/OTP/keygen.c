#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
  // check args
  if(argc != 2) {
    fprintf(stderr, "Usage: %s keylength\n", argv[0]);
    return 1;
  }

  // convert to int
  int keyLength = atoi(argv[1]);
  if (keyLength <= 0) {
    fprintf(stderr, "Key length must be a positive int\n");
    return 1;
  }

  // gen random number 
  srand(time(NULL));

  // generate and print 
  // random from A - Z
  for(int i = 0; i < keyLength; i++) {
    char randomChar = 'A' + rand() % 26;
    printf("%c", randomChar);
  }

  // new line
  printf("\n");
  return 0;
}
