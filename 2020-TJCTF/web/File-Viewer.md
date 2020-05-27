# File-Viewer
Web, 70

>  Written by saisree
>  So I've been developing this really cool site where you can read text files! It's still in beta mode, though, so there's only six files you can read.

There's LFI in the file query parameter, and it turns out there's RFI as well, which means you can put a url in the query parameter and it'll send a request to the url and render the page. Even better, it renders PHP!

So, I just put a PHP webshell in pastebin and found the flag by running `ls` a couple of times.

The flag was in a file called `flag.php`, under a directory called `i_wonder_whats_in_here`.

Flag: `tjctf{n1c3_j0b_with_lf1_2_rc3}`