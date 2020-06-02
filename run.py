from operator import itemgetter
import click
import argparse
import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time
from urllib.request import urlopen
import math
my_videos = []


def DownloadVideo(format):
    with open("data.json") as f:
        for line in f:
            if(".bin" in line):
                link = line.split('"url": ')[1].split(
                    ",")[0].split('"')[1].split('"')[0]
                site = urlopen(link)
                meta = site.info()
                my_videos.append(
                    {"url": link, "video_size": math.ceil(int(meta["Content-Length"]) / float(1 << 20))})
        sorted(my_videos, key=itemgetter('video_size'), reverse=True)


def getVideos(id, format):
    page = requests.get("http://fast.wistia.net/embed/iframe/" + id).text
    content = []
    findstr = r'W\.iframeInit\({"assets":(\[.*\])'
    assets = re.search(findstr, page)

    if(assets):
        content = assets.group(1)
        with open('data.txt', "w") as outfile:
            outfile.write(content.split("],")[0] + "]")
            print("got data from wistia")
    DownloadVideo(format)


@ click.command()
@ click.option('--id',
               '-i',
               help='wistia video id')
@click.option('-f', '--format', default='1080p', help='video quality eg:720p')
def main(id, format):
    """
    wistia video downloader command line tool\n
    example: python run.py -i f5rf5rfr
    """
    # getVideos(id, format)
    DownloadVideo(format)


if __name__ == '__main__':
    main()
