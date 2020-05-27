# Bad-Python
Rev, 50

>  Written by avz92
>  My friend wrote a cool program to encode text data! His code is sometimes hard to understand, and only he knows how it works. I ran the program twice, but forgot the input I used for the first time. I didn't save the key I used either, but I know it was 15 characters long. Can you figure out what text I encoded the first time? Output 1
Input 2
Output 2 

Bad Python had some really cursed code but after renaming some variables it turned out that it was just using some complicated algorithm to xor each byte in the input with some number determined solely by the index of the character. Which means, the solution is as simple as `input1 ^ input2 ^ output2`. Fun.

Flag: `tjctf{th15_iS_r3Al_pY7h0n_y4y}`