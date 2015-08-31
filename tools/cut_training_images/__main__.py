import os, sys, getopt, csv
from tile_map import TileMap, TileMapBoundsError
from tree_list import TreeList
from street_list import StreetList
from coord_utils import CoordUtils

def main(argv):
    usage_string = 'python tools/cut_training_images --trees_dir data/trees --map_dir data/maps/2014 --streets_dir data/streets --slices_dir data/slices/2014_64px --slice_size=64'
    trees_dir = ''
    map_dir = ''
    streets_dir = ''
    slices_dir = ''
    slice_size = 0

    try:
        opts, args = getopt.getopt(argv,"h", ["trees_dir=","map_dir=","slices_dir=","slice_size=","streets_dir="])
    except getopt.GetoptError:
        print usage_string
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print usage_string
        elif opt == '--trees_dir':
            trees_dir = arg
        elif opt == '--map_dir':
            map_dir = arg
        elif opt == '--streets_dir':
            streets_dir = arg
        elif opt == '--slices_dir':
            slices_dir = arg
        elif opt == '--slice_size':
            slice_size = int(arg)

    if not os.path.exists(trees_dir):
        print "trees dir missing"
        sys.exit(2)
    if not os.path.exists(map_dir):
        print "map dir missing"
        sys.exit(2)
    if not os.path.exists(streets_dir):
        print "streets dir missing"
        sys.exit(2)
    if len(slices_dir) == 0:
        print "slices dir not specified"
        sys.exit(2)

    if not os.path.exists(slices_dir):
        os.makedirs(slices_dir)
    slices_0_dir = '{}/0'.format(slices_dir)
    slices_1_dir = '{}/1'.format(slices_dir)
    if not os.path.exists(slices_0_dir):
        os.makedirs(slices_0_dir)
    if not os.path.exists(slices_1_dir):
        os.makedirs(slices_1_dir)

    tile_map = TileMap(map_dir)
    trees = list(TreeList(trees_dir))
    street_list = StreetList(streets_dir)
    for street in street_list:
        i = 0
        for waypoint_latlng in street['waypoints']:
            waypoint = CoordUtils.stateplane_for_latlng(waypoint_latlng)
            i = i + 1
            l1_radius = slice_size/2
            trees_seen = []
            # TODO faster please
            for tree in trees:
                if (
                    tree['stateplane'][0] > waypoint[0]-l1_radius and
                    tree['stateplane'][0] < waypoint[0]+l1_radius and
                    tree['stateplane'][1] > waypoint[1]-l1_radius and
                    tree['stateplane'][1] < waypoint[1]+l1_radius):
                    trees_seen.append(tree)
            label = (0 if (len(trees_seen) == 0) else 1)
            try:
                region = tile_map.crop_around_stateplane(waypoint,slice_size)
                slice_fn = '{}/{}/segment-{}-{}.jpg'.format(slices_dir,label,street['kml_id'],i)
                region.save(slice_fn)
                print slice_fn
            except TileMapBoundsError:
                print "WARNING: waypoint out of bounds: {}".format(waypoint)
                pass

if __name__ == "__main__":
    main(sys.argv[1:])
