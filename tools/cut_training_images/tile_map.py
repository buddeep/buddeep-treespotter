import json, csv
from PIL import Image
from coord_utils import CoordUtils

class TileMapBoundsError(Exception):
    pass

class TileMap:
    map_dir = ''
    origin = [0,0]
    tile_coord_size = [0,0]
    tile_pixel_size = [0,0]
    tile_count = [0,0]
    northeast = [0,0]

    def __init__(self,map_dir):
        self.map_dir = map_dir
        self.load_tiles_info_file()
        pass

    def load_tiles_info_file(self):
        with open('{}/map_info.json'.format(self.map_dir)) as data_file:
            data = json.load(data_file)
            self.origin = data['origin']
            self.tile_coord_size = data['tile_coord_size']
            self.tile_pixel_size = data['tile_pixel_size']
            self.tile_count = data['tile_count']
            emost = self.origin[0]+self.tile_coord_size[0]*self.tile_count[0]
            nmost = self.origin[1]+self.tile_coord_size[1]*self.tile_count[1]
            self.northeast = [emost,nmost]

    def tile_fn_for_tile(self,tile):
        return '{}/tiles/tile-{}_{}.jpg'.format(self.map_dir,tile[0],tile[1])

    def crop_around_tilepixel(self,tilepixel,pixels_wide):
        fn = self.tile_fn_for_tile(tilepixel[0])
        img = Image.open(fn)
        width, height = img.size
        l2rad = pixels_wide/2
        pixel = tilepixel[1]
        lower = [pixel[0]-l2rad, pixel[1]-l2rad]
        upper = [pixel[0]+l2rad, pixel[1]+l2rad]
        # TODO grab pixels from multiple tiles
        if (lower[0] < 0 or lower[1] < 0 or upper[1] > width or upper[1] > height):
            raise TileMapBoundsError("out of bounds")
        # PIL origin at upper left
        # our origin at lower left
        pil_left  = lower[0]
        pil_right = upper[0]
        pil_upper = height-upper[1]
        pil_lower = height-lower[1]
        return img.crop((pil_left, pil_upper, pil_right, pil_lower))

    def crop_around_stateplane(self,stateplane,pixels_wide):
        tilepixel = self.tilepixel_with_stateplane(stateplane)
        return self.crop_around_tilepixel(tilepixel,pixels_wide)

    def crop_around_latlng(self,latlng,pixels_wide):
        tilepixel = self.tilepixel_with_latlng(latlng)
        return self.crop_around_tilepixel(tilepixel,pixels_wide)

    def tilepixel_with_stateplane(self,stateplane):
        eing = stateplane[0]
        ning = stateplane[1]
        if (eing < self.origin[0] or eing > self.northeast[0]):
            raise TileMapBoundsError("out of bounds")
        if (ning < self.origin[1] or ning > self.northeast[1]):
            raise TileMapBoundsError("out of bounds")
        ediff = eing - self.origin[0]
        ndiff = ning - self.origin[1]
        tile = [int(ediff/self.tile_coord_size[0]),int(ndiff/self.tile_coord_size[1])]
        pixel = [int(ediff%self.tile_coord_size[0]),int(ndiff%self.tile_coord_size[1])]
        return [tile,pixel]

    def tilepixel_with_latlng(self,latlng):
        stateplane = CoordUtils.stateplane_for_latlng(latlng);
        return self.tilepixel_with_stateplane(stateplane)

    def pixels_around_latlng(self,latlng,width):
        stateplane = CoordUtils.stateplane_for_latlng(latlng);
        return self.pixels_around_stateplane(stateplane)
