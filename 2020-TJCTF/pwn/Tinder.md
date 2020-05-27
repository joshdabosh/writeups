# Tinder
Pwn, 25

>  Written by agcdragon
>  Start swiping! nc p1.tjctf.org 8002 

Upon decompiling the binary, we can see that there is an `input` function which takes in a buffer and a number `n` and reads `n * 16` bytes into the buffer. However, in the main function, on the fourth input, it calls `input(buf, 8)` on a 64 byte buffer. We have a buffer overflow :scream_cat:! Our goal is to overwrite a variable with `0xc0d3d00d`, so we convert it to little endian and then turn off our brains and just start brute-forcing offsets. The final payload was:
```
python -c 'print "A\nB\nC\n" + "X"*116 + "\x0d\xd0\xd3\xc0" | nc p1.tjctf.org 8002'
```

Flag: `tjctf{0v3rfl0w_0f_m4tch35}`