from operator import itemgetter
import click
import requests
import re
import json
import os
import time
import sys
from urllib.request import urlopen
import math
my_videos = []
sorted_videos = []


def download(link, size, filename):
    print("now downloading", filename)
    with open(filename, 'wb') as f:
        response = requests.get(link, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format(
                    'o' * done, '.' * (50-done)))
                sys.stdout.flush()
    sys.stdout.write('\n')
    os.remove("data.json")
    os.remove("data.txt")
    print("download finished!" + "\n")


def VideoFormatter(format, filename):
    with open("data.json") as f:
        for line in f:
            if(".bin" in line):
                link = line.split('"url": ')[1].split(
                    ",")[0].split('"')[1].split('"')[0]
                site = urlopen(link)
                meta = site.info()
                my_videos.append(
                    {"url": link, "video_size": math.ceil(int(meta["Content-Length"]) / float(1 << 20))})
        sorted_videos = sorted(
            my_videos, key=itemgetter('video_size'), reverse=True)
        if("1080" in format):
            return download(sorted_videos[0]["url"],
                            sorted_videos[0]["video_size"], filename + ".mp4")
        elif("720" in format):
            return download(sorted_videos[1]["url"],
                            sorted_videos[1]["video_size"], filename + ".mp4")
        elif("480" in format):
            return download(sorted_videos[2]["url"],
                            sorted_videos[2]["video_size"], filename + ".mp4")
        else:
            return download(sorted_videos[0]["url"],
                            sorted_videos[0]["video_size"], filename + ".mp4")


def getVideos(id, format, filename):
    print("connecting to servers..", "\n")
    page = requests.get("http://fast.wistia.net/embed/iframe/" + id).text
    content = []
    findstr = r'W\.iframeInit\({"assets":(\[.*\])'
    assets = re.search(findstr, page)

    if(assets):
        content = assets.group(1)
        with open('data.txt', "w") as outfile:
            outfile.write(content.split("],")[0] + "]")
    VideoFormatter(format, filename)


@click.command()
@click.option('--id',
              '-i',
              help='wistia video id')
@click.option('-f', '--format', default='1080p', help='video quality eg:720p')
@click.option('-n', '--filename', default='video', help='video name')
def main(id, format, filename):
    """
    Wistia video downloader command line tool\n
    example: python run.py -i f5rf5rfr -f 1080p -n myvideo
    """
    getVideos(id, format, filename)


if __name__ == '__main__':
    main()
