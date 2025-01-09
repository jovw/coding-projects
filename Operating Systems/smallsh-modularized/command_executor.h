#ifndef COMMAND_EXECUTOR_H
#define COMMAND_EXECUTOR_H
#include <sys/types.h>

void check_commands();
void handle_exit_call();
void handle_cd_call();
void non_built_in_commands();
void child_fork();
void parent_fork(pid_t childPid);

#endif
