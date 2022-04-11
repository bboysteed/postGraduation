CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC
all:
	$(CC) $(CFLAGS) tcas.c -o tcas
clean:
	rm -f tcas tcas.gcda
	rm -f tcas.gcno cov.xml
html:
	gcovr -r . --html --html-details -o coverage.html