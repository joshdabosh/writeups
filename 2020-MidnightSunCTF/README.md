# Midnight Sun CTF

I played as part of `tuxicide` and we placed 5th.

Here's one of the two challs I worked on during the CTF:

## Sh*thappens
![](https://i.imgur.com/mbPMl6w.png)

We are given a haproxy config file, with these rules:

```
http-request deny if METH_POST
http-request deny if { path_beg /admin }
http-request deny if { cook(IMPERSONATE) -m found }
http-request deny if { hdr_len(Cookie) gt 69 }
```

Seems like we just have to bypass them.

### POST bypass

We don't actually bypass this because it's impossible. We just avoid POST requests.

### /admin bypass

`path_beg` checks for `/admin`, so we can bypass by visiting `//admin`.

After doing some recon visiting `//admin`, the server tells us that we need the both the `IMPERSONATE` and `KEY` cookies.

### IMPERSONATE cookie bypass

This check makes sure that we don't have the `IMPERSONATE` cookie set. Weastie decided to bruteforce characters and apparently `=IMPERSONATE` cookies work.

### Getting correct cookies

We can send a `HEAD` request to `//admin`, and get the necessary Set-Cookie headers back, which include the `KEY` cookie, and `=IMPERSONATE` cookie.

### Cookie length bypass

Unfortunately, the key length is 64 characters, and another 4 from `KEY=` puts our Cookie length already at 68 - not enough for our `IMPERSONATE` cookie.

However, haproxy treats comma delimited values as separate values, so we can set our Cookie header to

`KEY=<key from HEAD request>;,;=IMPERSONATE=admin`

and retrieve the flag from `//admin`.

Flag: `midnight{hap_hap_h00r@y!!}`
