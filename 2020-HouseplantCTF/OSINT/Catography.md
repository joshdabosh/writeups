# Catography
Osint

> Jubie's released her own collection of cat pictures. Go check it out!
> 
> http://challs.houseplant.riceteacatpanda.wtf:30002
> 
> Note: The Unsplash author credit is not a part of the challenge, it's only there to conform with the Unsplash image license.

Originally I tried to exploit the `/api?page=<n>` route, but that turned out to be useless.

We get the spidey sense that we should check EXIF data again (for some reason) and so we find that we have GPS coordinates in each image. Moreover, the coordinates were mostly distinct.


I recognized this as similar to the last stage of a [HackTM 2020 challenge](https://github.com/joshdabosh/writeups/tree/master/HackTM2020) that I solved, so I tried applying the same idea: plotting the points on some surface.

I told my teammate how to do it and he solved :p

Apparently the flag overlapped with itself so he had to do it letter by letter. :confetti_ball: 
