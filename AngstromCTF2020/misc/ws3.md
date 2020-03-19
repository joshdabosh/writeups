# ws3
Misc, 180

> What the... record.pcapng
> Linked: record.png

For the record, I hate the fact that I named this one's recording `record.pcapng` and the others' `recording.pcapng`. Oh well.

This was probably my coolest challenge :sunglasses:.

Right away, we can see that I interacted with some sort of Git server (it was Gitea on my laptop).

There seem to be a lot of `unauthorized` messages, which were definetely on purpose.

We can narrow our list of data to check by only looking at the exportable HTTP objects:
![](https://i.imgur.com/c4WhkgG.png)

Packet #76 seems to be of key interest, since it's the largest. Let's start there.

We export the packet's data, and open it in a hex editor. This seems to be a git pack file, which we can find specifications for [here](https://git-scm.com/docs/pack-format).

![](https://i.imgur.com/lMoW3rN.png)

The specifications say that git packs start with the 4 bytes `PACK`, so let's delete everything up to that and save it as a `.pack` file.
![](https://i.imgur.com/DX4qtWm.png)

With our full pack file, we can now embark on our quest of getting the content of the repository back.

We move our pack file into an empty repository, and then turn it into an empty git repository by running `git init`.

Then, we can unpack the pack file using `cat new.pack | git unpack-objects`.
![](https://i.imgur.com/E7eB7iG.png)

:eyes: looks like we got stuff!

Since our repository still technically has 0 commits, `git log` is useless. So, we navigate to `.git/objects/`, and `ls.`
![](https://i.imgur.com/Lokk974.png)

Let's check out `34/`. We find a commit "body" (or whatever it's called).

We can use `git show <hash>` to print the contents of the body. Make sure to use `foldername+bodyname` as the hash, as that's just how git works.

![](https://i.imgur.com/uCE3fO5.png)
Oh... welp.
Let's try another one.![](https://i.imgur.com/QpV0WZZ.png)

Voila, there's a flag.jpg in this commit. Let's save the contents:
![](https://i.imgur.com/4zB7fvQ.png)

Now, when we open up `flag.jpg` in the root of our repository, we get a cool picture of Kaguya-chan, with the added bonus of a flag :).

Flag: `actf{git_good_git_wireshark-123323}`