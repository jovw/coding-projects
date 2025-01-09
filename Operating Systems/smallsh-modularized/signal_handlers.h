#ifndef SIGNAL_HANDLERS_H
#define SIGNAL_HANDLERS_H

void handle_SIGINT(int signo);
void handle_SIGTSTP(int signo);
void init_signal_handlers();

#endif
