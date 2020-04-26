# I-don't-like-needles
Web

> They make me SQueaL!
> 
> http://challs.houseplant.riceteacatpanda.wtf:30001

We get source by visiting `/?sauce`.

This is vulnerable to classic SQLi, but we have to actually read the source to find the right username: `flagman69`.

We log in with username `flagman69` and password `'=0;-- ` to get the flag.

Flag: `rtcp{y0u-kn0w-1-didn't-mean-it-like-th@t}`
