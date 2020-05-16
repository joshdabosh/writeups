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

	c.sendall("\n\n" + struct.pack(">I", 1234) + struct.pack(">I", 1234) + "\n\n\n")

	data = c.recv(4096)
	print(struct.unpack(">I", data))
	data = struct.unpack(">I", data)
	c.sendall("True")
	print(c.recv(4096))
	c.close()
s.shutdown()
