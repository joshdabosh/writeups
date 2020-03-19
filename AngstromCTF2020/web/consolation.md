# consolation
Web, 50

> I've been feeling down lately... Cheer me up!
>
> Linked: https://consolation.2020.chall.actf.co

50 points, should be relatively easy.

Upon opening, we see a button. Taking from the challenge name, we open the console.

Every time we click the button, the dollar count gets incremented by 25, and the console gets cleared.

Let's disable that. For some browsers even the "preserve log" option does not work, so we think of a high IQ move: we temporarily clear the code of the clearing function:
`console.clear = ""`

Now, we just click it again and the flag is displayed.

Flag: `actf{you_would_n0t_beli3ve_your_eyes}`

(if you didn't notice, the flag was printed from `iftenmillionfireflies.js` :D)

I've heard that some people solved by overwhelming the console through using a loop to click the button. Also, I repeatedly obfuscated the source code of the js file in order to get people to solve it using the console.