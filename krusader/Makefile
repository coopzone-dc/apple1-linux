# Needs cc65:  sudo apt install cc65
TAPEDIR ?= ../tape

krusader.bin: krusader.s krusader.cfg
	ca65 krusader.s -o krusader.o -l krusader.lst
	ld65 -C krusader.cfg krusader.o -o krusader.bin -m krusader.map
	@echo "size: $$(stat -c%s krusader.bin) bytes (limit 3840)"

# Create the .dat/.map tape pair for the emulator: C100R, then  R krusader.dat
tape: krusader.bin
	mkdir -p $(TAPEDIR)
	cp krusader.bin $(TAPEDIR)/krusader.dat
	printf '7100 %04X\n' $$((0x7100 + $$(stat -c%s krusader.bin) - 1)) > $(TAPEDIR)/krusader.map
	@cat $(TAPEDIR)/krusader.map

clean:
	rm -f krusader.o krusader.lst krusader.bin krusader.map

.PHONY: tape clean
