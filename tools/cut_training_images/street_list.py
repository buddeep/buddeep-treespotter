import csv
from coord_utils import CoordUtils

class StreetList:
    streets_dir = ''
    csvfile = ''
    csvreader = ''

    def __init__(self,streets_dir):
        self.streets_dir = streets_dir
        self.csvfile = open('{}/street_segments.csv'.format(streets_dir))
        self.csvreader = csv.DictReader(self.csvfile)
        pass

    def __iter__(self):
        return self

    def next(self):
        row = self.csvreader.next()
        bounds = [float(x) for x in row['bounds'].replace('(','').replace(')','').replace(' ','').split(',')]
        row['bounds'] = bounds
        row['waypoints'] = ''
        if len(bounds) == 4:
            row['waypoints'] = CoordUtils.waypoints_for_linestring(
                    [(bounds[1],bounds[0]),(bounds[3],bounds[2])],
                    32)
        return row
