# ws2
Misc, 80

> No ascii, not problem :)
> Linked: recording.pcapng

I never realized I had a typo in this until now :sweat_smile:.

We open the capture again in Wireshark, and we find another interesting POST request:
![](https://i.imgur.com/dYU1ZiP.png)

It seems like I uploaded a JPEG image.

We can export the data via Wireshark's `File > Export Objects > HTTP`.
There, we can choose the data that we want, which is the `multipart/form-encoded`.

We can then save it as `data`, and use `binwalk -D=".*" bin` to extract any images.
![](https://i.imgur.com/OrRDmb3.png)

We `cd _data.extracted`, and find a file (`88` in my case).
If we use the `file` command, we realize it is the image!
![](https://i.imgur.com/SNSeJ3w.png)

We open up `88`, and the flag is there in the image.

Flag: `actf{ok_to_b0r0s-4809813}`