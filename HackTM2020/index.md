# HackTM 2020
I played with DiceGang.
We placed 12th and ended up qualifying for the final round in Romania.

## OSINT

### OLD Times
A guy named `Vlaicu Petronel` is mentioned in the problem statement. We perform a google search for this name and end up at his twitter, [@PetronelVlaicu](https://twitter.com/PetronelVlaicu).

We go on a trip down the rabbit hole, stalking a mysterious man named `VenaticalManx58` who is one of Vlaicu's followers on Twitter. He appears very suspicious. We waste lots of time on him.

We look back to the challenge for any other hints. The title looks interesting: `OLD Times`. We figure this may be a reference to the Wayback Machine: we see 9 captures logged on 12/6 and 2 the day after; none at any other time. This isn't normal, so we figured it must be planned by the organizers.

Indeed, the captures reveal Petronel's deleted tweets. At one point he tweeted and deleted the following string: `1XhgPI0jpK8TjSMmSQ0z5Ozcu7EIIWhlXYQECJ7hFa20`. Later on he tweeted and then deleted `I love Google G Suite services!`.

GSuite services are products like Google Docs, Slides, etc., so we figure that the `1Xhg`... string must be part of a Google Docs/etc URL since it doesn't appear to decode to anything useful.

Google's format for Docs/Slides `https://docs.google.com/document/{service name}/{identifier}/edit`.
We try plugging the service name for Google Docs (d) and identifier in, and it gives us [this document](https://docs.google.com/document/d/1XhgPI0jpK8TjSMmSQ0z5Ozcu7EIIWhlXYQECJ7hFa20/edit), containing us information about a suspicious guy named `Iovescu Marian`.

In small text at the top, the report states that Iovescu goes by the name `E4gl3OfFr3ed0m` online.

The report details that he published his work on `a free and open platform`, but later deleted it. This seems to be hinting towards version control platforms like GitHub. Thus, we check GitHub for `E4gl3OfFr3ed0m`'s account, and we find [one](https://github.com/E4gl3OfFr3ed0m) account. His status shows the Romanian flag along with the text, `Beliver`, confirming that he is probably Iovescu.

Iovescu only has 1 repository, named `resistance`. When we inspect it, we find `README.md` and `heart.jpg`. Inspecting the commit history reveals that `E4gl3OfFr3ed0m` had a file named `spread_locations.php`. The source will be useful later. We probe the files deeper. Upon inspection, `README.md` actually has a commented link to [a site](http://138.68.67.161:55555/), which we only found through viewing the raw markdown file.

This site returns a 403 error upon visiting it. However, we can use information we previously gathered and try to visit `/spread_locations.php`. Voila, it doesn't return a 403!

When we look at the `spread_locations.php` source from commit `7f284eee2c71cf993f8e217c48cbd47cf15ba923`, we see that it will return a location corresponding to a number that the user requests, if the number is between [0, 128]. Also there is a pretty glaringly obvious XSS attack on this but oh well, it won't matter in the long run when we track down who's trying to overthrow the communist government of Romania.

We can use the following script to extract all locations:
```python
import requests

for i in range(129):
	p = requests.get("http://138.68.67.161:55555/spread_locations.php?region="+str(i))
	print(p.text.split(" ", 1)[1])
```

This will print out a list of coordinates. We assume they are longitude and latitude pairs. However, when we plug a sample coordinate in, we only see some Middle-Eastern men looking at a dysfunctional magic carpet. No luck.

Then, we attempt to plot them. This can be done by saving location markers in Google Maps, or even just graphing the points in Desmos.

The resulting plot will spell out the flag.
