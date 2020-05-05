# DeepCTF 2020

If you thought NeverLAN was bad (it was okay), just wait until you experience DeepCTF.

As someone in their Discord server said,
> I understand this is the first time these people have organized a CTF
and a lot can go wrong for the first CTF
but holy sh*t you guys got so many things wrong

Put together for the first time by [http.deep](https://ctftime.org/user/63655) and co, I grew wary of their presence after someone decided to advertise their Discord server after AngstromCTF 2020 concluded.

Rather than writeups or a guide on improvement, this'll just be a document for recording what went down in the CTF from our side. Hop in.


## Overview
The CTF ran from 6:30 AM EST 4/4/20 to 6:30 AM EST 4/5/20 - 24 hours long.

In the span of about 24 hours (really 18 hours since I started at around 12), I along with other b1c members:
- [maxed the initial release of problems, leveling out at 2nd for a while](#maxing)
- [first blooded at least 3-4 challenges and climbed to first](#first-bloods-and-first-place)
- ["took down" a challenge site accidentally](#taking-down-greetings-accidentally)
- [got banned from the CTFd site](#ctfd-ban)
- [got banned from the Discord server (3 times, 3 accounts)](#discord-server-ban)
- [pissed off the admins](#pissed-off-admins)
- [listened to bad ban excuses](#bad-ban-excuses)

For reference, these are the official rules as stated on their CTFd website.
![](https://i.imgur.com/kayGIEx.png)


## Maxing
Initially I hoarded some flags as I was unsure if b1c wanted to do it. Then we decided to do it and I dumped.
![](https://i.imgur.com/SuQO0b3.png)

We finished our last (first-batch) problem at around 8 PM EST. At this point we kind of complained about the extreme guessiness of the challenges in the server, but the admins didn't seem to care.

## First bloods and first place
Random challenges got released and they were all pretty easy, so I ended up blooding at least 3 of them. My solving streak continued well into 4AM EST. That's when the `Greetings!` challenge appeared.

## Taking down Greetings accidentally
It's funny how there were 2-3 challenges from DeepCTF that were blatantly copied from other thigns. This challenge was basically ripped off [this article](https://ajinabraham.com/blog/server-side-template-injection-in-tornado), which is the first result on Google when searching for `tornado ssti`.

I didn't realize it was running Tornado, so I just tried some generic SSTIs. One of them (I forget) made the site hang, and refreshing didn't work. So, being someone with a nonzero IQ, I contacted the admin.

## CTFd Ban
A few minutes after contacting the admin, I was banned from the CTFd site.

![](https://i.imgur.com/Pb9SiQZ.png)


When I asked for the reason for the ban, I was told,
> can't trust

(???) repeatedly. Our log is below.

![](https://i.imgur.com/bMAWUZD.png)

After further inspection, it turns out that my payload didn't actually crash and was the INTENDED solution. The admin still kept my ban.

![](https://i.imgur.com/SsvpTLC.png)
![](https://i.imgur.com/PDcFxaz.png)

Later, it turns out that spawning a "reverse shell" (only to find out where the flag was) was against the rules. What a joke.

![](https://i.imgur.com/xcoCa2c.png)

The most hilarious thing to me about this statement is that we never even submitted the flag. Take it from this screenshot, go to our team profile on their site[, even look at the logs from the admin in [Bad ban Excuses](#bad-ban-excuses): we did not submit the flag.

![](https://i.imgur.com/LGoqEu1.png)


## Discord Server Ban
Shortly after my CTFd ban, the admins decided to make memes about it. Here's an admin advertising the memes.

![](https://i.imgur.com/eFO6qyn.png)

Enjoy some lower-than-F-tier memes from [SherlockHolmes](https://instagram.com/@holmes._._) himself (:

![](https://i.imgur.com/PLHLsr9.png)
![](https://i.imgur.com/wOiMxMp.png)
![](https://i.imgur.com/Nub3qBI.png)
![](https://i.imgur.com/wvdcO0t.png)
![](https://i.imgur.com/oM7aXFI.png)

(sorry for terrible cropping).

The Phil Swift one is particularly funny to me because Phil Swift slapping on Flex Seal to stop the leak is usually seen as an expression of irony / mockery.

Of course, me with my ~30k Reddit karma couldn't resist.

![](https://i.imgur.com/Igl9mOi.png)
![](https://i.imgur.com/PtmRPDc.png)

I was then banned. Reason?

![](https://i.imgur.com/2W0ws3w.png)

Nice. Seems like they can't take their own medicine.

![](https://i.imgur.com/9XT3UWG.png)

This is only the start of how a solid part of my Sunday was spent.


## Pissed off admins
After getting banned from the Discord server as well, I let my teammates know and I went to sleep (at around 6 AM EST). I woke up to our teammates arguing with the admins who refused to unban us after the CTF ended.

I quickly rejoined with a new account, h_yi. I ended up getting banned again and my messages were deleted, but there's still plenty screenshots to go around.

The admins got so annoyed when we weren't satisfied with their lousy excuses (more on that later) that they decided to revert to "OK BOOMER"s, switching to conversing in Hindi, and even sending and tolerating blatant slurs against us (Asians).

"OK BOOMERS":

![](https://i.imgur.com/PNDW0uo.png)

![](https://i.imgur.com/nLxLcaH.png)

Hindi (it goes on forever but I don't want this document to be THAT long):

![](https://i.imgur.com/mInGa5x.png)

![](https://i.imgur.com/IxUSmif.png)

![](https://i.imgur.com/Mz7jiYN.png)

As a counter, I started speaking in Chinese. I was using my alt, `h_yi`, at the time. It seems the messages from me directly got deleted, but quotes are still there. They started slurs after, mostly calling us pandas.

Slurs:

![](https://i.imgur.com/tAnheaT.png)

![](https://i.imgur.com/YjubwfQ.png)

![](https://i.imgur.com/VJyica9.png)

![](https://i.imgur.com/RVjMdUj.png)

![](https://i.imgur.com/pyQU8kP.png)

![](https://i.imgur.com/ma3CSHb.png)

![](https://i.imgur.com/Qra4ivS.png)

![](https://i.imgur.com/CEyILia.png)

![](https://i.imgur.com/HUtZkyU.png)

![](https://i.imgur.com/FcMSRr4.png)

This stuff is disgusting.

## Bad ban excuses
I (h_yi) was banned again. So, I registered another account, 0xpwn, and decided to go under the guise of a Spanish speaking haxxor. ~~This is the account I'm still using to access the server now.~~ I got banned again.

After long interrogation, the admins collectively revealed that we were banned for:
- flaming their CTF
- offending admins
- taking down infrastructure intentionally
- sharing flags with another team
- getting a reverse shell (on a web chall)

I've already explained the first three, and how they don't make sense.

The last statement is basically a "lol what??". I think they were referring to either Greetings ("solved" by me) or another web (solved by Aplet). In both cases we didn't know where the flag was so we had to run an `ls` first.

However, they decided to throw another excuse at us: we shared flags with another team, `test123`.

The admins cite this as their only evidence:

b1c log

![](https://i.imgur.com/PLEscIp.png)

test123 log

![](https://i.imgur.com/v8YFYR2.png)

I have to admit, from a context-less background it does look slightly suspicious. However, when you take into account that:
- the challenges were released in that order
- both teams are in the top 10, so they're going to solve quickly
- b1c solved consistently earlier than test123

the argument that we shared flags falls apart.

If you think of it logically: why would I, a team in contention for prizes, give flags to another team in contention for prizes? The admins refuse to answer this question.

The only situation plausible is that I gave flags to test123, which didn't happen. I can't even contact test123 because I don't know who they are, whereas my Discord username, JoshDaBosh, basically go hand in hand with my CTF username, bosh.

The admins refused any form of justification from our side. We offered writeups, but they were unconvinced. I guess that's what happens when your challenges are trivially easy and rely on guesswork to solve.

Even more suspicious is how the admins did not want to give out who was on `test123`.

![](https://i.imgur.com/FDMWGN1.png)

We're both banned, we're innocent (at least on my side), why not let at least the affected talk to each other? No clue.

The admins also decided to start talking trash about b1c, which was ironic because we just got 5th and qualified in Midnight Sun Quals as part of okay blue (tuxicide) less than 12 hours after the CTF ended.

![](https://i.imgur.com/nybicTa.png)

![](https://i.imgur.com/Yvnqtsc.png)

## Summary
This CTF was a clear example of not only what to avoid challenge-wise, but also an example of poor administration and an overall lack of reasoning. 

However, it's not like we missed out on much - first to third place were subscriptions to PentesterLabs, and top 15 got... wait for it... certificates!

We fought mainly to just clear b1c's name. The admins refused to do that, as well. They kind of remind me about a particular trait of Fujiwara Chika.
