#include <stdio.h>
#include <stdint.h>
#include <string.h>

static char const alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                               "abcdefghijklmnopqrstuvwxyz"
                               "0123456789+/=";

int main(int argc, char *argv[]) {
    FILE* input_fd = stdin;
    // If there is a FILE argument and it isn't "-", then open that file
    if (argc > 1 && strcmp(argv[1], "-") != 0) {
        input_fd = fopen(argv[1], "r");
    }

    uint8_t in[3];
    uint8_t out_idx[4];
    int count = 0;
    while (1) {
        // read three bytes
        size_t bytes_read = fread(in, sizeof(uint8_t), 3, input_fd);
        // If end-of-file AND no bytes to process, print newline and exit
        if (bytes_read == 0 && count == 0) {
            printf("\n");
            break;
        }
        // process input using base64 algorithm
        // Upper 6 bits of byte 0
        out_idx[0] = in[0] >> 2;
        // Lower 2 bits of byte 0, shift left and or with the upper 4 bits of byte 1
        out_idx[1] = ((in[0] & 0x03u) << 4) | (in[1] >> 4);
        // Lower 4 bits of byte 1, shift left and or with upper 2 bits of byte 2
        out_idx[2] = ((in[1] & 0x0Fu) << 2) | (in[2] >> 6);
        // Last 6 bits of byte 2
        out_idx[3] = in[2] & 0x3Fu;
        // Write four output bytes
        for (int i = 0; i < 4; i++) {
            if (i < bytes_read) {
                printf("%c", alphabet[out_idx[i]]);
            } else {
                printf("=");
            }
        }
        // If end-of-file, print newline and exit
        if (bytes_read < 3) {
            printf("\n");
            break;
        }
        // If count == 76, print a newline
        count += 4;
        if (count == 76) {
            printf("\n");
            count = 0;
        }
    }
    if (input_fd != stdin) {
        fclose(input_fd);
    }
    return 0;
}