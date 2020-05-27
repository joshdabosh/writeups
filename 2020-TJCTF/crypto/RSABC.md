# RSABC
Crypto, 50

>  Written by boomo
>  I was just listening to some relaxing ASMR when a notification popped up with this. ???

We are given n, e, and c.

Standard Intro-to-RSA. N is easily factorizable with [factordb](http://factordb.com/index.php?query=57772961349879658023983283615621490728299498090674385733830087914838280699121).

```
phi = 57772961349879658023983283615621490727811513942828735462407211309915750394432
d = 44272299081643288299441360906720516766592151810988369202023512922571811592065
m = 10141227296934397750285339393723710527726461
```

Converting m to hex then to ASCII gives the flag.

Flag: `tjctf{BOLm1QMWi3c}`
