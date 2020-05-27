# Gym
Rev, 20

>  Written by agcdragon
>  Aneesh wants to acquire a summer bod for beach week, but time is running out. Can you help him create a plan to attain his goal?
>  nc p1.tjctf.org 8008 

Basically, you had to drop 31 pounds in 7 days, but there were only 4 actions you could do (I might've mixed up the names):
- Pushups to drop 1 pound
- Sleep to drop 2 pounds
- Run to drop 3 pounds
- Eat healthy to drop 4 pounds

So, the most you could do is drop 28 pounds. However, there's a bug where running doesn't exit to program and proceeds to continue on to sleeping, so you can drop 5 pounds in a day. So, the solution is to run 6 times then pushup.

Flag: `tjctf{w3iGht_l055_i5_d1ff1CuLt}`