#include "command_parser.h"
#include "global.h"
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

#ifndef MAX_WORDS
#define MAX_WORDS 512
#endif

/* Splits a string into words delimited by whitespace. Recognizes
 * comments as '#' at the beginning of a word, and backslash escapes.
 *
 * Returns number of words parsed, and updates the words[] array
 * with pointers to the words, each as an allocated string.
 */
size_t 
wordsplit(char const *line) {
  size_t wlen = 0;
  size_t wind = 0;

  char const *c = line;
  for (;*c && isspace(*c); ++c); /* discard leading space */

  if (*c == '#') return 0;

  for (; *c;) {
    if (wind == MAX_WORDS) break;
    if (*c == '#') break;
    
    // check for redirection
    if (*c == '>' || *c == '<' || *c == '&' || (c[0] == '>' && c[1] == '>')){
      // Output or append
      if (*c =='>') {
        if (c[1] == '>') {
          redirect_append = true;
          c ++;
        } else {
          redirect_out = true;
        }
      } else if (*c == '<') { 
        redirect_in = true;     
      } else if (*c == '&') {
        is_background = true;
      }

      c++;
      while (*c && isspace(*c)) c++;
      
      if (redirect_in || redirect_out || redirect_append) {
        const char *fileNameStart = c;
        while (*c && !isspace(*c) && *c != '>' && *c != '<' && *c != '&') c++; // File name ends

        size_t fileNameLen = c - fileNameStart;
        char *fileName = malloc(fileNameLen + 1);
        strncpy(fileName, fileNameStart, fileNameLen);
        fileName[fileNameLen] = '\0';

        if (redirect_in) file_in = fileName;
        else if (redirect_out) file_out = fileName;
        else file_append = fileName;

        // Reset redirection flags for next iteration if needed
        redirect_in = redirect_out = redirect_append = false;
          continue; // Move to next word or symbol
      }
    }

    // no redirection 
    for (;*c && !isspace(*c) && *c != '>' && *c != '<' && *c != '&'; ++c) {
      if (*c == '\\') {
        if (*(c + 1) == 'n') {
          words[wind][wlen++] = '\n';
          ++c;
        }
        ++c;
      }
      /* store realloc in temp var, make sure it is not nul, and then set a new var to temp
       * This is for error handling */
      void *tmp = realloc(words[wind], sizeof **words * (wlen + 2));
      if (!tmp) err(1, "realloc");
      words[wind] = tmp;
      words[wind][wlen++] = *c; 
      words[wind][wlen] = '\0';
    }

    if (wlen > 0) {
      ++wind;
      wlen = 0;
    }
    for (;*c && isspace(*c); ++c);
    numWords ++; 
  }
  words[wind] = NULL;
  return wind;
}

/* Expands all instances of $! $$ $? and ${param} in a string 
 * Returns a newly allocated string that the caller must free
 */
char *
expand(char const *word)
{
  char const *pos = word;
  char const *start, *end;
  char c = param_scan(pos, &start, &end);
  char pid_str[20];
  char status_str[20];
  build_str(NULL, NULL);
  build_str(pos, start);
  while (c) {
    if (c == '!') {
      if (last_bg_pid != -1) {
        sprintf(pid_str, "%d", last_bg_pid);
        build_str(pid_str, NULL);
      } else {
        build_str("", NULL);
      }
    }
    else if (c == '$') {
      sprintf(pid_str, "%d", getpid());
      build_str(pid_str, NULL);
    }
    else if (c == '?') {
      sprintf(status_str, "%d", exit_status);
      build_str(status_str, NULL);
    }
    else if (c == '{') {
      char *param_name = strndup(start + 2, end - start - 3);
      char *param_value = getenv(param_name);
      if (param_value){
        build_str(param_value, NULL);
      } else {

      }
      free(param_name);
    }
    pos = end;
    c = param_scan(pos, &start, &end);
    build_str(pos, start);
  }
  return build_str(start, NULL);
}

/* Find next instance of a parameter within a word. Sets
 * start and end pointers to the start and end of the parameter
 * token.
 */
char
param_scan(char const *word, char const **start, char const **end)
{
  static char const *prev;
  if (!word) word = prev;
  
  char ret = 0;
  *start = 0;
  *end = 0;
  for (char const *s = word; *s && !ret; ++s) {
    s = strchr(s, '$');
    if (!s) break;
    switch (s[1]) {
    case '$':
    case '!':
    case '?':
      ret = s[1];
      *start = s;
      *end = s + 2;
      break;
    case '{':;
      char *e = strchr(s + 2, '}');
      if (e) {
        ret = s[1];
        *start = s;
        *end = e + 1;
      }
      break;
    }
  }
  prev = *end;
  return ret;
}

/* Simple string-builder function. Builds up a base
 * string by appending supplied strings/character ranges
 * to it.
 */
char *
build_str(char const *start, char const *end)
{
  static size_t base_len = 0;
  static char *base = 0;

  if (!start) {
    /* Reset; new base string, return old one */
    char *ret = base;
    base = NULL;
    base_len = 0;
    return ret;
  }
  /* Append [start, end) to base string 
   * If end is NULL, append whole start string to base string.
   * Returns a newly allocated string that the caller must free.
   */
  size_t n = end ? end - start : strlen(start);
  size_t newsize = sizeof *base *(base_len + n + 1);
  void *tmp = realloc(base, newsize);
  if (!tmp) err(1, "realloc");
  base = tmp;
  memcpy(base + base_len, start, n);
  base_len += n;
  base[base_len] = '\0';

  return base;
}