# RSAPWN
Misc

> nc challenges.tamuctf.com 8573

Seems like we just have to factor a number. Easy enough with pwntools :).

```python
from pwn import *

r = remote("challenges.tamuctf.com", 8573)


from functools import reduce

def factors(n):
	return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5)+1) if n%i==0)))


r.sendlineafter("ready.", "")


r.recv()
number = int(r.recvline())

f = factors(number)
f = list(f)
f.sort()

f = map(str, f)

print(f)

f = ' '.join([f[1], f[2]])

r.sendline(f)

print(r.recv())
print(r.recv())
```
