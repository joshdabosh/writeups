# MAGIC oCTF 2020

b1c takes first! :)

## nortum_client
No description here since the challenges locked after the CTF ended.

Basically we are given a binary called [nortum_client](nortum_client). We are supposed to implement a socket server, and we'll get the flag somehow.

The binary is compiled with nuitka, which makes decompiling pretty difficult.

The challenge description also gives us important clues:
- We have to format our server messages as `<Line> <Line> <Data> [line] [line] [line] ...`
- We have to bind our server to port 1228
- We have to send 2 big or little endian unsigned ints to the server

It takes a bit to think of the right way to interpret it, but the correct way to send data is:

`\n\n<packed number><packed number>\n\n\n`

Now to analyze the binary, we can try running `strings` on the binary:
```
?127.0.0.1decodeAF_INETpackaged_answerabsdiffcombinedencodeosError preforming arithmetic function. Incorrect data type?utf-8IPUnknown error packing and sending reply.socketConnection to the server failed. Verify that the IP and port are correct.charscp437intsError unpacking data. Incorrect data type?sub__debug__Did not receive correct confirmation response.received_datatimeoutbuild_flagrecvsetblockingNo message was received before timeout.Sent flag.splitlinesitem>Istart_timeWaiting for welcoming message. . .
TrueexitWaiting for boolean response. . .
SOCK_STREAMnumconnect
Received tuple: %smsgrecv_timeoutbytes_linestrstructsleepFalseprint_received_msgReceived message doesn't have the correct formatting.types
Sending answer. (%s)syssendall<module>/root/Desktop/nortum_client_packed.pyappendReceived correct confirmation.PORT
```

In the mess above we can see a `>I`, so we can most likely assume that's how the server is unpacking bytes we send, meaning it wants big endian (`>`) unsigned ints (`I`), according to Python's [struct documentation](https://docs.python.org/2/library/struct.html).

After some light guesswork, our binary does the following:
- Connect to 127.0.0.1 on port 1228
- Expect a welcome message
- Validate a welcome message
- Do some operations on the welcome message
- Send something back
- Wait a confirmation value back
- Validate the confirmation value
- Give the flag

We can implement a basic Python socket server:

```python
import socket, struct

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print "ok"

port = 1228
s.bind(("", port))

print "bound to 1228"

s.listen(5)

print "listening"

while True:
	c, addr = s.accept()
	print "conn from ", addr

	c.sendall("\n\n" + struct.pack(">I", 1234) + struct.pack(">I", 1234) + "\n\n\n") # send two big endian unsigned ints

	data = c.recv(4096) # receive response
	print struct.unpack(">I", data) # view response
	c.close()
    
s.shutdown()
```

Running the server and then the client gives:

![](https://i.imgur.com/4TYQx9n.png)

![](https://i.imgur.com/54UKJwU.png)

So we need to send some sort of boolean response.
We can't send an actual boolean, and sending 0x0, 0x1, or any other integer doesn't work.

However, from the `strings` mess above, we can see a `True` in there. So, we try to send a string, `"True"`:

![](https://i.imgur.com/RjmkdXd.png)

![](https://i.imgur.com/Zs2QNv9.png)

!! Nice!

We can just print the flag that the client sent with
`print c.recv(4096)`.

Final [server script](server.py):
```python
import socket, struct

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print "ok"

port = 1228
s.bind(("", port))

print "bound to 1228"

s.listen(5)

print "listening"

while True:
	c, addr = s.accept()
	print "conn from ", addr

	c.sendall("\n\n" + struct.pack(">I", 1234) + struct.pack(">I", 1234) + "\n\n\n") # send two big endian unsigned ints

	data = c.recv(4096) # receive response
	print struct.unpack(">I", data) # view response
    
	c.sendall("True") # send "boolean" value
	print c.recv(4096) # receive flag
	c.close()
    
s.shutdown()
```

Flag: `flag{sixty6}`

All credit goes to MAGIC for their challenge. This is just a writeup.
