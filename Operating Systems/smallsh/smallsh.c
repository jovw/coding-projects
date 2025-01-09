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

#ifndef MAX_WORDS
#define MAX_WORDS 512
#endif


// Global var
int activeProcesses = 0;
char *words[MAX_WORDS];
int numWords = 0;
int exit_status = 0;
bool should_exit = false;
pid_t last_bg_pid = -1;

// global variables for parsing commands
bool is_background = false;
bool redirect_in = false;
bool redirect_out = false;
bool redirect_append = false;
char* file_in = NULL;
char* file_out = NULL;

// Functions
size_t wordsplit(char const *line);
char * expand(char const *word);
void check_commands();
void handle_exit_call();
void handle_cd_call();
void non_built_in_commands();
void child_fork();
void parent_fork();

int main(int argc, char *argv[])
{
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
prompt:; /* This will allow you to come back to the start of the loop unconditionally */
    /* TODO: Manage background processes */

    /* TODO: prompt */
    if (input == stdin) { // if intput is stdin then interactive, else non-interactive
      // handle the rest of the prompt code here 
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
    //printf("redirect_in is set to: %d before going into check commands\n", redirect_in);
   // printf("Checking commands...\n"); 
    check_commands();

    if (should_exit) {
      break;
    }
  }
  free(line);
  fclose(input);
  exit(exit_status);
}

char *words[MAX_WORDS] = {0};


/* Splits a string into words delimited by whitespace. Recognizes
 * comments as '#' at the beginning of a word, and backslash escapes.
 *
 * Returns number of words parsed, and updates the words[] array
 * with pointers to the words, each as an allocated string.
 */
size_t 
wordsplit(char const *line) {
 // printf("Parsing input line: %s\n", line);
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
      //printf("COMPARING\n");
      // Output or append
      if (*c =='>') {
        //printf("we for a >\n");
        if (c[1] == '>') {
          redirect_append = true;
          c ++;
        } else {
          redirect_out = true;
          //printf("redirect_in is set to: %d\n", redirect_out);
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
        else file_out = fileName; // Handle both redirection out and append the same way for simplicity

        // Reset redirection flags for next iteration if needed
        //redirect_in = redirect_out = redirect_append = false;
        //  continue; // Move to next word or symbol
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
  //printf("redirect_in is still set to: %d\n", redirect_out);
  words[wind] = NULL;
  return wind;
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

void
check_commands() {
  //printf("inside the check commands function\n");
  if(strcmp(words[0], "exit") == 0) {
    handle_exit_call();
  } else if (strcmp(words[0], "cd") == 0) {
      handle_cd_call();
  } else if (strcmp(words[0], "_suspend") == 0 ) {
      printf("Shell suspend operation invoked.\n");
      sleep(5);
      return;
  } else {
      //printf("Moving on to non built in\n");
      non_built_in_commands();
  }
}

void handle_exit_call() {
    // Check if an exit status is provided
    if (numWords > 1) {
        // Convert the exit status argument to an integer
        char *endptr;
        exit_status = (int) strtol(words[1], &endptr, 10);

        // Check if conversion was successful
        if (*endptr != '\0' || errno == ERANGE) {
            exit_status = 1;
        }
    } else {
        exit_status = 0;
    }
    should_exit = true;
}

void 
handle_cd_call() {
  char* path = NULL;
  // if no arg go HOME
  if (numWords == 1) {
    path = getenv("HOME");
    if (!path) {
      fprintf(stderr, "cd: Home not set\n");
      return;
    }
  } else if (numWords == 2) { // if path was provided
    path = words[1];
  } else {
    fprintf(stderr, "cd: too many arguments\n");
    return;
  }

  if (chdir(path) != 0) {
    perror("cd");
  }
}

void
non_built_in_commands() {
 // printf("inside non built in\n");
  pid_t pid;
  pid = fork();

  if (pid == -1) {
    return;
  } else if (pid == 0) {
    //if (is_background) {
      // do something
    //}
   // printf("goign to chilf\n");
    child_fork();
    exit(0);
  } else {
    if (is_background) {
      //printf("Started background process PID: %d\n", pid);
     // last_bg_pid = pid;
     // printf("Set last bg pid: %jd\n", (intmax_t) last_bg_pid);

      // Do not wait for the background process here. Instead, handle it asynchronously.
      // You might want to add the process to a list of background processes if you're tracking them.
    } else {
      int status;
      waitpid(pid, &status, 0);
      if (WIFEXITED(status)) {
        exit_status = WEXITSTATUS(status);
      } else if (WIFSIGNALED(status)) {
        int sig_num = WTERMSIG(status);
       exit_status = 128 + sig_num;
      } else {
        exit_status = 1;
      }
    }
  }
}

void
child_fork() {
  //printf("redirect_out: %d\n", redirect_out);
  //printf("file_out: %s\n", file_out);
  // output redirection and append
  if (redirect_out || redirect_append) {   
    int flags = O_WRONLY | O_CREAT | (redirect_append ? O_APPEND : O_TRUNC); 
    int fd_out = open(file_out, flags, 0777);

    if (fd_out < 0) {
      perror("open");
      exit(1);
    }

    if (dup2(fd_out, STDOUT_FILENO) < 0) {
      perror("dup2");
      exit(1);
    }

    //redirect_out = redirect_append = false;
    //fflush(stdout);
    close(fd_out);
  } 

  // input redirection
  if (redirect_in) {
    //printf("%s", file_in);
    int fd_in = open(file_in, O_RDONLY);

    if (fd_in < 0) {
      perror("open");
      exit(1);
    }

    if (dup2(fd_in, STDIN_FILENO) < 0) {
      perror("dup2");
      exit(1);
    }
   // redirect_in = false;
    close(fd_in);
  } 

  //handle non-built-in and non-directional commands
  if (execvp(words[0], words) < 0) {
    perror("execvp");
    fflush(stdout);
    exit(1);
  }
}


