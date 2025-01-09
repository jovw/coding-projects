#ifndef GLOBALS_H
#define GLOBALS_H

#include <stdbool.h>
#include <sys/types.h>

extern int activeProcesses;
extern char *words[];
extern int numWords;
extern int exit_status;
extern bool should_exit;
extern pid_t last_bg_pid;
extern int processes[];
extern int numProcesses;
extern bool is_background;
extern bool redirect_in;
extern bool redirect_out;
extern bool redirect_append;
extern bool allow_background;
extern char* file_in;
extern char* file_out;
extern char* file_append;

#endif
