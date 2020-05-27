# Rap-God
Forensics, 40

>  Written by rj9
>  My rapper friend Big Y sent me his latest track but something sounded a little off about it. Help me find out if he was trying to tell me something with it. Submit your answer as tjctf{message}

When we open in Audacity we see that one track is clearly different. Let's split to mono and switch to spectrogram view. The second track becomes:

![](https://i.imgur.com/Gc8jEIj.png)

After reconning we find that those symbols spell out `sonic` in wingdings font. Doesn't work as a flag. We then for some reason decide that we must expand our frequency range in Audacity by adjusting spectrogram settings. While we're at it, we can also make the symbols clearer by changing the gain to around 6-7.

We get:

![](https://i.imgur.com/IKAhO7g.png)

Translating from wingdings, the flag is revealed.

Flag: `tjctf{quicksonic}`