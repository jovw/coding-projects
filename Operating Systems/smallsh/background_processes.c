#include "background_processes.h"
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

// Function to manage background processes
void 
manage_background_processes() {
    int status;
    pid_t pid;

    // Check if the processes array is empty
    if (numProcesses == 0) {
        // If no processes to manage, return early
        return;
    }

    // Iterate over the array of processes
    for (int i = 0; i < numProcesses; i++) {
        if (processes[i] != -1) {
          pid = waitpid(processes[i], &status, WNOHANG | WUNTRACED | WCONTINUED);
          if (pid > 0) {
              if (WIFEXITED(status)) {
                  // Process has exited normally
                  fprintf(stderr, "Child process %jd done. Exit status %d.\n", (intmax_t)pid, WEXITSTATUS(status));
                  exit_status = 0;
                  processes[i] = -1; // Mark the process as exited
              } else if (WIFSIGNALED(status)) {
                  // Process was terminated by a signal
                  fprintf(stderr, "Child process %jd done. Signaled %d.\n", (intmax_t)pid, WTERMSIG(status));
                  exit_status = 0;
                  processes[i] = -1; // Mark the process as exited
              } else if (WIFSTOPPED(status)) {
                  // Process was stopped, do not mark as exited
                  fprintf(stderr, "Child process %jd stopped. Continuing.\n", (intmax_t)pid);
                  exit_status = 0;
                  // Do not mark as exited; the process may still resume
              } else if (WIFCONTINUED(status)) {
                  // Process was continued after being stopped
                  fprintf(stderr, "Child process %jd continued.\n", (intmax_t)pid);
                  // Do not mark as exited; it's still running
              }
          } else if (pid == -1 && errno != ECHILD) {
              // Handle waitpid error that's not "No child processes"
              perror("waitpid");
              exit(EXIT_FAILURE);
          }
        }
    }
}