CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC
all:
	$(CC) $(CFLAGS) schedule2.c -lm -o schedule2
clean:
	rm -f schedule2 schedule2.gcda
	rm -f schedule2.gcno cov.xml
html:
	gcovr -r . --html --html-details -o coverage.html