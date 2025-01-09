#include "global.h"
#include <stdlib.h> // For NULL

#ifndef MAX_WORDS
#define MAX_WORDS 512
#endif

int activeProcesses = 0;
char *words[MAX_WORDS];
int numWords = 0;
int exit_status = 0;
bool should_exit = false;
pid_t last_bg_pid = -1;
int processes[1000];
int numProcesses = 0;
bool is_background = false;
bool redirect_in = false;
bool redirect_out = false;
bool redirect_append = false;
bool allow_background = false;
char* file_in = NULL;
char* file_out = NULL;
char* file_append = NULL;
