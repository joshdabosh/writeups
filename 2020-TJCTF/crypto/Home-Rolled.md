# Home-Rolled
Crypto, 80

>  Written by nthistle
>  It's that time of year again... time to home roll your own crypto! Since pesky CTF players keep breaking my schemes, this time I obfuscated the source code, so you'll never be able to figure out what it's doing. I also used cutting-edge Python 3.8 syntax! Security by obscurity! nc p1.tjctf.org 8012 

Source code:
```python
import os,itertools
def c(l):
 while l():
  yield l
r,e,h,p,v,u=open,any,bool,filter,min,len
b=lambda x:(lambda:x)
w=lambda q:(lambda*x:q(2))
m=lambda*l:[p(e(h,l),key=w(os.urandom)).pop(0)for j in c(lambda:v(l))]
f=lambda l:[b(lambda:m(f(l[:k//2]),f(l[k//2:]))),b(b(l))][(k:=u(l))==1]()()
s=r(__file__).read()
t=lambda p:",".join(p)
o=list(itertools.permutations("rehpvu"))
exec(t(o[sum(map(ord,s))%720])+"="+t(b(o[0])()))
a=r("flag.txt").read()
print("".join(hex((g^x)+(1<<8))[7>>1:]for g,x in zip(f(list(range(256))),map(ord,a))))
```
Notice the line `s=r(__file__).read()`. This probably means that the program is reading it's own source code. Yuck! We copy/paste the source into a multi-line string and set `s` equal to that. Now we can safely modify the code.

We can also see that there's a sneaky little `exec` in the code as well. We change the `exec` to a `print` and get `r,v,h,e,p,u=r,e,h,p,v,u`. Tricksy hobbitses.

Let's take a look at the last line. The code runs through each character in the flag and performs an XOR with a corresponding number in whatever `f(list(range(256)))` is. Great, it's a stream cipher. The resulting output is then converted to hex.

I spent way too much time digging into the functions - essentially, the function `f` is performing a randomized merge sort, where in each merge, elements are pulled from both sublists at random. However, this information isn't actually necessary. If we look at a bunch of outputs of `f(list(range(256)))`, they are all permutations of the numbers from 1 to 256. 

This seems unbreakable at first - after all, the permutations are genereated with `os.urandom`. However, there is a fatal flaw in the key generation - no number is ever repeated in the key.

We connect to the server and get a relatively short output, so we have good reason to believe that this is the encrypted flag. This means the plaintext must start with `tjctf{` and end with `}`. And here's where the flaw comes in: If the first character of the decoded output is `ord('t')^x`, no other character could have been XORed with `x`. Through multiple connections to the server, we can lower the possibilities to just one character each.

```python
from pwn import *

possible = [set(range(256)) for i in range(38)]
known = b"tjctf{???????????????????????????????}"
for x in range(1000):
	while 1:
		try:
			r = remote("p1.tjctf.org", 8012)
			break
		except:
			pass
	a = bytes.fromhex(r.readline().strip().decode())
	for i in [0,1,2,3,4,5,37]:
		c = a[i]
		for j in range(6,37):
			possible[j].discard(c^known[i]^a[j])
	r.close()
	if x%100==0: print(x)
for i in possible:
	if len(i)==1:
		print(chr(i[0]),end="")
print()
```

The flag is `tjctf{n3v3r_r0LL_ur_0wn_cryptOMEGALUL}`