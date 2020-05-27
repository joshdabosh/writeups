# Login
Web, 30

>  Written by saisree
>  Could you login into this very secure site? Best of luck!

Looking at the source, we can see that clicking on the `Login` button calls `checkUsername()`. Here's the pretty-printed definition of the function:
```js
checkUsername = function() {
    username = document[_0x4a84('0x1')]('username')[0x0]['value'];
    password = document[_0x4a84('0x1')]('password')[0x0][_0x4a84('0x3')];
    temp = md5(password)[_0x4a84('0x2')]();
    if (username == _0x4a84('0x6') && temp == _0x4a84('0x4'))
        alert(_0x4a84('0x0') + password + '890898}');
    else
        alert(_0x4a84('0x5'));
}
```
Some strings have been obfuscated, but we can just copy the function call into the javascript console to get the strings. Here is the deobfuscated version:
```js
checkUsername = function() {
    username = document.getElementsByName('username')[0].value;
    password = document.getElementsByName('username')[0].value;
    temp = md5(password).toString();
    if (username == "admin" && temp == "c2a094f7d35f2299b414b6a1b3bd595a")
        alert("tjctf{" + password + '890898}');
    else
        alert("Sorry. Wrong username or password.");
}
```
So, we just plug `c2a094f7d35f2299b414b6a1b3bd595a` into crackstation, and get the password of `inevitable`, then login with username `admin` and password `inevitable` to get the flag.

Flag: `tjctf{inevitable890898}`