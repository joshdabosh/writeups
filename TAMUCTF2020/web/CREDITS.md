# CREDITS
Web

> Try testing out this new credit system that I just created!
>
>http://credits.tamuctf.com/
>
>Hint: Credit generation is rate limited. It is literally impossible to generate 2,000,000,000 credits within the CTF timeframe. Don't be that guy.

After making an account on the website, it's pretty clear what we have to do: get a load of credits.

We see some function definitions in the body of the HTML document. Let's change the `increment` parameter in the POST data to `2,000,000,000`.
```
data: {
increment: 2000000000
}
```
After that we can just modify the function definition by copypasting our function into the console.

![](https://i.imgur.com/xyQdoEZ.png)

Now after we click the button, it gives us all our credits. With that, we can buy the flag.

This is the part that pisses me off the most because I would have blooded it otherwise >:(

We have to go to our inventory to view the flag.

Flag: `gigem{serverside_53rv3r5163_SerVeRSide}`.

They had a CSRF sequel to this which I also solved but it got removed :(
