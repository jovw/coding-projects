#define _POSIX_C_SOURCE 200809L
#include <assert.h>
#include <err.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

// #include "gprintf.h"

#if CHAR_BIT != 8
#error "CHAR_BIT != 8"
#endif

#define ARRAY_LEN(x) (sizeof(x) / sizeof *(x))
// #define TRIBBLE_BIT 3

/* Aye, sir. Before they went into warp, I transported the whole kit 'n'
 * caboodle into their engine room, where they'll be no tribble at all.
 * - Scotty */

static char const b64a[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    "+/";

void 
base64encode(const char *data, size_t n) {
    static const char pad_char = '=';

    for (size_t i = 0; i < n; i += 3) {
        // Collect bytes into a 24-bit word
        unsigned long dword = data[i] << 16;
        if (i + 1 < n) dword |= (data[i + 1] << 8);
        if (i + 2 < n) dword |= data[i + 2];

        // Process each 24-bit word, 6 bits at a time
        for (int j = 0; j < 4; ++j) {
            if ((i * 8 + j * 6) < (n * 8)) {
                int idx = (dword >> (18 - j * 6)) & 0x3F;
                putchar(b64a[idx]);
            } else {
                putchar(pad_char);
            }
        }
    }
    putchar('\n');
}

int
// argc ->
// argv ->
main(int argc, char *argv[])
{
  printf("The base64 alphabet is: %s\n", b64a);
  // cat
  //int i = 1;

  char const *filename;
  FILE *fp;

  if (argc < 2) {
    /* If no FILE, read from standard input */
    filename = "-";
    fp = stdin;
    goto dfl_stdin;
  } else if (argc == 2) {
    filename = argv[1];
    if (strcmp(filename, "-") == 0) {
      fp = stdin;
      goto dfl_stdin;
    } else {
      fp = fopen(filename, "r");
      if (!fp) err(EXIT_FAILURE, "%s", filename);
    }
  } else {
    errx(EXIT_FAILURE, "Usage: %s [FILE]", argv[0]);
  }

  // char buf[BUFSIZ];
  // while (1) {
  //   size_t num = fread(buf, 1, sizeof buf, fp);
  //   if (num < sizeof buf && ferror(fp)) err(EXIT_FAILURE, "%s", filename);
  //   if (num == 0) break;
  //   base64encode(buf, num);
  // }
  
  dfl_stdin:;
    char buf[BUFSIZ];

    for (;;) {
      size_t nr = fread(buf, 1, sizeof buf, fp);
      if (nr < sizeof buf && ferror(stdin)) err(EXIT_FAILURE, "%s", argv[1]);
      if (nr == 0) break; // end of file, empry buf

      size_t nw = fwrite(buf, 1, nr, stdout);
      if (nw < nr) err(EXIT_FAILURE, "stdout");

      if (nr < sizeof buf) break; // end of file, partial buf
    }
    if (fp != stdin)
      fclose(fp);

  fflush(stdout);
  if (ferror(stdout)) err(EXIT_FAILURE, "stdout");

  // assert(0);

  puts("Made it to the end! Goodbye :)");
  return EXIT_SUCCESS;
}