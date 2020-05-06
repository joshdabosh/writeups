# Zh3r0 PreCTF 2020

Another smaller CTF.

As usual there were quite some guess challenges. The web category was pretty lacking, but the pwn seemed okay-ish (I don't like pwn, and I'm not good at it either).

However there was one RSA challenge that was quite "refreshing" to do, as I hadn't really touched more advanced RSA systems after PACTF 2019.

## Ultra Strong RSA
>A simple RSA maybe be easy to crack, what if we use multilayered encryption, where we encrypt the flag in multiple methods. To crack an advanced RSA Script, study the script well before even trying to crack it.
>
>Not always tools help.
>
>HAPPY HACKING :)
>
>Attached: [chall.py](ultrarsa/chall.py), [out.txt](ultrarsa/out.txt)

Starting from out.txt, we are given quite a few numbers:

- n
- n1
- n2
- n3
- ct_hint
- ct_flag
- key(b64 encoded)

It is important to observe that one can recover any primes `p` and `q` from a given difference `p-q` and their product `pq`:

![(p-q)^2 = p^2 + q^2 - 2pq](https://render.githubusercontent.com/render/math?math=(p-q)%5E2%20%3D%20p%5E2%20%2B%20q%5E2%20-%202pq), ![(p+q)^2 = p^2 + q^2 + 2pq](https://render.githubusercontent.com/render/math?math=(p%2Bq)%5E2%20%3D%20p%5E2%20%2B%20q%5E2%20%2B%202pq)
\
![p^2 + q^2 = (p-q)^2 + 2pq](https://render.githubusercontent.com/render/math?math=p%5E2%20%2B%20q%5E2%20%3D%20(p-q)%5E2%20%2B%202pq)

![(p+q)^2 = (p-q)^2 + 4pq](https://render.githubusercontent.com/render/math?math=(p%2Bq)%5E2%20%3D%20(p-q)%5E2%20%2B%204pq)
\
![p+q = \sqrt{(p-q)^2+4pq}](https://render.githubusercontent.com/render/math?math=p%2Bq%20%3D%20%5Csqrt%7B(p-q)%5E2%2B4pq%7D)


Because `n` is simply `pq` in the RSA keygen process, we can simplify this to

![p+q = \sqrt{(p-q)^2+4pq}](https://render.githubusercontent.com/render/math?math=p%2Bq%20%3D%20%5Csqrt%7B(p-q)%5E2%2B4n%7D)

Let `p-q` (given) be `d` (not to be confused with the RSA decryption modulus `d`).

Summing `p-q` and `p+q` will give us

![2p = d + \sqrt{(p-q)^2+4pq}](https://render.githubusercontent.com/render/math?math=2p%20%3D%20d%20%2B%20%5Csqrt%7B(p-q)%5E2%2B4pq%7D)
\
![p = \frac{d + \sqrt{(p-q)^2+4pq}}{2}](https://render.githubusercontent.com/render/math?math=p%20%3D%20%5Cfrac%7Bd%20%2B%20%5Csqrt%7B(p-q)%5E2%2B4pq%7D%7D%7B2%7D)

Knowing `p`, it is trivial to recover `q`:

![q=p-d](https://render.githubusercontent.com/render/math?math=q%3Dp-d)


With that trick aside, let us examine the source.

The source generates 6 2048-bit primes, `p q r s x y`, and multiplies them.

- n = x ⋅ y
- n1 = p ⋅ q
- n2 = r ⋅ s
- n3 = n1 ⋅ n2

Futher, the script also calculates the differences of some of the primes:

- key = |x-y|
- a = |p-q|
- b = r+q
- c = r+p

Note that `a b c` are written to another file instead of `out.txt`.

We will decrypt the hint first (ct `N`), because that is the only one possible so far.

Applying our trick mentioned above of recovering the primes, we can easily decrypt `N` after calculating the totient and private exponent.

The hint gives us a link to `https://pastebin.com/Ss2RBhVN`, which contains `a b c`.

We now have the final pieces of information to decrypt the flag.

We can recover `p` and `q` from the given `a` (the difference) using the trick above again.

To recover `r`, note the following.

![b+c = 2r + p+q](https://render.githubusercontent.com/render/math?math=b%2Bc%20%3D%202r%20%2B%20p%2Bq)

We already have `p+q` from our trick, so we can recover r through

![\frac{b+c - (p+q)}{2} = r ](https://render.githubusercontent.com/render/math?math=%5Cfrac%7Bb%2Bc%20-%20(p%2Bq)%7D%7B2%7D%20%3D%20r%20)

Now we have recovered `p q r s`.

As long as the four primes are distinct, it is guaranteed that n1 (p ⋅ q) and n2 (r ⋅ s) will be coprime.

We can thus apply the rule that `ϕ(ab)=ϕ(a)⋅ϕ(b)` to n3 (n1 ⋅ n2).

We can calculate `ϕ(n1)` and `ϕ(n2)` easily as we know the primes `p q r s`. Substituting back into the calculation of `ϕ(n3)`, we get:

![\phi(n3) = (p-1)(q-1)\cdot(r-1)(s-1)](https://render.githubusercontent.com/render/math?math=%5Cphi(n3)%20%3D%20(p-1)(q-1)%5Ccdot(r-1)(s-1))

Now we know the totient, we can calculate the private exponent `d` and decrypt the flag.

Full solution script [here](ultrarsa/solve.py).

Flag: `zh3r0{Y0u_h4v3_b34ten_RSA}`

It does seem a bit contrived, but I found the math of it pretty fun compared to "guess-the-cipher" and "weird-encoding".
