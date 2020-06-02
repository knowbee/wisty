wisty
=======================

A fast minimal command line tool to download videos hosted on wistia with video id.


How to get a video id ?
------------------------

You right click on a video and select "Copy link and Thumbnail" paste it in a text file reader and find wvideo grab its value and voila!...That is the video id.

Installation
------------

    $ pip3 install -r requirements.txt

Usage
----------- 

    $ chmod +x ./wisty.py
    $ wisty --help

Download a video
-----------------
```cli

   $ wisty -i <Video id> -r <Resolution> -n <Video name>

```

Example
--------
```cli

   wisty -i ffff5f5 -r 1080p -n "best video"

```

Author
------
Igwaneza Bruce