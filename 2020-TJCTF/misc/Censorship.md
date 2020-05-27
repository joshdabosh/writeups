# Censorship
Misc, 30

>  Written by avz92
>  My friend has some top-secret government intel. He left a message, but the government censored him! They didn't want the information to be leaked, but can you find out what he was trying to say? nc p1.tjctf.org 8003
 
 Upon connecting the netcat service we are given a captcha or something. When we solve the captcha (just an addition of two numbers), we get `tjctf{[CENSORED]}`. Getting the captcha wrong will just kill the netcat session. Putting a non-int will throw an error and kill the session.

Using context clues and given the low point value, we can probably reason it's not a Python int() 0day. So we just write a script to add the two given numbers, giving us the flag.

```python
from pwn import *

c = remote("p1.tjctf.org", 8003)

data = c.recvuntil("?").strip("?").split()

n1 = int(data[-1])
n2 = int(data[-3])

c.sendline(str(n1+n2))

c.interactive()
```

Flag: `tjctf{TH3_1llum1n4ti_I5_R3aL}`