# RGBSA
Crypto, 70

>  Written by boomo
>  I love me some pixel art! Peep the red channels! Flag is in flag{} format

There were 3 gifs, `c.gif`, `e.gif`, `n.gif`, each containing an RSA coefficient. Each gif had 76 frames and each frame had the RSA coefficient embedded in red channel LSB. After extracting the data, we get a bunch of values of `c`, `e`, and `n`.

First thing we notice is that all the `n`s are the same. We then check all the values of `e` and find that $\left(e_{44},e_{45}\right)$ is the only pair of `e` values that have a GCD of 1. We can get `m` by finding a pair of integers $(a,b)$ such that $ae_{44}+be_{45}=1$, and then computing $c_{44}^a\cdot c_{45}^b\mod n$.

```python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
r,s = 44,45
x,y,z=egcd(e[r],e[s])
m = (pow(c[r],y,n)*pow(c[s],z,n))%n
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(m))
```

Flag: `flag{excitable_illumination_wanderer_}`.

Note: a previous vesion of this challenge was broken due to gif compression destroying 75% of the frames in c.gif, including the frame encoding for $c_{44}$. This only enabled people to get $m^{13}\mod n$, which was not sufficient to solve the challenge.