# Login-Sequel
Web, 40

>  Written by saisree
>  Login as admin you must. This time, the client is of no use :(. What to do? 

This challenge gives a login page vulnerable to SQL injection but it seems to have a blacklist for certain substrings.

Specifically, `--` is blocked, so `admin' -- ` doesn't work.

Trying a different comment string, `admin' /*`, gives us the flag: `tjctf{W0w_wHa1_a_SqL1_exPeRt!}`.