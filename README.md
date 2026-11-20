# apple1 – Apple I emulator for Linux

Linux port of the Raspberry Pi Pico Apple I emulator design. Plain C, no
libraries. The terminal replaces the Pico's USB-serial console, and a normal
directory replaces the SD card as the cassette "tape".

## Build (Debian/Ubuntu and relatives)

```
sudo apt install build-essential
make
./apple1

```

## Options

```
./apple1 [-t tapedir]

```

| Option | Meaning | 
| ----- | ----- | 
| `-t DIR` | Tape directory (default `./tape`, created if missing) | 

**ROMs and other images:**  WOZMON is built into the emulator at `$FF00-$FFFF`, but can also be a tape file in the tape directory that will overide the default one. Integer BASIC can be placed in the tape directory as `.dat` + `.map` files and either loaded manually via `C100R` or loaded automatically at startup using the
`AUTO` flag in the `.map` file.

## Keys

Lower case is converted to upper case. `Ctrl-R` reset, `Ctrl-]` quit,
`Esc` = Apple I ESC, `Ctrl-C` = BASIC break, Backspace/Delete = `_` rubout (`$5F`), Tab = space.
`Ctrl-R`/`Ctrl-]` also work when a program has hung and isn't reading the keyboard.

## Memory map

| Range | Use | 
| ----- | ----- | 
| `$0000-$BFFF` | RAM – WOZMON's line buffer is at `$0200` | 
| `$C000-$CFFF` | Cassette area: not RAM; `C100R` is trapped by the emulator | 
| `$D000-$DFFF` | RAM, except the keyboard/display PIA at `$D010-$D013` (mirrored at every address with bit 4 set) | 
| `$E000-$FEFF` | RAM; Integer BASIC can be loaded into `$E000-$EFFF` from tape and modified (`E000R` cold start, `E2B3R` warm start) | 
| `$FF00-$FFFF` | WOZMON ROM (can be overridden from tape via an `AUTO` `.map` or `*R`) | 

`is_ram()` in `apple1.c` defines the layout. `Ctrl-R` resets the CPU but leaves RAM (including a loaded or modified BASIC) as it is; restart the emulator to reload `AUTO` tapes.

## Cassette interface (filesystem tape)

Type `C100R` in WOZMON. You get a `*` prompt:

```
*100.200W 500.600W file.dat [AUTO [ADDR]]   write ranges (optionally mark AUTO)
*100.200R file.dat                          read file into the range
*R file.dat                                 read, ranges taken from file.map
*L                                          list tapes that have a .map file
*?                                          help
*                                           (blank line) back to WOZMON

```

* A name without an extension gets `.dat`.

* Each save writes `NAME.dat` (ranges concatenated) plus `NAME.map`.

* `.map` is plain text, one `START END` hex pair per line (`#` comments,
  `.`/`,`/`-` accepted as separators), plus an optional `AUTO [ADDR]` line:

  ```
  AUTO 0300
  0300 03FF
  
  ```

* `AUTO` loads the tape's ranges into memory automatically at startup (logging
  what was loaded and where it went). If an optional hex `ADDR` is given
  (e.g. `AUTO 0300`), execution jumps to `ADDR` after loading; without `ADDR`,
  it only loads the data and boots normally into WOZMON.

* `L` shows only tapes that have a `.map`, with their ranges and `[AUTO]` status.

* `NAME.MAP` (upper case, e.g. copied from DOS) is also accepted.

* File names may not contain `/` or start with `.`; they must not look like
  a range (e.g. `ab.cdw`).

Make a tape on a PC:

```
printf 'AUTO 0300\n0300 03FF\n' > tape/test.map
cp mycode.bin tape/test.dat       # 256 bytes for $0300-$03FF

```

To autoload Integer BASIC at startup without jumping straight into it:

```
printf 'AUTO\nE000 EFFF\n' > tape/basic.map
cp basic.bin tape/basic.dat       # 4096 bytes for $E000-$EFFF

```

## Differences from the Pico build

No LED flashes at reset/power-up (no on-board LED). The display never reports
busy, so output runs at host speed.