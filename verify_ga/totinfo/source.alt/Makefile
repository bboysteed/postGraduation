CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC
all:
	$(CC) $(CFLAGS) tot_info.c -lm -o tot_info
clean:
	rm -f tot_info tot_info.gcda
	rm -f tot_info.gcno cov.xml
html:
	gcovr -r . --html --html-details -o coverage.html