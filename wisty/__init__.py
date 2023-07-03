#!/usr/bin/env python3
"""
Author:Igwaneza Bruce
Email:knowbeeinc@gmail.com
"""
import json
import os
import re
import sys
import click
import requests
from tqdm import tqdm


def download_video(link, filename):
    click.echo(click.style(filename, fg="green"))
    with open(filename, "wb") as file:
        try:
            response = requests.get(link, stream=True)
            download_size = response.headers.get("content-length")

            if download_size is None:
                download_size = len(response.raw.read())
                if download_size is None:
                    print("Network is too slow. Please try again later.")
                return
            else:
                pbar = tqdm(
                    total=int(download_size),
                    initial=0,
                    unit="B",
                    unit_scale=True,
                    position=0,
                    leave=True,
                )
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        pbar.set_description("Progress")
                        pbar.update(1024)
                pbar.close()
        except:
            click.echo(
                click.style("Network is too slow. Please try again later.", fg="red")
            )
    sys.stdout.write("\n")
    click.echo(click.style("Download complete!", fg="green"))


def parse_resolution(metadata, resolution, filename):
    try:
        with open(metadata, "r") as file:
            res = json.load(file)

            resolution_mapping = {
                "1080p": 1080,
                "720p": 720,
                "540p": 540,
                "480p": 480,
                "360p": 360,
            }

            selected_resolution = resolution_mapping.get(resolution, 1080)
            video_url = [x["url"] for x in res if x["height"] == selected_resolution][0]
            download_video(video_url, filename + ".mp4")
    except Exception as e:
        print(e)
        sys.exit(0)


def fetch_resolutions(id, resolution, filename):
    print("Connecting...\n")
    import json

    try:
        page = requests.get("http://fast.wistia.net/embed/iframe/" + id).text
        content = []
        regex = r'"assets":(\[.*?\])'
        match = re.search(regex, page)
        if match:
            content = json.loads(match.group(1))
            with open("extract.json", "w") as outfile:
                json.dump(content, outfile)
        parse_resolution("extract.json", resolution, filename)
    except Exception as e:
        print(e)
        sys.exit(0)


@click.command()
@click.option("--id", "-i", help="Wistia video id")
@click.option(
    "-r", "--resolution", default="1080p", help="Video resolution (e.g., 720p)"
)
@click.option("-n", "--name", default="video", help="Video name")
def main(id, resolution, name):
    """
    Wistia video downloader command line tool\n
    Example: wisty -i f5rf5rfr -r 1080p -n myvideo
    """
    if len(sys.argv) == 1:
        click.echo(
            click.style(
                "Missing required arguments. Run 'wisty --help' for help.", fg="red"
            )
        )
        sys.exit(0)
    fetch_resolutions(id, resolution, name)
    if os.path.exists("extract.json"):
        os.remove("extract.json")


if __name__ == "__main__":
    main()
