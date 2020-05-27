# Corrupted-Project
Forensics, 90

>  Written by lighthouse64
>  Your friend was trying to send you the stuff that he did for your group project, but the data mysteriously got corrupted.
>  
>  He said his computer got infected before he was able to send it. Regardless of what happened, you need to fix it or you won't be able to complete the project. 

We are given some sort of file. The presence of a filename (`project-files.zip`) indicates it could be a zip file, and the fact the the first two bytes are `.K` confirms that it is likely a corrupted zip file (those two bytes should be `PK`). At byte 0x4b, we see a bzip2 stream header, `BZ`. We don't really need the zip file metadata, so we will deal with bzip2 directly. Deleting all bytes before `BZ` and looking at [pyflate](https://github.com/pfalcon/pyflate/blob/master/pyflate.py) shows that there are a few messed up constants. Namely, `e` should be `h` and the first block's `blocktype` must be changed to 0x314159265359. Running `pyflate.py` on the modified file gives a new zip file with 3 PNGs:

```
[kmh@kmh corrupted]$ python2 pyflate.py bz > /dev/null
[kmh@kmh corrupted]$ file out
out: Zip archive data, at least v2.0 to extract
[kmh@kmh corrupted]$ unzip out
Archive:  out
   creating: project-files/
  inflating: project-files/project-notes-1.png  
  inflating: project-files/project-notes-0.png  
  inflating: project-files/project-notes-2.png  
```

`project-notes-1.png` is corrupted. Opening it in a hex editor reveals that the first four bytes are `HELP`, not `89 50 4E 47`. Fixing these gives us an image with the flag: `tjctf{plz_dont_procrastinate}`.