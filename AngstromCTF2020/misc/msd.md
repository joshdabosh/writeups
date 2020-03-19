# msd
Misc, 140

> You thought Angstrom would have a stereotypical LSB challenge... You were wrong! To spice it up, we're now using the Most Significant Digit. Can you still power through it?

> Here's the encoded image, and here's the original image, for the... well, you'll see.

> Linked: public.py, output.png, breathe.jpg


From the description, we know that we have to extract the most significant digit, similar to how LSB (least bit steganography) works.

After analyzing the code given, we discover that the `encode` function has two edge cases:
1. When the digit to encode is 0, the most significant digit is the one over. `0 -> 123` gives `23`
2. When the encoded output is > 255, PIL automatically caps at 255, meaning data is lost. `955` gets capped to `255` after `im.putpixel`.

To resolve edge case 1, we can simply compare the length of the original pixel with the encoded pixel. If they are different, then we know the digit encoded was a 0.

To resolve edge case 2, we don't. We observe that the flag is repeated many times, and can reason that the full flag will be in there somewhere ;).

```python
from PIL import Image

im = Image.open("output.png")
im2 = Image.open("breathe.jpg")

width, height = im.size

def decode(i, compare):
    """
    Pads the encoded value with 0s from the left,
    based on the length of the original value
    Think about why this works!
    """
    i = list(str(i).zfill(len(str(compare))))
    return i[0]


pixels = im.load()
pixels2 = im2.load()

s = ""
binary = []

for j in range(height):
    for i in range(width):
        data = []
        
        for a, compare in zip(im.getpixel((i,j)), im2.getpixel((i, j))):
            data.append(decode(a, compare))    # get MSD of the pixel

        s += ''.join(data)


s = list(s)
data = []

while len(s) > 0:
    t = ""
    curr = s.pop(0)

    if curr != "1":
        # handle the 1xx ascii codes
        t += curr + s.pop(0)

    else:
        # handle the xx ascii codes
        t += curr + s.pop(0) + s.pop(0)

    data.append(t)
    
data = ''.join([chr(int(i)) for i in data])    # turn all the results into ASCII


import re

r1 = re.findall(r"actf{.*?}", data)    # look for the flag using regex

min = min(map(len, r1))    # get shortest result

for i in r1:
	if len(i) == min:
		print(i)    # print shortest result
```