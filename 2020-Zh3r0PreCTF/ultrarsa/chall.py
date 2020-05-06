from base64 import b64encode as b64e
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from flag import flag, hint

pt=bytes_to_long(flag)
ht=bytes_to_long(hint)
p=getPrime(2048)
q=getPrime(2048)
r=getPrime(2048)
s=getPrime(2048)
x=getPrime(1024)
y=getPrime(1024)
e=65537
if x>y:
	key=x-y
else:
	key=y-x

key=b64e(str(key))

n=x*y
n1=p*q
n2=r*s
n3=n1*n2

if p>q:
	a=p-q
else:
	a=q-p
b=r+q
c=p+r

enh=pow(ht,e,n)
ct=pow(pt,e,n3)

opt="N : "+str(n)+"\ne : "+str(e)+"\nenc(Hint) : "+str(enh)+"\n\nN1 : "+str(n1)+"\nN2 : "+str(n2)+"\nN3 : "+str(n3)+"\nCipher Text : "+str(ct)+"\n\n\nkey : "+str(key)+"\n"
pvt="a = "+str(a)+"\nb = "+str(b)+"\nc = "+str(c)+"\n"
test="p="+str(p)+"\nq="+str(q)+"\nr="+str(r)+"\ns="+str(s)+"\nx="+str(x)+"\ny="+str(y)+"\n"
#print(opt,pvt)


ob=open("out.txt","w")
ob.write(opt)
ob.close()
ob=open("hint.txt","w")
ob.write(pvt)
ob.close()
ob=open("test.txt","w")
ob.write(test)
ob.close()
