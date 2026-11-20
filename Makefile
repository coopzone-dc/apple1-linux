CC      ?= gcc
CFLAGS  ?= -O2 -Wall -Wextra

apple1: apple1.c
	$(CC) $(CFLAGS) -o $@ apple1.c

clean:
	rm -f apple1

.PHONY: clean
