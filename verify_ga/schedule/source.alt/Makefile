CFLAGS = -lm -ftest-coverage -fprofile-arcs -fPIC
all:
	$(CC) $(CFLAGS) schedule.c -lm -o schedule
clean:
	rm -f schedule schedule.gcda
	rm -f schedule.gcno cov.xml
html:
	gcovr -r . --html --html-details -o coverage.html