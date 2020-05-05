# DawgCTF 2020

b1c placed 3rd.

We mostly got stuck on a certain guess challenge which was annoying.

Don't feel like doing detailed writeups but here's one for a decent challenge, `Benford's Law Firm, LLC`.

## Benford's Law Firm, LLC
We are given a zip of a lot csv files with flaglike filenames, and we are told one csv file contains fraudulent data. Also, we only have 25 submission attempts on the CTFd site so we can't brute force.

Googling [Benford's law](https://en.wikipedia.org/wiki/Benford%27s_law) gives us a pretty good idea of what to do: check leading digits in the finance reports.

We can chi square test it against a sample distribution.

The rest is just implementation.

```python
import os
import re

os.chdir("Benford_s_Law_Firm_LLC")

files = os.listdir()

# chi squared test from some site
def chisq_stat(O, E):
    return sum( (o - e)**2/e for (o, e) in zip(O, E) )

res = []

for fname in files:
    f = open(fname).read().strip()
    
    # find all finance data in a csv
    nums = re.findall("\$\d*\.?\d*", f)
    
    t = [0]*10
    
    for n in nums:
        # count digits
        t[int(n.strip("$")[0])] += 1
    
    # generate sample distribution
    follow = [ len(t)*log10(1 + 1/n) for n in range(1, 10) ]
    
    # chi square test given vs sample, save data to compare later
    res.append([chisq_stat(t[1:], follow), fname])

# sort data based on chi square test score
res.sort(key = lambda x: x[0])

# print the worst scoring filename
print(res[-1][1])
```

Flag: `DawgCTF{L3g@lly_D1s7ribu73d_St@t1st1c5_641}`
