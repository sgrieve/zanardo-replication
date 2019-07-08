from shapely.geometry import mapping, Point, MultiPoint
from shapely.ops import nearest_points
import fiona
from fiona.crs import from_epsg
from glob import glob
import csv
import sys

points = fiona.open('/data/home/faw513/zanardo-replication/shapefiles/pts_wgs84.shp')
# points = fiona.open('../shapefiles/pts_wgs84.shp')

index = int(sys.argv[1].split('_')[1])

point = Point(points[0]['geometry']['coordinates'][index])
buffered = point.buffer(0.05)

channel_pts = []
NI = []

filename = '/data/Geog-c2s2/zanardo/{}/full_network_{}.csv'.format(sys.argv[1], sys.argv[1])
print('built filename:', filename)
with open(filename) as csvfile:
# with open('full_network_buffer_{}.csv'.format(i)) as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        if float(row[3]) > 5:

            tmpPoint = Point(float(row[1]), float(row[0]))

            if tmpPoint.within(buffered):

                NI.append(int(row[4]))
                channel_pts.append(Point(tmpPoint))

nearest_geoms = nearest_points(point, MultiPoint(channel_pts))

for i, p in enumerate(channel_pts):
    if p == nearest_geoms[1]:
        print(NI[i])
