# wisty

[![Downloads](https://pepy.tech/badge/wisty)](https://pepy.tech/project/wisty)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)

A fast minimal command line tool to download videos hosted on wistia with video id.

## Preview

<p>
    <img src="https://raw.githubusercontent.com/knowbee/hosting/master/assets/wisty.png" width="auto" height="auto"/>
</p>

## How to get a video id ?

You right click on a video and select "Copy link and Thumbnail" paste it in a text file reader and find wvideo grab its value and voila!...That is the video id.

## Installation

    $ pip --no-cache-dir install wisty

Usage

```cli

    $ wisty --help
```

## Example

```cli

   wisty -i ffff5f5 -r 1080p -n "best video"

```

## Author

Igwaneza Bruce
