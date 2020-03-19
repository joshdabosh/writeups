# one-time-bad
Crypto, 100

> My super secure service is available now!

> Heck, even with the source, I bet you won't figure it out.

> nc misc.2020.chall.actf.co 20301

> Linked: server.py


The key observation to make here is that the pRNG seeding is based on the time you make the connection:
`random.seed(int(time.time()))`. Also, I truncated the time to an int to make life that much easier.

Thus, we can somewhat accurately seed our own random, and then generate the plaintext, key, and ciphertext.

One other important observation is to realize that the server is running in Python 3, shown by the usage of parenthesises around the `print` statement. This is because Python 2's `random` implementation is different than that of Python 3.

Yet another observation is that the seed may be slightly off. To account for this, we simply have to check the ciphertext against the one provided by the server. If it's different, we can try the seed + 1, and so forth until it matches.

After that, it's just implementation :)
```python
from pwn import *
import random
import time
import base64


def otp(a, b):
	r = ""
	for i, j in zip(a, b):
		r += chr(ord(i) ^ ord(j))
	return r


def genSample():
	p = ''.join([string.ascii_letters[random.randint(0, len(string.ascii_letters)-1)] for _ in range(random.randint(1, 30))])
	k = ''.join([string.ascii_letters[random.randint(0, len(string.ascii_letters)-1)] for _ in range(len(p))])

	x = otp(p, k)

	return x, p, k



conn = remote("misc.2020.chall.actf.co", 20301)

seed = int(time.time())
random.seed(seed)

sample_x, sample_p, sample_k = genSample()


conn.sendlineafter("> ", "2")

need = conn.recvline().strip()
data = conn.recvuntil(": ")


d = base64.b64decode(need).decode()

offset = -20
while sample_x != d:
        random.seed(seed+offset)
        sample_x, sample_p, sample_k = genSample()
        
        offset += 1

conn.sendline(sample_p)
print(conn.recv().decode())
```