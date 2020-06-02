#!/usr/bin/env python3
"""
Author:Igwaneza Bruce
Email:knowbeeinc@gmail.com
"""


from operator import itemgetter
import click
import requests
import re
import os
import time
import sys
from urllib.request import urlopen
import math
my_videos = []
sorted_videos = []


def downloader(link, size, filename):
    print("now downloading", filename)
    with open(filename, 'wb') as f:
        try:

            response = requests.get(link, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                print("invalid video id")
                return
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(
                        chunk_size=max(int(total / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50 * downloaded / total)
                    sys.stdout.write('\r[{}{}]'.format('o' * done,
                                                    '.' * (50 - done)))
                    sys.stdout.flush()
        except:
            print("network error...try again")
    sys.stdout.write('\n')
    os.remove("data.txt")
    print("download finished!" + "\n")


def download(resolution, filename):
    with open("data.txt") as f:
        for line in f:
            if (".bin" in line):
                link = line.split('"url":')[1].split('"')[1].split('"')[0]
                site = urlopen(link)
                meta = site.info()
                my_videos.append({
                    "url":
                    link,
                    "video_size":
                    math.ceil(int(meta["Content-Length"]) / float(1 << 20))
                })
        sorted_videos = sorted(my_videos,
                               key=itemgetter('video_size'),
                               reverse=True)
        if ("1080" in resolution):
            return downloader(sorted_videos[0]["url"],
                              sorted_videos[0]["video_size"],
                              filename + ".mp4")
        elif ("720" in resolution):
            return downloader(sorted_videos[1]["url"],
                              sorted_videos[1]["video_size"],
                              filename + ".mp4")
        elif ("480" in resolution):
            return downloader(sorted_videos[2]["url"],
                              sorted_videos[2]["video_size"],
                              filename + ".mp4")
        else:
            return downloader(sorted_videos[0]["url"],
                              sorted_videos[0]["video_size"],
                              filename + ".mp4")


def getVideos(id, resolution, filename):
    print("connecting to the servers..", "\n")
    try:
        page = requests.get("http://fast.wistia.net/embed/iframe/" + id).text
        content = []
        findstr = r'W\.iframeInit\({"assets":(\[.*\])'
        assets = re.search(findstr, page)

        if (assets):
            content = assets.group(1)
            with open('data.txt', "w") as outfile:
                outfile.write(content.replace(",", "\n").split("]")[0] + "]")
        download(resolution, filename)
    except:
        print("network error..try again")


@click.command()
@click.option('--id', '-i', help='wistia video id')
@click.option('-r',
              '--resolution',
              default='1080p',
              help='video resolution eg:720p')
@click.option('-n', '--filename', default='video', help='video name')
def wisty(id, resolution, filename):
    """
    Wistia video downloader command line tool\n
    example: wisty -i f5rf5rfr -r 1080p -n myvideo
    """
    if(len(sys.argv) == 1):
        print("missing required arguments: run wisty --help")
        sys.exit(0)
    getVideos(id, resolution, filename)


if __name__ == '__main__':

    wisty()
