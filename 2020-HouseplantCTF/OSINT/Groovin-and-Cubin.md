# Groovin-and-Cubin
Osint

> I really like my work, I get to make cool cryptography CTF challenges but with Rubik's cubes! Sadly, they aren't good enough to get released, but hey, I took a nice image of my work! You should go try to find some more about my work :)
> 
> Attached: vibin.zip

Extracting the zip gives us an image. Something inside our soul tells us to check EXIF data, so we do:

```
exiftool vibin.jpg 
ExifTool Version Number         : 10.94
File Name                       : vibin.jpg
Directory                       : .
File Size                       : 2.4 MB
...
Comment                         : A long day of doing cube crypto at work... but working at Groobi Doobie Shoobie Corp is super fun!
...
```

The comment leads us to look for a store named `Groobi Doobie Shoobie Corp`.

We find [their Twitter](https://twitter.com/GShoobie) eventually.

Scrolling to their first tweet reveals that they have an [Instagram account](https://www.instagram.com/groovyshoobie/) too. The flag is in the bio.

Flag: `rtcp{eXiF_c0Mm3nT5_4r3nT_n3cEss4rY}`
