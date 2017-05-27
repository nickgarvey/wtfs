# WTFS #
A silly filesystem that should leave you saying "WTF?"

It generates a bunch of random filenames from a word list, with contents being spam messages. The filenames and contents change over time.

* Filenames:  https://packages.debian.org/sid/text/wamerican-small
* Contents: http://packages.ubuntu.com/trusty/fortunes-spam

## Usage ##

```
$ python wtfs.py
usage: wtfs.py mountpoint
$ python wtfs.py /mnt/wtfs
$ ls /mnt/wtfs
agony  biographical  biped  caressed  clasps  converters nutted  outclassing  pretentiously thanks  twitches
$ cat /mnt/wtfs/biped
Do not visit this illegal websites!
```

## Setup ##
Ubuntu 16.04:
```
git clone https://github.com/nickgarvey/wtfs.git wtfs
pip install fusepy
```


