# Ling-Ling
Forensics, 10

>  Written by KyleForkBomb
>  Who made this meme? I made this meme! unless..... 

We are given an image. The description says, `Who made this meme?`, so we instinctively try to search for exif data with `exiftool`. The flag is the exif extracted Artist:

```
SCLs-Air:Downloads toaster$ exiftool d25fe79e6276ed73a0f7009294e28c035437d7c7ffe2f46285e9eb5ac94b6bec_meme.png
ExifTool Version Number         : 10.94
File Name                       : d25fe79e6276ed73a0f7009294e28c035437d7c7ffe2f46285e9eb5ac94b6bec_meme.png
...
Resolution Unit                 : inches
Artist                          : tjctf{ch0p1n_fl4gs}
Y Cb Cr Positioning             : Centered
...
```

Flag: `tjctf{ch0p1n_fl4gs}`