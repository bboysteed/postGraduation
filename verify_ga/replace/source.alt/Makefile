CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC
all:
	$(CC) $(CFLAGS) replace.c -lm -o replace
clean:
	rm -f replace replace.gcda
	rm -f replace.gcno cov.xml
html:
	gcovr -r . --html --html-details -o coverage.html