import json
import sys

# with open('/data/home/faw513/zanardo-replication/processing/download_links.json') as srtm:
with open('download_links.json') as srtm:
    links = json.load(srtm)

for url in links[sys.argv[1]]:
    print(url)
