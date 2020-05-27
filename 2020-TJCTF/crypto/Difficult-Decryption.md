# Difficult-Decryption
Crypto, 100

>  Written by saisree
>  We intercepted some communication between two VERY important people, named Alice and Bob. Can you figure out what the encoded message is? intercepted.txt 

This is a simple Diffie-Hellman key exchange. The first thing we want to do is to factor the modulus, so we plug it into factordb.com. 
![](https://i.imgur.com/yIa52Wn.png)
Wow, these are very small factors! We figure sage can do the rest of the work for us.
![](https://i.imgur.com/P1jp0Fs.png)
We then compute `message ^ (pow(your_key, A, modulus))` and get the flag.

Flag: `tjctf{Ali3ns_1iv3_am0ng_us!}`