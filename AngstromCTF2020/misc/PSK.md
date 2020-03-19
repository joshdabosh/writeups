# PSK
Misc, 90

> My friend sent my yet another mysterious recording...
> He told me he was inspired by PicoCTF 2019 and made his own transmissions. I've looked at it, and it seems to be really compact and efficient.
> Only 31 bps!!
> See if you can decode what he sent to me. It's in actf{} format
> Linked: transmission.wav

From the description, we can pretty much guess that the protocol used was PSK31.

There are many tools out there to decode, but my favorite is FLDIGI.

After setting it up, we play back the transmission using FLDIGI's `File > Audio > Playback`. We also set the decoding mode to BPSK-31 via `Op mode > PSK > BPSK-31`.

Now, just select the stream of data in the waterfall display and FLDIGI will do the rest.

![](https://i.imgur.com/QdcJZB3.png)
(the waterfall display is where the white space is, no idea why it isn't showing up).


Flag: `actf{hamhamhamhamham}`