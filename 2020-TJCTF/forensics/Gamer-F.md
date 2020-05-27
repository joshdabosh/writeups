# Gamer-F
Forensics, 80

>  Written by boomo
>  Now, for my latest release: SnakeTris! (I'll let you in on a little hint, there are a few easter eggs in the game!)

The first easter egg could be obtained by decompiling `Assembly-CSharp.dll` with a .NET decompiler (I really like dnSpy), and finding a hex-encoded flag part as the win message.

The second easter egg could be obtained by extracting the assets and listening through the second victory sound, which had another flag part.

The third easter egg was stored as a string in one of the files.