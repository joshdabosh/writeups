# ASMR
Rev, 60

>  Written by KyleForkBomb
>  I heard ASMR is a big hit on the internet!

I assembled and compiled the program with:
```
nasm -felf64 -g -Fdwarf asmr.asm -o asmr.o
ld -o asmr asmr.o -m elf_x86_64
```
Then, I ran `./asmr`, and with the power of GDB and `netstat -peanut | grep asmr` I found out that the program is listening on port 1337. We see that it takes input from the socket and xors everything with `0x69` (nice) then compares to `0x360c1f0605360c1e` and `0xc0c10361b041a08` so we decode from hex, xor with `0x69`, reverse for endianness, and get the password of `we_love_asmr_yee`. After entering the password in, the binary originally spat out a giant OGG file which we can play, and Kyle's beautiful voice whispered the flag into our ears. His voice really sent me into another realm. Sadly, the flag got leaked and he didn't want to recreate the audio so instead we just got a message back:
```
I really appreciate everyone still playing TJCTF. It really means a lot to me. I know this year hasn't been the greatest, and that a lot of what we've done as a team has made people upset. I really wish it didn't have to be this way, but what's done is done. 

Here's your flag: tjctf{s0m3_n1c3_s0und5_for_you!!!}

<3 -DM
```
:heartpulse:

Flag: `tjctf{s0m3_n1c3_s0und5_for_you!!!}`