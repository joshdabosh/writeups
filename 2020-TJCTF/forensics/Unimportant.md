# Unimportant
Forensics, 60

>  Written by KyleForkBomb
>  It's probably at least a bit important? Like maybe not the least significant, but still unimportant... unimportant.png source

The source makes this trivial. Essentially, the flag is encoded in the second-least significant bits of the green channel, along the columns of the image. We get a hex string starting with `e8d4c6e8ccf6dc60e8bee8d066bed8ca68e6e8bee6d272dc62ccd2c668dce8fa`. This is unprintable, but wait! The hint says that the author forgot to use `zfill`. We convert this to binary, prepend a zero, and convert to ASCII to get the flag.

Flag: `tjctf{n0t_th3_le4st_si9n1fic4nt}`