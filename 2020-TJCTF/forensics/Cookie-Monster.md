# Cookie-Monster
Forensics, 80

>  Written by Alaska47
>  The Cookie Monster remotely raided my company's desktop server using my laptop, but instead of going after cookies, he went after my flags! I'm sure he must have left a cache of crumbs behind...here's what I was able to recover from my laptop.
>  alt link

From running strings and grepping for "Cookie: ", we can find some cookie, likely Flask: `Cookie: session=eyJsb2dnZWRfaW4iOnRydWV9.XsqeZQ.C7x84FROMlFfzg_2Wwaj0SDtNjY`.

Grepping for "http://" gives us an interesting site,
`http://super-secret-file-server.herokuapp.com`. We can set our cookie to the cookie from before to log in.

We are presented with a menu to download any file (spoiler: no LFI).

![](https://i.imgur.com/wnTQOr0.png)

Using volatility, we can dump the output of the consoles from the memory.

```
SCLs-Air:volatility-2.6.1 toaster$ python vol.py -f dump.raw --profile=Win2008R2SP1x64_23418 -f dump_patched.raw
Volatility Foundation Volatility Framework 2.6.1
**************************************************
ConsoleProcess: conhost.exe Pid: 1316
Console: 0xffd06200 CommandHistorySize: 50
HistoryBufferCount: 1 HistoryBufferMax: 4
OriginalTitle: %SystemRoot%\system32\cmd.exe
Title: Administrator: C:\Windows\system32\cmd.exe
AttachedProcess: cmd.exe Pid: 1772 Handle: 0x60
----
CommandHistory: 0x368ee0 Application: cmd.exe Flags: Allocated, Reset
CommandCount: 6 LastAdded: 5 LastDisplayed: 5
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x60
Cmd #0 at 0x368390: cd Documents
Cmd #1 at 0x34cce0: type credentials.txt
Cmd #2 at 0x36f690: cd ..
Cmd #3 at 0x3685d0: cd Downloads
Cmd #4 at 0x34cd20: del supersecretflag.txt
Cmd #5 at 0x3477c0: del ..\Documents\credentials.txt
----
Screen 0x34fbc0 X:80 Y:300
Dump:
Microsoft Windows [Version 6.1.7601]                                            
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.                 
                                                                                
C:\Users\Administrator>cd Documents                                             
                                                                                
C:\Users\Administrator\Documents>type credentials.txt                           
Super Secret File Server                                                        
username: admin                                                                 
password: s$FCH-ZUMt2+xny                                                       
C:\Users\Administrator\Documents>cd ..                                          
                                                                                
C:\Users\Administrator>cd Downloads                                             
                                                                                
C:\Users\Administrator\Downloads>del supersecretflag.txt                        
                                                                                
C:\Users\Administrator\Downloads>del ..\Documents\credentials.txt               
                                                                                
C:\Users\Administrator\Downloads>                                               
**************************************************
ConsoleProcess: conhost.exe Pid: 1620
Console: 0xffd06200 CommandHistorySize: 50
HistoryBufferCount: 1 HistoryBufferMax: 4
OriginalTitle: C:\Users\Administrator\Downloads\DumpIt.exe
Title: C:\Users\Administrator\Downloads\DumpIt.exe
AttachedProcess: DumpIt.exe Pid: 1264 Handle: 0x60
----
CommandHistory: 0x1cab40 Application: DumpIt.exe Flags: Allocated
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x60
----
Screen 0x1afc70 X:80 Y:300
Dump:
  DumpIt - v1.3.2.20110401 - One click memory memory dumper                     
  Copyright (c) 2007 - 2011, Matthieu Suiche <http://www.msuiche.net>           
  Copyright (c) 2010 - 2011, MoonSols <http://www.moonsols.com>                 
                                                                                
                                                                                
    Address space size:        1073676288 bytes (   1023 Mb)                    
    Free space size:          23336112128 bytes (  22255 Mb)                    
                                                                                
    * Destination = \??\C:\Users\Administrator\Downloads\WIN-BIHBE396O07-2020052
4-161946.raw                                                                    
                                                                                
    --> Are you sure you want to continue? [y/n] y                              
    + Processing...
```

Now we have the actual credentials to log in (`admin`:`s$FCH-ZUMt2+xny`), as well as a mention of a suspicious file called `supersecretflag.txt`. We try to download it from the site, and it works! We get part of the flag:
`Cookie Monster says: _4nd_th1s_1s_th3_re5t_0f_1he_f1Ag}`.

Now we get stuck for 5+ hours and bang our heads against Volatility files, until we re-read the description and notice the specific wording.

Basically, the description says someone used a laptop to remote onto a server. We have the laptop's memory. So, we should try to restore the RDP session.

We can quickly verify this with a quick pslist in volatility:

```
SCLs-Air:volatility-2.6.1 toaster$ python vol.py -f dump.raw --profile=Win2008R2SP1x64_23418 pslist
Volatility Foundation Volatility Framework 2.6.1

Offset(V)          Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
------------------ -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0xfffffa8000c99040 System                    4      0     76      475 ------      0 2020-05-24 18:52:36 UTC+0000                                 
0xfffffa8001026130 smss.exe                248      4      2       29 ------      0 2020-05-24 18:52:36 UTC+0000                                 
0xfffffa80017f32d0 csrss.exe               316    308      9      300      0      0 2020-05-24 18:52:37 UTC+0000                                 
0xfffffa80018123d0 wininit.exe             368    308      3       77      0      0 2020-05-24 18:52:38 UTC+0000                                 
0xfffffa8001813650 csrss.exe               376    360     10      299      1      0 2020-05-24 18:52:38 UTC+0000                                 
0xfffffa8001827b30 winlogon.exe            404    360      3       93      1      0 2020-05-24 18:52:38 UTC+0000                                 
0xfffffa800187cb30 services.exe            464    368      6      188      0      0 2020-05-24 18:52:38 UTC+0000                                 
0xfffffa8001893b30 lsass.exe               472    368      7      668      0      0 2020-05-24 18:52:38 UTC+0000                                 
0xfffffa8001898b30 lsm.exe                 480    368     10      159      0      0 2020-05-24 18:52:38 UTC+0000                                 
0xfffffa800198bb30 svchost.exe             576    464     10      341      0      0 2020-05-24 18:52:39 UTC+0000                                 
0xfffffa8001a29b30 VBoxService.ex          636    464     11      136      0      0 2020-05-24 18:52:39 UTC+0000                                 
0xfffffa80019d7b30 svchost.exe             704    464      7      225      0      0 2020-05-24 15:52:41 UTC+0000                                 
0xfffffa8001a34410 svchost.exe             760    464     13      292      0      0 2020-05-24 15:52:41 UTC+0000                                 
0xfffffa8001a52b30 svchost.exe             836    464     28      825      0      0 2020-05-24 15:52:41 UTC+0000                                 
0xfffffa8001a6d370 svchost.exe             888    464      8      212      0      0 2020-05-24 15:52:41 UTC+0000                                 
0xfffffa8001a7f300 svchost.exe             928    464      7      199      0      0 2020-05-24 15:52:41 UTC+0000                                 
0xfffffa8001a97370 svchost.exe            1000    464     17      501      0      0 2020-05-24 15:52:42 UTC+0000                                 
0xfffffa8000fd7b30 svchost.exe             320    464     16      298      0      0 2020-05-24 15:52:42 UTC+0000                                 
0xfffffa800193e060 spoolsv.exe            1040    464     12      257      0      0 2020-05-24 15:52:42 UTC+0000                                 
0xfffffa80019de060 svchost.exe            1100    464      3       46      0      0 2020-05-24 15:52:43 UTC+0000                                 
0xfffffa8001a08060 wlms.exe               1140    464      4       44      0      0 2020-05-24 15:52:43 UTC+0000                                 
0xfffffa8001977060 sppsvc.exe             1324    464      4      143      0      0 2020-05-24 15:52:43 UTC+0000                                 
0xfffffa8001b79b30 taskhost.exe           1560    464      5      115      1      0 2020-05-24 15:52:52 UTC+0000                                 
0xfffffa8001b93b30 dwm.exe                1624    928      3       67      1      0 2020-05-24 15:52:53 UTC+0000                                 
0xfffffa8001ba7b30 explorer.exe           1660   1616     26      779      1      0 2020-05-24 15:52:53 UTC+0000                                 
0xfffffa8001c10b30 VBoxTray.exe           1960   1660     13      139      1      0 2020-05-24 15:52:54 UTC+0000                                 
0xfffffa8001002710 GoogleCrashHan          856   1760      5       99      0      1 2020-05-24 15:52:55 UTC+0000                                 
0xfffffa8001c41950 GoogleCrashHan         1052   1760      5       91      0      0 2020-05-24 15:52:55 UTC+0000                                 
0xfffffa800124ab30 svchost.exe             812    464      5       71      0      0 2020-05-24 15:54:43 UTC+0000                                 
0xfffffa80012786f0 msdtc.exe              1292    464     12      144      0      0 2020-05-24 15:54:44 UTC+0000                                 
0xfffffa80012b6060 mstsc.exe              1412   1660     14      671      1      0 2020-05-24 16:00:07 UTC+0000                                 
0xfffffa8001ca5690 cmd.exe                1772   1660      1       19      1      0 2020-05-24 16:16:58 UTC+0000                                 
0xfffffa80012c2060 conhost.exe            1316    376      2       38      1      0 2020-05-24 16:16:58 UTC+0000                                 
0xfffffa8001c7a060 chrome.exe              292   1660     28      763      1      1 2020-05-24 16:17:37 UTC+0000                                 
0xfffffa8000cd2060 chrome.exe             1876    292      8       78      1      1 2020-05-24 16:17:37 UTC+0000                                 
0xfffffa80012d0780 chrome.exe              960    292     15      351      1      1 2020-05-24 16:17:38 UTC+0000                                 
0xfffffa80012b8060 chrome.exe             2256    292      8      169      1      1 2020-05-24 16:17:40 UTC+0000                                 
0xfffffa8000cc4060 chrome.exe             2728    292     13      204      1      1 2020-05-24 16:18:16 UTC+0000                                 
0xfffffa8001cf0a30 DumpIt.exe             1264   1660      1       27      1      1 2020-05-24 16:19:46 UTC+0000                                 
0xfffffa8001ee5b30 conhost.exe            1620    376      2       33      1      0 2020-05-24 16:19:46 UTC+0000
```

Yep, there is a `mstsc.exe` running.

After some quick googling, we discover the primary location that RDP caches are stored, as well as how to get it, from [this guide](https://cyberforensicator.com/2018/02/12/rdp-cache-forensics/).

We can look for the cache with volatility, grepping for part of the file path:
```
SCLs-Air:volatility-2.6.1 toaster$ python vol.py -f dump.raw --profile=Win2008R2SP1x64_23418 filescan | grep -i "Terminal Server Client"
Volatility Foundation Volatility Framework 2.6.1
0x0000000005b32f20     25      1 RW-r-- \Device\HarddiskVolume2\Users\Administrator\AppData\Local\Microsoft\Terminal Server Client\Cache\bcache22.bmc
0x000000003ed5af20     25      1 RW-r-- \Device\HarddiskVolume2\Users\Administrator\AppData\Local\Microsoft\Terminal Server Client\Cache\bcache22.bmc
0x000000003ff7df20     23      1 RW-r-- \Device\HarddiskVolume2\Users\Administrator\AppData\Local\Microsoft\Terminal Server Client\Cache\bcache22.bmc
```

We can dump one of these files with their offsets:

```
mkdir dumpedfiles && python vol.py -f dump.raw  --profile=Win2008R2SP1x64_23418 dumpfiles -Q 0x000000003ff7df20  -D dumpedfiles -S summary.txt
```

This will dump the `bcache22.bmc` file at `0x000000003ff7df20` into the folder `dumpedfiles`.

In order to restore the desktop state, we can use [bmc-tools](https://github.com/ANSSI-FR/bmc-tools):

```
cd bmc-tools; mkdir out; python bmc-tools.py -s ../dumpedfiles/file.None.0xfffffa8001aa5f10.dat -d out/
```

This will create bitmap "tiles" of the remote desktop state, which we can open in a Windows OS.

At this point my Mac could not open .bmp images ~~and I was too tired to puzzle-piece the flag together on my desktop~~, so I yeeted them to Aplet who put the flag together and submitted it.

Flag: `tjctf{c00k1e_m0n5t3r_w4s_h3r3_4nd_y0u_w1ll_n3v3r_f1nd_m333}`