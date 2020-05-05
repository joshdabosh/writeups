# Patriot CTF 2020
DiceGang got [1st](scoreboard.png).

Sentence writeups because I needed an excuse for repo housekeeping.

## 2+2
Base 62 decode.

## Dilbert Random
We need a number from an [RFC 1149.5 compliant generator](https://xkcd.com/221/). The right number is 4.

## CYSE 425
We can use [this tool](https://www.tunnelsup.com/hash-analyzer/) to analyze the hash we're given. Turns out it's SHA1.

We use CeWL to generate a custom wordlist of the site (as hinted from the description), and store that in a file.

We run `hashcat -m 1000 hash.h wordlist.txt` to find the right password.

## Break This Hash
We can use [this tool](https://www.tunnelsup.com/hash-analyzer/) again to analyze the hash we're given. Turns out it's MD5.

From the format of the challenge description we can guess that it's referring to [what3words](https://what3words.com/). Using the coordinates we can build a dictionary to attack the hash with.

`hashcat -m 0 hash.h wordlist.txt`
