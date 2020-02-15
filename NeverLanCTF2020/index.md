# NeverLAN CTF 2020
Start: Sat, Feb 8 2020, 10:00 AM EST

End: Tue, Feb 11 2020, 7:00 PM EST

# Placing
- Schools: 1st (max score)
- General: 32nd

# Review
This weekend I played in NeverlanCTF as the solo team `bosh`. The challenges were alright, although many of them were just guessing.

I didn't like how they did not announce challenge drops before they actually released them, and how the platform went down after the last wave of challenge releases.

# Writeups
## Table of contents
| Challenge Name | Category | Points |
|:-:|:-:|:-:|
| [Adobe Payroll](#adobe-payroll) | Reverse Engineering | 100 |
| [Script Kiddie](#script-kiddie) | Reverse Engineering | 100 |
| [Reverse Engineer](#reverse-engineer) | Reverse Engineering | 200 |
| [Pigsfly](#pigsfly) | Cryptography | 30 |
| [BaseNot64](#basenot64) | Cryptography | 50 |
| [Don't Take All Knight](#don't-take-all-knight) | Cryptography | 75 |
| [The Invisibles](#the-invisibles) | Cryptography | 75 |
| [Stupid Cupid](#stupid-cupid) | Cryptography | 100 |
| [My Own Encoding](#my-own-encoding) | Cryptography | 200 |
| [BabyRSA](#babyrsa) | Cryptography | 250 |
| [CryptoHole](#cryptohole) | Cryptography | 250 |
| [It is like an onion of secrets](#it-is-like-an-onion-of-secrets) | Cryptography | 300 |
| [Unsecured Login](#unsecured-login) | PCAP | 50 |
| [Unsecured Login2](#unsecured-login2) | PCAP | 75 |
| [FTP](#ftp) | PCAP | 100 |
| [Teletype Network](#teletype-network) | PCAP | 125 |
| [hidden-ctf-on-my-network](#hidden-ctf-on-my-network) | PCAP | 250 |
| [Listen to this](#listen-to-this) | Forensics | 125 |
| [Open Backpack](#open-backpack) | Forensics | 150 |
| [Look into the past](#look-into-the-past) | Forensics | 250 |
| [DasPrime](#dasprime) | Programming | 100 |
| [password_crack](#password_crack) | Programming | 100 |
| [Robot Talk](#robot-talk) | Programming | 200 |
| [BitsnBytes](#bitsnbytes) | Programming | 200 |
| [Evil](#evil) | Programming | 200 |
| [Front page of the Internet](#front-page-of-the-internet) | Recon | 50 |
| [The Big Stage](#the-big-stage) | Recon | 75 |
| [The Link](#the-link) | Recon | 75 |
| [Thats just Phreaky](#thats-just-phreaky) | Recon | 200 |
| [Cookie Monster](#cookie-monster) | Web | 10 |
| [Stop the Bot](#stop-the-bot) | Web | 50 |
| [SQL Breaker](#sql-breaker) | Web | 50 |
| [SQL Breaker 2](#sql-breaker-2) | Web | 75 |
| [Follow Me!](#follow-me) | Web | 100 |
| [Browser Bias](#browser-bias) | Web | 150 |
| [Chicken Little 1](#chicken-little-1) | Chicken Little | 35 |
| [Chicken Little 2](#chicken-little-2) | Chicken Little | 36 |
| [Chicken Little 3](#chicken-little-3) | Chicken Little | 37 |
| [Chicken Little 4](#chicken-little-4) | Chicken Little | 38 |
| [Chicken Little 5](#chicken-little-5) | Chicken Little | 39 |
| [Chicken Little 6](#chicken-little-6) | Chicken Little | 40 |
| [Chicken Little 7](#chicken-little-7) | Chicken Little | 100 |
| [Milk Please](#milk-please) | Trivia | 10 |
| [Professional Guessing](#professional-guessing) | Trivia | 10 |
| [Base 2^6](#base-2^6) | Trivia | 10 |
| [AAAAAAAAAAAAAA! I hate CVEs](#aaaaaaaaaaaaaa!-i-hate-cves) | Trivia | 20 |
| [Rick Rolled by the NSA???](#rick-rolled-by-the-nsa???) | Trivia | 50 |

## Reverse Engineering
### Adobe Payroll
Once we unzip with 7z we end up with two files:
`description.MD`
`Adobe_Employee_Payroll.exe`

`description.MD` hints towards a software called [DotPeek](https://www.jetbrains.com/decompiler/).

DotPeek decompiles (read: translates to semi human readable code) .NET files, such as our .exe file. After we open `Adobe_Employee_Payroll.exe` up, we can explore the files:

![](https://i.imgur.com/FDU78kE.png)

Double clicking on something seems like a good idea. Now we can see the decompiled code for something that looks important:
![](https://i.imgur.com/X4hnWnz.png)
As you can see, `r1`, `r2`, `r3` and so (till `r38`) on seem to be holding integers. They seem like they're ASCII values... and they are!

Without even looking at the rest of the program, we can find the flag by converting all the values from `r1` through `r38` to letters.

### Script Kiddie
### Reverse Engineer

## Cryptography
### Pigsfly
Basic substitution cipher, using the pigpen cipher alphabet.

Decrypting gives the flag.

### BaseNot64
As from the title, the data is not in base 64. We play around with the different encodings in [cyberchef](https://gchq.github.io/CyberChef/).

Noticing that there are only capital letters / symbols in the plaintext, we can probably guess that the base will be relatively small. We try to decode it as a base 32 string, and it works.

Decoding gives the flag.

### Don't Take All Knight
Another basic substitution cipher, using the Knights Templar Code cipher. Decode.f<span>r</span> has a [nice solver](https://www.dcode.fr/templars-cipher).

Decrypting gives the flag.

### The Invisibles
Yet another basic substitution cipher, using the Arthurs and the Invisibles alphabet. Decode.f<span>r</span> has a [nice solver](https://www.dcode.fr/arthur-invisibles-cipher).

Decrypting gives the flag.

### Stupid Cupid
Googling `Cupid cipher` gives us some results about how James Madison hid his plaintexts in some text using numbers.

When we count the amount of numbers in the ciphertext at the top of the file, we find that it is equal to the amount of rows there are, and the highest number in the ciphertext does not exceed the number of columns :eyes:

We then guess that each row corresponds to a character of the plaintext, and each number in the ciphertext is the corresponding column to pick from.

For example:
The first number in the ciphertext is `6`. The character at the first row, 6th column is `V`.
Then, the second number in the ciphertext is `12`. The character at the second row, 12th column is `E`.

Continue to get the flag.

### My Own Encoding
We are presented with 16 5x5 grids, each with a single box blacked out.
Shot in the dark.
We reason that since it is 5x5, there are 25 choices which is close enough to 26 (letters of the alphabet).

We assume the top left represents the letter A, and the next one to the right represents B, and so on.

Doing so, we get `MHBDI...`, until we reach the 12th box. There is no marking here! Another shot in the dark. We assume that no marking represents the letter `A`.

Thus, our previously transcribed "plaintext" has to be Caesar shifted by 1 to get the flag, easy enough.

### BabyRSA
Questionable RSA. I didn't know what to do with the numbers since they were spaced out. I finally guessed they were individual characters of the flag and successfully decrypted them as such.

Using [factordb](http://factordb.com/), we can factor `n` into `17 * 149`, obviously the p and q for this challenge.

Now, using modified code from [a StackExchange article](https://crypto.stackexchange.com/questions/19444/rsa-given-q-p-and-e), we can decrypt the flag character by character.

```python
# Function from Geeks for Geeks
def modInverse(a, m): 
    m0 = m, y = 0, x = 1
    if (m == 1): 
        return 0
    while (a > 1) : 
        q = a // m 
        t = m 
        m = a % m 
        a = t 
        t = y 
        y = x - q * y 
        x = t
        
    if (x < 0):
        x += m0
        
    return x 


def decrypt(ct):
    p = 17
    q = 149
    e = 569

    # compute n
    n = p * q

    # Compute phi(n)
    phi = (p - 1) * (q - 1)

    # Compute mult mod inv of e
    d = modInverse(e, phi)

    # Decrypt ciphertext
    pt = pow(ct, d, n)
    print(chr(pt), end="")


chall = "2193 1745 2164 970 1466 2495 1438 1412 1745 1745 2302 1163 2181 1613 1438 884 2495 2302 2164 2181 884 2302 1703 1924 2302 1801 1412 2495 53 1337 2217".split()

# this is probably bad practice but it works
list(map(lambda x: decrypt(int(x)), chall))
```

### CryptoHole
Basically just a bunch of ciphers. Each level has a chal.txt which contains an encrypted password, and a password-protected zip file for the next layer.

Here is the order:

Layer 1 -`A ffine Cipher here 3`:
- Affine Cipher
- Brute force
- Password is `AfvqPZW0bDMB&HTfzo`

Layer 2 - `Two is better than one`
- Double Transposition Cipher
- Both keys are `NEVERLANCTF`
- Ciphertext decrypts to `PASSWORDV78DTNRI6KBD3SDFQXXXXXXXX`
- Password is `V78DTNRI6KBD3SDFQ`

Layer 3 - `I'm on the fence with this one`
- Rail Fence Cipher:
- Brute force
- `password:·VSEAS5aevg8Bwlovr`

Layer 4 - `Salad Time`
- Keyed Caesar Cipher
- Key is `neverLANCTF`
- Shift is `0`
- Password is `gTLvCGk$HyRVSssXVaSX`

Layer 5 - `ROTten`
- Standard Caesar Cipher
- Shift is `13`
- Password is `e1Ydr*zxOOybF6RR%h5f`

Layer 6 - `Vigenere Equivent E`
- Standard Caesar Cipher
- Shift is `22`
- Password is `fI7BPZL#ZN5PI!&pbTXc`

Layer 7 - `Easy one`
- Base64 encoded string
- Password is `vxw@Ztet#ZfBnYVxJ1IM`

Layer 8 - `Message indigestion`
- MD5 digest
- Brute force
- Password is `password23`

Layer 9 - `For SHA dude`
- SHA1 digest
- Brute force
- Password is `applez14`

Layer 10 - `ONE more TIME`
- One Time Pad
- First part of key is `This is our world now...` from `chal.txt`
    - Hints to a section from the Hacker Manifesto
- Full key is: `This is our world now... the world of the electron and the switch, the
beauty of the baud.  We make use of a service already existing without paying
for what could be`
- Decrypt the OTP to get the flag

### It is like an onion of secrets
We get download the png image. In it is a funky lookin dog with no flag :(

We guess it is LSB encrypted since Binwalk doesn't return anything useful.

We plug it into [stylesuxx's LSB tool](https://stylesuxx.github.io/steganography) and we decode.

We get some base64, which we now play with a bunch in [CyberChef](https://gchq.github.io/CyberChef/).

After we base64 decode it twice, we get a bunch of:
`lspv wwat kl rljvzfciggvnclzv`

Now we guess again and decrypt it using the `Variant Beaufort Vigenere cipher` (found on Cryptii's Vigenere tool) and key `NeverLANCTF`. The plaintext gives the flag.

## PCAP
### Unsecured Login
You don't even need Wireshark, just use `strings mysite.pcap | grep flag`

### Unsecured Login2
You don't even need Wireshark, just use `strings mysite2.pcap | grep flag`

### FTP
You don't even need Wireshark, just use `strings ftp.pcap | grep flag`
If you want to, you can right click on any ftp packet and follow the tcp stream. If there's no flag, then move on to the next stream.

### Teletype Network
You don't even need Wireshark, just use `strings telnet.pcap | grep flag`

### hidden-ctf-on-my-network
You don't even need Wireshark, just use `strings telnet.pcap | grep flag`

## Forensics
### Listen to this
When we listen to the mp3 initially, we can hear a faint beeping in the background. This sounds like Morse code, so let's find an easy way to transcribe it to text dits and dahs (radio speak for dots and dashes).

We open it up in Audacity, and notice there are two tracks. Let's switch to spectrogram view. We can do this by clicking on the arrow pointing downwards next to the track name, then clicking `Spectrogram`:
![](https://i.imgur.com/jrIw77T.png)

If we zoom in on the beginning of the track, we can see that the Morse code is in the second track:
![](https://i.imgur.com/FaffDFU.png)

One huge issue right now is that the Morse code is "covered" by the actual vocals of the track. I was stuck on this portion for a while.

Let's split the tracks to mono using the track settings.

Then, we subtract the original track from the track with morse code. After that, we'll be able to clearly see the morse code in spectrogram view.

First, we select one track, and invert it (`Effect > Invert`). Then, we select both tracks and mix them together (`Tracks > Mix > Mix and Render`).

It's still a bit hard to see, so let's change the coloring.

We open up track settings and then select `Spectrogram Settings`. We change the color range to 20 dB instead of 80 dB (decibels).

The result is morse code. Now all we have to do is open up a text editor, copy the morse code down, and convert it to text using an online tool (:

The short ones are dits and the long ones are dahs. I usually represent the short ones with `.` and the long ones with `-`, which is a format most online morse-to-text tools use as well.

![](https://i.imgur.com/nMOCs8o.png)

That would be the first letter in the text.


### Open Backpack
The image says something is unzipped...
Let's try `binwalk`.

Command: `binwalk -e openbackpack.jpg`

Binwalk extracts two files, a zip and a file called `flag.png`, which has the flag of course.

### Look into the past

## Programming
### DasPrime
We want to find the 10947th prime number. We are given the following algorithm:
```python
import math
def main():
    primes = []
    count = 2
    index = 0
    while True:
        isprime = False
        for x in range(2, int(math.sqrt(count) + 1)):
            if count % x == 0: 
                isprime = True
                continue
        if isprime:
            primes.append(count)
            print(index, primes[index])
            index += 1
        count += 1
if __name__ == "__main__":
    main()
```

This algorithm seems kind of slow...

We can write a faster script such as this one:
```python
from math import sqrt

def is_prime(n):
    if (n <= 1):
        return False
    if (n == 2):
        return True
    if (n % 2 == 0):
        return False

    i = 3
    while i <= sqrt(n):
        if n % i == 0:
            return False
        i = i + 2

    return True


def prime_generator():
    n = 1
    while True:
        n += 1
        if is_prime(n):
            yield n

generator = prime_generator()

x = []


for i in range(10948):
    x.append(next(generator))
```

We access the 10497th element of `x` to get the flag (x[10496]).

### password_crack
Simple MD5 brute force. I got the author names from the Discord server.
More on this later when they publish the challenges again (they took them down).

### Robot Talk
We just have to convert 5 base64 values to ASCII.

I used pwntools, a pretty neat library for tasks like these.

```python
from pwn import *
import base64

conn = remote("challenges.neverlanctf.com", 1120)


for i in range(5):
	print(conn.recvuntil("decrypt: "))
	x = conn.recv().strip()
	print(x)
	y = base64.b64decode(x)
	print(y)
	conn.send(y)
	print(conn.recvline())

print(conn.recv())
```
### BitsnBytes
> https://challenges.neverlanctf.com:1150

This site gives an svg which we can download. Quite obviously, the colors represent `0` and `1` in binary (gray is 1, green is 0).

We find out that we can download the svg information directly from `/svg.php`, which makes it much easier for a script.

We parse the image, using regex to remove all different attributes such as x, y, width, and height for each `<rect>` in the svg. Then, we simply just use `str.replace()` in Python to get the binary string.

Then we convert that binary string into text.

However, most of the time the server will return an svg that doesn't have the flag. Instead, it will return some time hash information which is useless to us.

We can repeatedly query the server for an svg until it gives us a flag svg.

```
from __future__ import print_function


import requests

while True:
        f = requests.get("https://challenges.neverlanctf.com:1150/svg.php").text.decode()


        f = f[336:-9]

        f= f.strip()

        import re

        s = re.compile(r"\sid='\d*'")
        a = re.compile(r"\sx='\d*'")
        b = re.compile(r"\sy='\d*'")

        c = re.compile(r"width='\d*' ")
        d = re.compile(r"height='\d*' ")

        f = s.sub("", f)
        f = a.sub("", f)
        f = b.sub("", f)
        f = c.sub("", f)
        f = d.sub("", f)

        #print(f)

        f = f.replace("<rect style='fill:#333136'/>", "1")
        f = f.replace("<rect style='fill:#00ff00'/>", "0")

        f = [f[i:i+8] for i in range(0, len(f), 8)]

        #print(f)

        x = "".join([chr(int(i, 2)) for i in f])

        if not "time hash:" in x:
                print(x)
```

### Evil
> ssh neverlan@medusa.neverlanctf.com -p 3333
> password: eyesofstone

We initially find an intel.txt, giving us information. We have to ssh onto `evil@victim`.

Using Medusa (an ssh password cracker), we can bruteforce the password easily. It is `0024`.

Once ssh'd, we find a zip file with some base64 as its name. It's password protected, so we try decoding the name.

Decoded, the name of the zip file is `stonecold`, which is used to unzip the zip file.

The content of the zip file is the flag.

## Recon
### Front page of the Internet
The "front page of the Internet" is Reddit.
The author is `ZestyFE`, so we guess that he has a Reddit account under the same name.

We navigate to `/u/ZestyFE` on Reddit, and find the flag in one of ZestyFE's comments.

### The Big Stage
We search up SaintCon keynotes and find that NeverLAN keynoted in 2018

Unfortunately the SaintCon site is not 100% functional so we're stuck...

Then we guses that keynoting a conference is pretty cool and they must have posted something to commemorate the event on [their Twitter](https://twitter.com/NeverLanCTF).

They actually link us [their slides](https://twitter.com/NeverLanCTF/status/1044640438131388422)

The flag is right next to a picture of Rick Astley :p


### The Link
During the competition there were streams for music and the like. If we go under their music tab and select track #2 we see a YouTube video.

Exploring the comments reveals a flag that someone commented.

### Thats just Phreaky
We Google for `01 September 2017 | 14:01 phreak`.

We find the first [Darknet Diaries episode](https://darknetdiaries.com/episode/1/).

By some stroke of pure geniosity we right click to view the source code of the site and the flag is at the bottom.

## Web
### Cookie Monster
> https://challenges.neverlanctf.com:1110

The title hints that it has something to do with cookies.

When we visit the site, it says `He's my favorite Red guy`. We guess this to be `Elmo` from Sesame Street.

We look at the cookies, and find a cookie `Red_Guy's_Name: NameGoesHere`. We replace `NameGoesHere` with `elmo`.

We get the flag by refreshing the tab.

### Stop the Bot
> https://challenges.neverlanctf.com:1140

The site looks pretty boring, so let's take a look at `/robots.txt`, which is hinted at by the title:
```
User-agent: *
Disallow: /
Disallow: flag.txt
```

We navigate to `/flag.txt` for the flag.

### SQL Breaker
> https://challenges.neverlanctf.com:1160/

Simple SQL injection in the login page.
Note that the password does not matter, only the username is vulnerable.

The goal is to log in as an admin.

Payload:
```
Username: ' OR 1=1;-- 
Password: asdf
```

Return to the home page for the flag.

### SQL Breaker 2
> https://challenges.neverlanctf.com:1165/

Simple SQL injection in the login page.
Note that the password does not matter, only the username is vulnerable.

The goal is to log in as an admin.

This time, there seems to be multiple accounts, and the previous payload logs us in as `John`, who is not an admin. We have to skip over John's account using SQL's `LIMIT` to log in as admin.

Payload:
```
Username: ' OR 1=1, LIMIT 1;-- 
Password: asdf
```

Return to the home page for the flag.

### Follow Me
> https://7aimehagbl.neverlanctf.com

This website redirects so many times your browser just gives up. We can use Python's `requests` module and the `follow_redirects=False` option:
```python
import requests
p = requests.get("https://7aimehagbl.neverlanctf.com", allow_redirects=False)
```
On the first visit (using Python), the page states where it's redirecting. How convenient. How about we just follow the trail?

```python
import requests

url = "https://7aimehagbl.neverlanctf.com"

while True:
    p = requests.get(url, allow_redirects=False)
    print(p.text)
    url = "https://" + p.text.split()[-1]
```

The flag is in one of the sites that we get redirected to.

### Browser Bias
> https://challenges.neverlanctf.com:1130

When we try to visit the site normally, it says that the site is only for `commodo 64` browsers.

We guess that the server tells what browser we are using based on the User-Agent header of the request.

When we Google for Commodo 64 browsers, we end up with a browser named `Contiki`. We search for the Contiki User-Agent.

We find a [really long list of User-Agents](https://gist.github.com/dstufft/2502524) that ever downloaded something from PyPI on GitHub Gists, and we Ctrl-F for Contiki.

We find the User-Agent for Contiki as `Contiki/1.0 (Commodore 64; http://dunkels.com/adam/contiki/)`.

We set that as our User-Agent using Python's `requests`, and request the home page, which gives us the flag.

## Chicken Little
### Chicken Little 1

### Chicken Little 2
### Chicken Little 3
### Chicken Little 4
### Chicken Little 5
### Chicken Little 6
### Chicken Little 7

## Trivia
### Milk Please
> Trivia Question: a reliable mechanism for websites to remember stateful information. Yummy!
>
It's talking about cookies, which is the flag.
### Professional Guessing
> The process of attempting to gain Unauthorized access to restricted systems using common passwords or algorithms that guess passwords

Google the description.

An article defines the description for the term "password cracking", which is the flag.
### Base 2^6
> A group of binary-to-text encoding schemes that represent binary data in an ASCII string format by translating it into a radix-64 representation

`Radix-64` basically tells us that the flag is base64.

### AAAAAAAAAAAAAA! I hate CVEs
> This CVE reminds me of some old school exploits. If flag is enabled in sudoers

We Google `If flag is enabled in sudoers cve` and find [this site](https://www.exploit-db.com/exploits/47995), which has the flag in it.

### Rick Rolled by the NSA???
> This CVE Proof of concept Shows NSA.go<span>v</span> playing "Never Gonna Give You Up," by 1980s heart-throb Rick Astley.
Use the CVE ID for the flag. flag{CVE-?????????}

I remember seeing this as a meme on Reddit :laughing:
Googling the description gives news articles detailing the correct CVE ID for the flag.
