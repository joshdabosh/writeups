# Chord-Encoder
Rev, 40

>  Written by boomo
>  I tried creating my own chords, but my encoded sheet music is a little hard to read. Please play me my song! chord_encoder.py 
Here's the source:
```python
f = open('song.txt').read()

l = {'1':'A', '2':'B', '3':'C', '4':'D', '5':'E', '6':'F', '7':'G'}
chords = {}
for i in open('chords.txt').readlines():
	c, n = i.strip().split()
	chords[c] = n

s = ''
for i in f:
	c1, c2 = hex(ord(i))[2:]
	if c1 in l:
		c1 = l[c1]
	if c2 in l:
		c2 = l[c2]
	s += chords[c1] + chords[c2]
open('notes.txt', 'w').write(s)
```
and here are the chords:
```
A 0112
B 2110
C 1012
D 020
E 0200
F 1121
G 001
a 0122
b 2100
c 1002
d 010
e 0100
f 1011
g 000
```
and here are the notes:
```
1121112111211002112101121121001001210000101221121011200102000110120200101100100111211011001020020010111012011202001011112110121121011211211002112110020200101111210112020010111121010112102001121100211211011020020001010
```
Basically, we want to convert a giant string of notes back into the chords, but there's an issue. `D` is `020` and `E` is `0200`, which means there's no easy way to do this. So, we'll have to do some dynamic programming. Here's my haskell solve script (don't murder me please):
```haskell
import qualified Data.Map as M
import Data.List
import Control.Applicative

arrToTuple :: [a] -> (a, a)
arrToTuple (x:y:_) = (x, y)

processChords :: String -> M.Map String String
processChords = M.fromList . map (arrToTuple . reverse . words) . filter (not . null) . lines

trim :: String -> String
trim = reverse . f . reverse . f
    where f ""     = ""
          f (x:xs) = if elem x " \t\n\r" then f xs else x:f xs

interpret :: M.Map String String -> String -> Maybe String
interpret m "" = Just ""
interpret m s  = try 3 <|> try 4
    where try n = liftA2 (++) (M.lookup (take n s) m) (interpret m $ drop n s)

swap :: Char -> Char
swap x = if elem x ['A'..'G'] then head . show $ fromEnum x - fromEnum '@' else x

hexVal :: Char -> Maybe Int
hexVal c = elemIndex c $ ['0'..'9'] ++ ['a'..'f']

fromHex :: String -> Maybe Int
fromHex "" = Just 0
fromHex s  = hexVal (last s) >>= \n -> (\v -> n + 16 * v) <$> fromHex (init s)

hexToAscii :: String -> Maybe String
hexToAscii "" = Just ""
hexToAscii s  = liftA2 (:) (toEnum <$> fromHex (take 2 s)) (hexToAscii $ drop 2 s)

main = do
    notes <- trim <$> readFile "notes.txt"
    chords <- processChords <$> readFile "chords.txt"
    let (Just interpreted) = interpret chords notes
    let (Just flag) = hexToAscii . map swap $ interpreted
    putStrLn flag

```

Flag: `flag{zats_wot_1_call_a_meloD}`