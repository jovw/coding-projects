#ifndef COMMAND_PARSER_H
#define COMMAND_PARSER_H

#include <stdlib.h>

size_t wordsplit(char const *line);
char *expand(char const *word);
char param_scan(char const *word, char const **start, char const **end);
char * build_str(char const *start, char const *end);

#endif
