# Titanic
Crypto, 35

>  Written by jpes707
>  I wrapped tjctf{} around the lowercase version of a word said in the 1997 film "Titanic" and created an MD5 hash of it: 9326ea0931baf5786cde7f280f965ebb. 

Copy the Titanic script from [online](https://subslikescript.com/movie/Titanic-120338) and test all the words. Script below:
```python
from hashlib import md5
import string
with open("script.txt") as f:
  words = set(f.read().strip().lower().split())
  for word in words:
    flag = "tjctf{%s}"%word.strip(string.punctuation)
    if md5(flag.encode()).hexdigest()=="9326ea0931baf5786cde7f280f965ebb":
      print(flag)
      break
```
This gives us the flag: `tjctf{marlborough's}`

Note: I looked at four different scripts; only the one linked above worked. Two of the scripts didn't have this word at all, and another script replaced this with the word `Malborough's` without the `r`. A previous version of this challenge had the flag `tjctf{ismay's}`, and the three other scripts all had that word. The script linked above used the word `lsmay's`, presumably as a copyright trap.