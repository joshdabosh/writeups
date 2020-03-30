# VAULT
Rev

> Linked: vault

Straight rev.

Opening in Ghidra, we see some suspicious hex strings.
![](https://i.imgur.com/1uQWQHW.png)

Converting to ASCII doesn't work. We see a `strcmp` call, so let's open it up in gdb and just step through until the flag is in memory (gdb gef helps a lot with this).

Flag: `gigem{p455w0rd_1n_m3m0ry1}`
