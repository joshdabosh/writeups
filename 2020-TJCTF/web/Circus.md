# Circus
Web, 80

>  Written by KyleForkBomb
>  They called me a clown for using PHP, but little did they know I used military-grade SHA256! I'll bet you can't even login to a single account! Brute force is NOT required http://circus.tjctf.org/

We find a git directory at https://circus.tjctf.org/.git/HEAD. Using a git dumper, we can get the entire directory, which contains the source for the program. We can see that the password hashes are compared with `==`, which is insecure because PHP sucks.

We can look at previous versions of the website as well through the git history. We find a database backup with a list of users and password hashes.

One of the users, `Andon1956`, has a password hash of `0e75759761935916943951971647195794671357976597614357959761597165`. Since PHP sucks, this hash is interpreted as the number `0`. We can log in with a string that produces a [SHA256 magic hash](https://github.com/spaze/hashes/blob/master/sha256.md) such as `34250003024812` and get the flag. 

Flag: `tjctf{juggl1n9_cl0wn_up_in_th3_b4ck}`