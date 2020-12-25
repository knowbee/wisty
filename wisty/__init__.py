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
from tqdm import tqdm

all_videos = []
sorted_videos = []


def download(link, filename):
    click.echo(click.style(
        filename, fg="green"))
    with open(filename, 'wb') as f:
        try:

            response = requests.get(link, stream=True)
            download_size = response.headers.get('content-length')

            if download_size is None:
                download_size = len(response.raw.read())
                if download_size is None:
                    print("network too slow, try again later")
                return
            else:
                pbar = tqdm(
                    total=int(download_size),
                    initial=0,
                    unit='B',
                    unit_scale=True,
                    position=0,
                    leave=True)
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.set_description("progress")
                        pbar.update(1024)
                pbar.close()
        except:
            click.echo(click.style(
                "network too slow, try again later", fg="red"))
    sys.stdout.write('\n')
    os.remove("data.txt")
    click.echo(click.style(
        "finished !", fg="green"))
    sys.exit(0)


def parser(resolution, filename):
    try:
        with open("data.txt") as f:
            for line in f:
                if (".bin" in line):
                    link = line.split('"url":')[1].split('"')[1].split('"')[0]
                    site = urlopen(link)
                    meta = site.info()
                    all_videos.append({
                        "url":
                        link,
                        "video_size":
                        math.ceil(int(meta["Content-Length"]) / float(1 << 20))
                    })
            sorted_videos = sorted(all_videos,
                                   key=itemgetter('video_size'),
                                   reverse=True)
            if ("1080" in resolution):
                download(sorted_videos[0]["url"],
                         filename + ".mp4")
            elif ("720" in resolution):
                download(sorted_videos[1]["url"],
                         filename + ".mp4")
            elif ("540" in resolution):
                download(sorted_videos[2]["url"],
                         filename + ".mp4")
            elif ("480" in resolution):
                download(sorted_videos[3]["url"],
                         filename + ".mp4")
            elif ("360" in resolution):
                download(sorted_videos[4]["url"],
                         filename + ".mp4")
            else:
                download(sorted_videos[0]["url"],
                         filename + ".mp4")
    except:
        sys.exit(0)


def fetch_all_resolutions(id, resolution, filename):
    print("connecting..", "\n")
    try:
        page = requests.get("http://fast.wistia.net/embed/iframe/" + id).text
        content = []
        findstr = r'W\.iframeInit\({"assets":(\[.*\])'
        assets = re.search(findstr, page)

        if (assets):
            content = assets.group(1)
            with open('data.txt', "w") as outfile:
                outfile.write(content.replace(",", "\n").split("]")[0] + "]")
        parser(resolution, filename)
    except:
        sys.exit(0)


@click.command()
@click.option('--id', '-i', help='wistia video id')
@click.option('-r',
              '--resolution',
              default='1080p',
              help='video resolution eg:720p')
@click.option('-n', '--name', default='video', help='video name')
def main(id, resolution, name):
    """
    Wistia video downloader command line tool\n
    example: wisty -i f5rf5rfr -r 1080p -n myvideo
    """
    if(len(sys.argv) == 1):
        click.echo(click.style(
            "missing required arguments: run wisty --help", fg="red"))
        sys.exit(0)
    fetch_all_resolutions(id, resolution, name)


if __name__ == '__main__':

    main()
