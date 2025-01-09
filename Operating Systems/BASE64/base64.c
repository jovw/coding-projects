#define _POSIX_C_SOURCE 200809L
#include <assert.h>
#include <err.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

static char const b64a[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            "abcdefghijklmnopqrstuvwxyz"
                            "0123456789"
                            "+/";

int
main(int argc, char *argv[])
{
    char const *fn = "-";

    if (argc > 2) {
        errno = EINVAL;
        err(1, "Too many arguments");
    } else if (argc > 1 && strcmp(argv[1], "-")) {
        fn = argv[1];
        void *res = freopen(fn, "r", stdin);
        if (!res) err(1, "%s", fn);
    }

    int line_count = 0;
    for (;;) {
        unsigned char buf[3] = {0};

        size_t nr = fread(buf, 1, sizeof buf, stdin);
        if (nr < sizeof buf && ferror(stdin)) {
            err(EXIT_FAILURE, "%s", fn);
        }
        if (nr == 0) break;

        long long unsigned int bits = 0;
        bits |= buf[0]; /*buf[0] = abcdefgh -> 000...000abcdefgh*/
        bits <<= CHAR_BIT; /* 000...000abcdefgh00000000 */
        bits |= buf[1]; /* buf[1] = ijklmnop -> 000...000abcdefghijklmnop */
        bits <<= CHAR_BIT; /* 000...000abcdefghijklmnop00000000 */
        bits |= buf[2]; /* buf[2] = qrstuvwx -> 00000000abcdefghijklmnopqrstuvwx */

        unsigned char b64i [4];
        b64i[3] = bits & 0x3f;
        bits >>= 6;
        b64i[2] = bits & 0x3f;
        bits >>= 6;
        b64i[1] = bits & 0x3f;
        bits >>= 6;
        b64i[0] = bits;

        char b64o[4];
        b64o[0] = b64a[b64i[0]];
        b64o[1] = b64a[b64i[1]];
        b64o[2] = b64a[b64i[2]];
        b64o[3] = b64a[b64i[3]];

        // padding
        if (nr < 3) b64o[3] = '=';
        if (nr < 2) b64o[2] = '=';

        fwrite(b64o, 1, sizeof b64o, stdout);
        fflush(stdout);
        line_count += sizeof b64o;

        if (line_count >= 76) {
            assert(line_count == 76);
            line_count = 0;
            putchar('\n');
        }

        if (nr < 3) break;
    }
    if (line_count != 0) putchar('\n');

    return EXIT_SUCCESS;
}