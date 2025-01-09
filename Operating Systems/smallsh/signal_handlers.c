#include "signal_handlers.h"
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
handle_SIGINT(int signo) {
    char* message = "\nTerminated by signal 2\n";
    write(STDOUT_FILENO, message, 23); // Using write for async-signal safety
}

void 
handle_SIGTSTP(int signo) {
    if (allow_background) {
        char* message = "\nEntering foreground-only mode (& is now ignored)\n";
        write(STDOUT_FILENO, message, 50);
        allow_background = false;
    } else {
        char* message = "\nExiting foreground-only mode\n";
        write(STDOUT_FILENO, message, 30);
        allow_background = true;
    }
}

void 
init_signal_handlers() {
    struct sigaction SIGINT_action = {0}, SIGTSTP_action = {0};

    // SIGINT should be ignored by the shell itself, only child processes should be affected
    SIGINT_action.sa_handler = SIG_IGN;
    sigfillset(&SIGINT_action.sa_mask);
    SIGINT_action.sa_flags = 0;
    sigaction(SIGINT, &SIGINT_action, NULL);

    // SIGTSTP toggles background process allowance
    SIGTSTP_action.sa_handler = handle_SIGTSTP;
    sigfillset(&SIGTSTP_action.sa_mask);
    SIGTSTP_action.sa_flags = 0;
    sigaction(SIGTSTP, &SIGTSTP_action, NULL);
}