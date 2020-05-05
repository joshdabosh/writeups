# Fire-place
Web

> You see, I built a nice fire/place for us to all huddle around. It's completely decentralized, and we can all share stuff in it for fun!!
> Hint! I wonder... what's inside the HTML page?

Inspecting the source of the HTML doc reveals that this uses Google FireBase's FireStore.

We can get a DB reference to the `data` collection by typing the following in the console:

```javascript
var x = await db.collection("board").doc("data").get()
console.log(x.data())
```

(`.get()` returns a Promise so we have to await it)

After a few more minutes of poking around I told a teammate and left.

The solution was to guess that there was another document named `flag` and retrieve that:

```javascript
var x = await db.collection("board").doc("flag").get()
console.log(x.data())
```

angery :(

Flag: `rtcp{d0n't_g1ve_us3rs_db_a((3ss}`
