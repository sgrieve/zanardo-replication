from shapely.geometry import mapping, Point
import fiona
from fiona.crs import from_epsg
from glob import glob


points = fiona.open('pts_wgs84.shp')

for i, p in enumerate(points[0]['geometry']['coordinates']):
    point = Point(p)

    # 0.75 is approximately 82km in the USA, which is the approx
    # square root of the largest basin area (7200 km^2)
    buffered = point.buffer(0.75)


    schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int'},
    }

    with fiona.open('raster_clipper/buffer_{}.shp'.format(i), 'w',
                    crs=from_epsg(4326), driver='ESRI Shapefile',
                    schema=schema) as c:
        c.write({
            'geometry': mapping(buffered),
            'properties': {'id': 1},
        })
