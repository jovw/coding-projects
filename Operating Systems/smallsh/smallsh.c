#define _POSIX_C_SOURCE 200809L
#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <err.h>
#include <errno.h>
#include <unistd.h>
#include <ctype.h>
#include <string.h>
#include <sys/wait.h>
#include <stdbool.h>
#include <fcntl.h>
#include <stdint.h>
#include <string.h>
#include <signal.h>

#include "signal_handlers.h"
#include "command_parser.h"
#include "command_executor.h"
#include "background_processes.h"
#include "global.h"

#ifndef MAX_WORDS
#define MAX_WORDS 512
#endif


int main(int argc, char *argv[])
{
  init_signal_handlers();

  FILE *input = stdin;
  char *input_fn = "(stdin)";
  if (argc == 2) {
    input_fn = argv[1];
    input = fopen(input_fn, "re"); /* e char -> indicated to use the O_CLOEXEC flag when opening file */
    if (!input) err(1, "%s", input_fn);
  } else if (argc > 2) {
    errx(1, "too many arguments");
  }

  char *line = NULL;
  size_t n = 0; /* hold the len of &line */
  for (;;) {
prompt:; 
    manage_background_processes();

    if (input == stdin) { // if intput is stdin then interactive, else non-interactive
      if (isatty(STDIN_FILENO)) { // Check if in interactive mode
        char* ps1 = getenv("PS1");
        if (!ps1) ps1 = ":"; // Default prompt if PS1 is not set
        fprintf(stderr, "%s ", ps1);
        fflush(stderr);
      }
    }

    /* 1. Reading a line of input with getline :Man getline
    * getline is implemented on input - which at this point is either stdin or file content
    */
    ssize_t line_len = getline(&line, &n, input);
    if (line_len < 0) {
      if (feof(input)) {
        break;
      } else {
        err(1, "%s", input_fn);
      }
    }
    /* 2. Word splitting*/
    /* 3. Expansion */
    numWords = 0;
    size_t nwords = wordsplit(line);
    for (size_t i = 0; i < nwords; ++i) {
      char *exp_word = expand(words[i]);
      free(words[i]);
      words[i] = exp_word;
    }
    
    /* Run the command */
    if (words[0] != NULL) {
      check_commands();
    }

    if (should_exit) {
      manage_background_processes();
      break;
    }
  }
  //free(line);
  fclose(input);
  exit(exit_status);
}
