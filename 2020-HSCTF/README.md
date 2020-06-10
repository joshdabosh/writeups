# HSCTF 2020

b1c got 3rd. maxxed all but pwn bc half of it was heap lol

## Generic Flag Checker

> https://twitter.com/mcclure111/status/1002648636516282368

For some reason I solved a decently-worth rev chall this CTF instead of getting aplet to do it ("not on Windows").

Just running the exe gives us a `bad input`. So we reason that it must be passed in with the command line. It gives back, "checking..." and then depending on the length of the input, either a "Incorrect!" or it just exits.

Obviously there must be some memcmp happening, and using `strings memes.exe` we see a memcmp at the end.


Opening it in Ghidra makes the disassembly look scary so we opt for dynamic analysis.

Open it in x64db. Configure it to send cmd line input with `File > Change Command Line`. For now, let's just use `AAAABBBBCCCCDDDD` as our input.

In the beginning there are just some Windows DLL stuff so we can just skip to memes.EntryPoint with the call stack after it appears.

We can keep going until we see "checking..." inputted. After some annoying breakpointing we can see that the call to whatever outputs "checking..." is here:
![](https://i.imgur.com/2Ojba1l.png)

Skipping through it, we end up at a function call to what appears to be the flag checking function.


Eventually, we see our own input at:

![](https://i.imgur.com/x70KaaY.png)


A few more F8s... What's this?

![](https://i.imgur.com/H3Xs8gC.png)

It seems to have taken off 5 characters (`AAAAB`) from the front and 1 character (`D`) from the back, which perfectly fits the flag format! Now we know it must be checking the contents of our flag.


After holding down F8 through a loop, we can see our modified flag being built, and our original input ends up as:

![](https://i.imgur.com/5FNpf8X.png)

Now, you may have to squint a bit, but you'll see that the new character is simply the old character minus the index of it in the string. If you're not convinced, you can simply input a `flag{ABCDEF}`. The registers will end up as `AAAAAA`.

Great, so now we know what's happening to our input. What's it comparing to?

Holding down F8 again, we see a suspicious string,

![](https://i.imgur.com/403GWDE.png)

stored in the registers near 00007FF6CBC012DE. Moreover, we can even see a `memcmp` call soon after!

![](https://i.imgur.com/mCV8E6Q.png)

So, let's just reverse the subtraction of the index by adding the index back.

```py=
s = "con\\i`g^k"
for i in range(len(x)):
    print(chr(ord(x[i])+i), end="")
```

This gives us the flag.


Flag: `flag{cpp_memes}`
