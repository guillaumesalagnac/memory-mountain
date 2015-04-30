one: one.c human.c
	gcc -Wall -o $@ $^

run: data.txt

data.txt: one dewit.py
	./dewit.py | tee data.txt

plot: data.txt
	./plot.py
