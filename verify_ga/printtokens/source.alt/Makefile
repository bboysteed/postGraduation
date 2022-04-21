CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC
all:
	$(CC) $(CFLAGS) print_tokens.c -lm -o print_tokens
clean:
	rm -f print_tokens print_tokens.gcda
	rm -f print_tokens.gcno cov.xml
html:
	gcovr -r . --html --html-details -o coverage.html