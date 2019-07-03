import json
import re

def tryint(s):
    '''
    These three sorting functions are from https://nedbatchelder.com/blog/200712/human_sorting.html
    '''
    try:
        return int(s)
    except ValueError:
        return s

def alphanum_key(s):
    """
    Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """
    Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

with open('download_links.json') as srtm:
    links = json.load(srtm)

with open('bboxes.json') as bbox:
    bboxes = json.load(bbox)

lats = []
lngs = []

with open('../supplement/tabula-jgrf_20029_fs1.csv') as f:
    f.readline()
    data = f.readlines()

for d in data:
    spl = d.split(',')
    lats.append(spl[2].strip())
    lngs.append(spl[3].strip())

# make a list of the shape names in human sorted order
shape_names = []
for key, urls in links.items():
    shape_names.append(key)

sort_nicely(shape_names)


# Write the required params for each job into a file in the format:
# job_id shapefile_name(no extension) utm_zone north/south lat long
with open('array_params.txt', 'w') as f:
    for i, a in enumerate(shape_names, start=1):
        utm = bboxes[a]['utm_zone']

        f.write('{} {} {} {} {} {}\n'.format(str(i).zfill(4), a[:-4], utm[0],
                                          utm[1], lats[i-1], lngs[i-1]))
