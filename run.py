import requests
import re
from bs4 import BeautifulSoup
import json
import os
import time

page = requests.get("http://fast.wistia.net/embed/iframe/x2lne5zhq4").text
content = []
findstr = r'W\.iframeInit\({"assets":(\[.*\])'
assets = re.search(findstr, page)

if(assets):
    content = assets.group(1)
    with open('data.txt', "w") as outfile:
        outfile.write(content.split("],")[0] + "]")
        print("got data from wista")


print("waiting 1 seconds to format data")
time.sleep(1)
os.rename("data.txt", "data.json")
print("data converted!")
