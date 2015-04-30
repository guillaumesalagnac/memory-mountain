default: help

help:
	@echo "see README.md"

DATAFILE=data-$(shell hostname -s).txt

benchmark: benchmark.c pretty.c
	gcc -O2 -Wall -o $@ $^

run: ${DATAFILE}

# we run the script with -u aka PYTHONUNBUFFERED, so that we get
# something to look at during the execution.

${DATAFILE}: benchmark harness.py
	python -u ./harness.py | tee ${DATAFILE}

plot: ${DATAFILE}
	./plot.py ${DATAFILE}

clean:
	-rm -f benchmark  ${DATAFILE}
