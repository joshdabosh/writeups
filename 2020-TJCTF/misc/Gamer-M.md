# Gamer-M
Misc, 100

>  Written by boomo
>  I just fixed my old-school-ninja-kung-fu-mega-fighter game! I think there may be a few cheat codes built in though!
>  Users
>  
>  nc p1.tjctf.org 8007 

Here's the source:

```py
import random

def shuffle(s):
	for i in range(len(s)):
		j = random.randint(0, len(s) - 1)
		s[i], s[j] = s[j], s[i]
	return s


def combat(level):
	rps = ['rock', 'paper', 'scissors']
	crit = rps[random.randint(0, 2)]
	if crit == 'rock':
		print('A disciple stands in your way! Take your action!')
	elif crit == 'paper':
		print('A disciple blocks your way! Take your action!')
	elif crit == 'scissors':
		print('A disciple stalls your advance! Take your action!')

	print('\tChoose your weapon (\'rock\', \'paper\', \'scissors\')')
	if input('\tChoice: ').lower().strip() == crit:
		print('Sucess!')
		for name, c in level:
			print('%s dropped: %s' % (name, c))
		print('You rest and continue your journey.\n')
		return 1
	else:
		print('It wasn\'t very effective! The disciple counters with a seven page combo of punches and you die.')
		print('Try again when you reincarnate.')
		return 0


def game():
	flag = open('flag.txt').read().strip()
	names = shuffle([i.strip() for i in open('names.txt').readlines()])
	match = [(names[i], flag[i]) for i in range(len(flag))]

	levels = shuffle([shuffle(match[::5]), shuffle(match[1::5]), shuffle(match[2::5]), shuffle(match[3::5]), shuffle(match[4::5])])

	print('Welcome to the temple.\n' + \
		'\n' + \
		'You will face five tests.\n' + \
		'Each test involves combat against five disciples.\n' + \
		'Each disciple holds a key.\n' + \
		'Combine the keys to unlock the scroll\'s message.')

	for n, level in enumerate(levels):
		print()
		print('- = - Level %i - = - ' % (n + 1))
		if not combat(level):
			return

	print('You triumphed over all trials!')


if __name__ == "__main__": 
	game()
```

It's very easy to get characters in the flag, (disciple stands = rock, disciple blocks = paper, disciple stalls = scissors), but the characters are all scrambled up and it's hard to find their order. Luckily, the characters are split up into groups of 5 groups of 5, and they're only scrambled within their group. This means we can get 5 groups, and we can order the groups based on known characters in the flag format:

```
1: tR06{
2: e3bij
3: o5c4n
4: AtrC2
5: JFfx}
```

Now, it turns out the `shuffle` function does not fairly shuffle, and has the greatest probability to turn `12345` into `21453`. This means that, with enough data points, we can unshuffle the flag. Here's my script to automatically collect data:

```py
from pwn import *
import json

def lvl(p):
    p.recvuntil("- =")
    p.recvline()
    line = p.recvline()
    if b"stands" in line:
        p.sendline("rock")
    if b"blocks" in line:
        p.sendline("paper")
    if b"stalls" in line:
        p.sendline("scissors")
    chars = b""
    p.recvuntil("Sucess")
    for i in range(5):
        p.recvuntil(": ")
        chars += p.recv(1)
    return chars.decode("utf8")

def play():
    p = remote("p1.tjctf.org", 8007)
    ret = []
    for i in range(5):
        ret.append(lvl(p))
    p.close()
    return ret

context.log_level = "error"
freqs = {}
for i in range(10000):
    if i % 10 == 0:
        with open("freqs.json", "w") as jsonf:
            json.dump(freqs, jsonf)
        print(f"at index {i}", file=sys.stderr)
    for fs in play():
        charset = "".join(sorted(fs))
        if charset not in freqs:
            freqs[charset] = {}
        if fs not in freqs[charset]:
            freqs[charset][fs] = 0
        freqs[charset][fs] += 1

print(freqs)
```

It turns out I had to run it twice to get 20000 data points before the distributions were correct, but the most common orderings were:
```
1: {tR60
2: ije3b
3: 5cn4o
4: AtC2r
5: Jfx}F
```

Unscrambling them by reversing the `21453` permutation we get:
```
1: t{0R6
2: jibe3
3: c5on4
4: tArC2
5: fJFx}
```

Making the flag: `tjctf{i5AJ0borFRenCx6342}`