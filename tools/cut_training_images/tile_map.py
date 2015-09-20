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

    def concat_tiles(self, img, tilepixel, move_x, move_y, paste_x, paste_y, lim1, corner=False, lim2=None):
        """
        This is a helper function for crop_around_tilepixel to avoid a bunch of if/else statements
        --- It creates the 8 tiles that neighbour original tile in new 3000x3000 image
        --- Controls for edge case of tile being on border of full map
                --- pastes blank image of same size where a neighbouring tile doesnt exists
        """
        if not corner:
            if tilepixel[0][lim1[0]] == lim1[1]:
                tile = Image.new("RGB", (1000, 1000))
            else:
                fn = self.tile_fn_for_tile([tilepixel[0][0] + move_x, tilepixel[0][1] + move_y])
                tile = Image.open(fn)
        else:
            if tilepixel[0][lim1[0]] == lim1[1] or tilepixel[0][lim2[0]] == lim2[1]:
                tile = Image.new("RGB", (1000, 1000))
            else:
                fn = self.tile_fn_for_tile([tilepixel[0][0] + move_x, tilepixel[0][1] + move_y])
                tile = Image.open(fn)
        img.paste(tile, (paste_x, paste_y))

    def crop_around_tilepixel(self,tilepixel,pixels_wide):
        fn = self.tile_fn_for_tile(tilepixel[0])
        img = Image.open(fn)
        width, height = img.size
        l2rad = pixels_wide/2
        pixel = tilepixel[1]
        lower = [pixel[0]-l2rad, pixel[1]-l2rad]
        upper = [pixel[0]+l2rad, pixel[1]+l2rad]
        # TODO grab pixels from multiple tiles
        if (lower[0] < 0 or lower[1] < 0 or upper[0] > width or upper[1] > height):
            # add 8 neighbouring tiles to make bigger square (3000x3000)
            try:
                # create new blank 3000x3000 image
                new_img = Image.new("RGB", (3000, 3000))
                # list of params to pass in helper function, 0th element is tile position
                to_add = [['top_left', -1, 1, 0, 0, [0,0], True, [1,self.tile_count[1]-1]],
                          ['mid_left', -1, 0, 0, 1000, [0,0], False, None],
                          ['bottom_left', -1, -1, 0, 2000, [0,0], True, [1, 0]],
                          ['top_middle', 0, 1, 1000, 0, [1,self.tile_count[1]-1], False, None],
                          ['bottom_middle', 0, -1, 1000, 2000, [1,0], False, None],
                          ['top_right', 1, 1, 2000, 0, [0,self.tile_count[0]-1], True, [1,self.tile_count[1]-1]],
                          ['middle_right', 1, 0, 2000, 1000, [0,self.tile_count[0]-1], False, None],
                          ['bottom_right', 1, -1, 2000, 2000, [0,self.tile_count[0]-1], True, [1,0]]]
                for block in to_add:
                    self.concat_tiles(new_img, tilepixel, block[1], block[2], block[3],
                                        block[4], block[5], block[6], block[7])
                # paste original image in center
                new_img.paste(img, (1000, 1000))
                width, height = new_img.size
                lower = [lower[0]+1000, lower[1]+1000]
                upper = [upper[0]+1000, upper[1]+1000]
                img = new_img
            except:
                # try/except just for precaution, but error never raised here
                # always comes from tilepixel_with_stateplane()
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
