# shifter
Misc, 160

> What a strange challenge...
> It'll be no problem for you, of course!
> nc misc.2020.chall.actf.co 20300

Gotta admit, this description definetely will not win any creativity awards.

Upon our first connection, we are presented with the rules.
1. We need to solve 50 problems
2. In each problem, we have to caesar shift a plaintext by the nth fibonacci number
3. n < 50, p is completely uppercase and alphabetic, len(p) < 50
4. We have 60 seconds to do it

Obviously, doing it by hand will not cut it. Thus, we gotta do it with a script.

In order to find the nth Fibonacci, we can use [Binet's formula](https://artofproblemsolving.com/wiki/index.php/Binet%27s_Formula).

After that, we can modulo our shift by 26 in order to quickly shift our plaintext.


```python
from pwn import *

from math import sqrt


conn = remote("misc.2020.chall.actf.co", 20300)


# binet's formula implementation
def find(n):
    n = ((1+sqrt(5))/2)**n - ((1-sqrt(5))/2)**n
    return int(n/sqrt(5))


# shifting function
def solve(p,n):
    shift = find(n) % 26

    r = ""

    for a in p:
        r += chr((ord(a) - 65 + shift) % 26 + 65)

    return r


# solve each individual problem
def chall():
    conn.recvuntil("Shift ")
    s = conn.recvuntil(": ")


    s = s.split()
    pt = s[0]
    amt = int(s[2][2:])


    ct = solve(pt, amt)

    conn.sendline(ct)

# loop to solve 50
for _ in range(50):
    chall()


# print the result, which is the flag
print(conn.recv())
```