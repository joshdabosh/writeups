# ws1
Misc, 30

> Find my password from this recording (:
> Linked: recording.pcapng

For some strange reason this challenge had more solves than the sanity check...

Anyway, this was the generic "wireshark data capture" challenge.

We open up the capture in Wireshark, and scroll a bit.

Eventually, we find an interesting POST request:
![](https://i.imgur.com/3AyCs9c.png)

The flag is visible in the form data, but we have to un-urlencode it.

Flag: `actf{wireshark_isn't_so_bad_huh-a9d8g99ikdf}`