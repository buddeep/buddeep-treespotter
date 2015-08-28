import os, sys, getopt
from tile_map import TileMap, TileMapBoundsError
from tree_list import TreeList

def main(argv):
    usage_string = 'python tools/cut_training_images --trees_dir data/trees --map_dir data/maps/2014 --slices_dir data/slices/2014_64px --slice_size=64'
    trees_dir = ''
    map_dir = ''
    slices_dir = ''
    slice_size = 0

    try:
        opts, args = getopt.getopt(argv,"h", ["trees_dir=","map_dir=","slices_dir=","slice_size="])
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
    tree_list = TreeList(trees_dir)
    for tree in tree_list:
        try:
            region = tile_map.crop_around_latlng(tree['latlng'],slice_size)
            slice_fn = '{}/{}/{}.jpg'.format(slices_dir,'1',tree['id'])
            region.save(slice_fn)
            print slice_fn
        except TileMapBoundsError:
            print "WARNING: tree out of bounds: {}".format(tree)
            pass

if __name__ == "__main__":
    main(sys.argv[1:])
