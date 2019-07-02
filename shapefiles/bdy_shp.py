from shapely.geometry import mapping, Polygon, Point, MultiPolygon, MultiPoint
import fiona
from glob import glob
import os
import csv


points = []
point_ids = []

polys = []

with open('../supplement/tabula-jgrf_20029_fs1.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for row in reader:
        point_ids.append(row[1])
        points.append(Point(float(row[3]), float(row[2])))


files = glob('../mopex-boundary-files/*.BDY')

for f in files:
    basin_id = os.path.splitext(os.path.basename(f))[0]
    data = []
    with open(f) as bdy:
        bdy.readline()
        lines = bdy.readlines()

    for row in lines:
        s = row.strip().split()
        tmp = (float(s[0]), float(s[1]))

        data.append(tmp)

    polys.append(Polygon(data))



    # for i, point in enumerate(points):
    #     if poly.contains(point):
    #         print(basin_id, point_ids[i])

mp = MultiPoint(points)

# Define a polygon feature geometry with one attribute
schema = {
    'geometry': 'MultiPoint',
    'properties': {'id': 'int'},
}

# Write a new Shapefile
with fiona.open('pts.shp', 'w', 'ESRI Shapefile', schema) as c:
    c.write({
        'geometry': mapping(mp),
        'properties': {'id': 1},
    })
