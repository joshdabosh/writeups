# Secret-Flag
Pwn, 348

There's a super secret flag in printf that allows you to LEAK the data at an address??
>
> nc 2020.redpwnc.tf 31826

Going from the description I assumed the flag is on the stack somewhere. Reading source shows fstring vulnerability, so I spammed offsets of %s until I got the flag.

I deleted my solve script but basically you use a for loop and iterate from 0 to some decently high number. Each time, you connect to the service and enter your name as `%<i>$s` to print the `i`th value on the stack as a string.