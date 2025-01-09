#include "command_executor.h"
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

void
check_commands() {
  if(words[0] != NULL && strcmp(words[0], "exit") == 0) {
    handle_exit_call();
  } else if (words[0] != NULL && strcmp(words[0], "cd") == 0) {
      handle_cd_call();
  } else {
      non_built_in_commands();
  }
  is_background = false;
}

void 
handle_exit_call() {
    // Check if an exit status is provided
    if (numWords > 2) {
        // Too many arguments provided
        fprintf(stderr, "Too many arguments for exit command\n");
        exit_status = 1;
    } else if (numWords == 2) {
        // Convert the exit status argument to an integer
        char *endptr;
        exit_status = (int) strtol(words[1], &endptr, 10);

        // Check if conversion was successful
        if (*endptr != '\0' || errno == ERANGE) {
            // Conversion failed
            fprintf(stderr, "Invalid argument for exit command\n");
            exit_status = 1;
        }
    } else {
        // No exit status provided
        char last_exit_status_str[20];
        sprintf(last_exit_status_str, "%d", exit_status);
        char* last_exit_status_expanded = expand(last_exit_status_str);
        exit_status = atoi(last_exit_status_expanded);
        free(last_exit_status_expanded);
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
  pid_t pid;
  pid = fork();
  // keep track of all processes runnning
  processes[numProcesses] = pid;
  numProcesses ++;

  if (pid == -1) {
    // NEW
    perror("fork()");
    exit(1);
    return;
  } else if (pid == 0) {
    child_fork(); 
    exit(0);
  } else {
    if (is_background) {
      last_bg_pid = pid;
    } else {
      parent_fork(pid);
    }
  }
}

void
child_fork() {
  struct sigaction SIGINT_action = {0};

  if (!is_background) {
  SIGINT_action.sa_handler = SIG_DFL; // Default action for SIGINT
  sigaction(SIGINT, &SIGINT_action, NULL);
  } else {
    SIGINT_action.sa_handler = SIG_IGN; // Ignore SIGINT for background processes
    sigaction(SIGINT, &SIGINT_action, NULL);
  }

  redirect_in = redirect_out = redirect_append = false;

  // output redirection
  if (file_out != NULL && (strcmp(words[0], "printf") == 0)) {   

    int flags = O_WRONLY | O_CREAT | O_TRUNC;

    int fd_out = 0;
    if ((fd_out = open(file_out, flags, 0777)) < 0) {
      fflush(stdout);
      exit(1);
    }

    // dup2(fd_out, 1);
    if (dup2(fd_out, 1) < 0) {
      perror("dup2");
      exit(1);
    }
    close(fd_out);
    free(file_out);
    file_out = NULL;
  }

  // input redirection
  if (file_in != NULL) {
    int fd_in = open(file_in, O_RDONLY);

    if (fd_in < 0) {
      perror("open");
      exit(1);
    }

    if (dup2(fd_in, STDIN_FILENO) < 0) {
      perror("dup2");
      exit(1);
    }
    close(fd_in);
    free(file_in);
    file_in = NULL;
  } 

  if (file_append != NULL && (strcmp(words[0], "printf") == 0)) {   

    int flags = O_WRONLY | O_CREAT | O_APPEND;

    int fd_append = 0;
    if ((fd_append = open(file_append, flags, 0777)) < 0) {
      fprintf(stderr, "cannot open %s for append\n", file_append);
      fflush(stdout);
      exit(1);
    }

    if (dup2(fd_append, 1) < 0) {
      perror("dup2");
      exit(1);
    }
    close(fd_append);
    free(file_append);
    file_append = NULL;
  }

  if (execvp(words[0], words) < 0) {
    perror("execvp");
    fflush(stdout);
    exit(1);
  }
}

void 
parent_fork(pid_t childPid) {
  int status;

  if (is_background) {
    waitpid(childPid, &status, WNOHANG);
    fflush(stdout);
  } else {
    waitpid(childPid, &status, 0);
  }

  if (WIFEXITED(status)) {
    exit_status = WEXITSTATUS(status);
  } else if (WIFSIGNALED(status)) {
    int sig_num = WTERMSIG(status);
    exit_status = 128 + sig_num;
  } else {
    exit_status = 1;
  }
}