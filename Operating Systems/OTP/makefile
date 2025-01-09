TARGETS=enc_server enc_client dec_server dec_client keygen

.PHONY: all clean
all: $(TARGETS)

clean:
	@rm $(TARGETS) 2>/dev/null

define compile
gcc $(CPPFLAGS) $(CFLAGS) -o $@ $<
endef

dec_% : CPPFLAGS += -DDEC
dec_%: %.c ; $(compile)
enc_%: %.c ; $(compile)
%: %.c ; $(compile)


# CC=gcc
# CFLAGS=-Wall -std=c99

# # Define all executables you want to build
# TARGETS=enc_server enc_client dec_client dec_server keygen

# all: $(TARGETS)

# enc_server: enc_server.c
# 	$(CC) $(CFLAGS) -o enc_server enc_server.c

# enc_client: enc_client.c
# 	$(CC) $(CFLAGS) -o enc_client enc_client.c

# dec_server: dec_server.c
# 	$(CC) $(CFLAGS) -o dec_server dec_server.c

# dec_client: dec_client.c
# 	$(CC) $(CFLAGS) -o dec_client dec_client.c

# keygen: keygen.c
# 	$(CC) $(CFLAGS) -o keygen keygen.c

# clean:
# 	rm -f $(TARGETS)