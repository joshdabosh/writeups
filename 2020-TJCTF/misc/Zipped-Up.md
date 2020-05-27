# Zipped-Up
Misc, 70

>  Written by agcdragon
>  My friend changed the password of his Minecraft account that I was using so that I would stop being so addicted. Now he wants me to work for the password and sent me this zip file. I tried unzipping the folder, but it just led to another zipped file. Can you find me the password so I can play Minecraft again? 

This challenge sucked.

The following script needs the zip files to be extracted to a parent folder named `zips`. It just keeps unzipping until it finds a flag file that isn't `tjctf{n0t_th3_fl4g}`.

```python
from os import listdir, rmdir
import tarfile
from zipfile import ZipFile
import shutil
start = 1
for i in range(start,1000):
	d = listdir(f"zips/{i-1}")
	if i!=start:
		with open(f"zips/{i-1}/{i-1}.txt") as f:
			a = f.read()
			if a.strip() != "tjctf{n0t_th3_fl4g}":
				break
	for x in d:
		if ".txt" not in x:
			d = x
			break
	if ".bz2" in d:
		t = tarfile.open(f"zips/{i-1}/{d}",mode='r:bz2')
		t.extractall(path="zips/")
	elif ".gz" in d:
		t = tarfile.open(f"zips/{i-1}/{d}",mode='r:gz')
		t.extractall(path="zips/")
	elif ".kz3" in d:
		t = ZipFile(f"zips/{i-1}/{d}")
		t.extractall(path="zips/")
	else:
		break
	if i!=start:
		shutil.rmtree(f"zips/{i-2}")
```
After running this script, we get the flag in 829.txt.

Flag: `tjctf{p3sky_z1p_f1L35}`