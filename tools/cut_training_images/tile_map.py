import json, csv, pyproj
from PIL import Image

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
            raise Exception("out of bounds")
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
            raise Exception("out of bounds")
        if (ning < self.origin[1] or ning > self.northeast[1]):
            raise Exception("out of bounds")
        ediff = eing - self.origin[0]
        ndiff = ning - self.origin[1]
        tile = [ediff/self.tile_coord_size[0],ndiff/self.tile_coord_size[1]]
        pixel = [ediff%self.tile_coord_size[0],ndiff%self.tile_coord_size[1]]
        return [tile,pixel]

    def tilepixel_with_latlng(self,latlng):
        stateplane = self.stateplan_for_latlng(latlng);
        return self.tile_with_stateplan(stateplane)

    def pixels_around_latlng(self,latlng,width):
        stateplane = self.stateplan_for_latlng(latlng);
        return self.pixels_around_stateplan(stateplane)

    def stateplane_for_latlng(self,latlng,epsg="2908"):
        """
        Function accepts a latlng co-ordinate and returns a stateplane co-ordinate
        -- latlng is a set in the form of (latitude,longitude)
        -- stateplane is a set in the form of (easting,northing)
        -- EPSG is the stateplane identifier which defaults to the identifier for Manhattan:
                EPSG:2908: NAD83(HARN) / New York Long Island (ftUS)
        """
        lat,lng = latlng[0], latlng[1]
        sp_epsg = "EPSG:"+epsg 
        # Preserve units keeps projection in ftUS
        stateplane_projection = pyproj.Proj(init=sp_epsg, preserve_units=True) 
        wgs84_projection = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
        stateplane = pyproj.transform(wgs84_projection,stateplane_projection,lng,lat)
        return stateplane
        
    
    def latlng_for_stateplane(self,stateplane,epsg="2908"):
        """
        Function accepts a stateplane co-ordinate and returns a latlng coordinate set
        -- latlng is a set in the form of (latitude,longitude)
        -- stateplane is a set in the form of (easting,northing)
        -- EPSG is the stateplane identifier which defaults to the identifier for Manhattan:
                EPSG:2908: NAD83(HARN) / New York Long Island (ftUS)
        """
        easting, northing = stateplane[0], stateplane[1]
        sp_epsg = "EPSG:"+epsg 
        # Preserve units keeps projection in ftUS
        stateplane_projection = pyproj.Proj(init=sp_epsg, preserve_units=True)
        wgs84_projection = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
        longlat = pyproj.transform(stateplane_projection,wgs84_projection,easting,northing)
        # flip longLat to latlng
        return (longlat[1],longlat[0])
