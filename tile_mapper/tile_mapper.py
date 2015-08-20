import csv
import pyproj

class TileMapper:
    """Tile Mapper loads a CSV file containing various geographic tiles and """
    tile_list = []
    PIXELS = 256
    
    def __init__(self,pixels=256):
        """pixels specifies the tile resolution
        Program assumes that we're dealing with square tiles"""
        self.PIXELS = 256
        pass
        
    def load_csv (self,csv_path):
        """Function takes one argument which is the full csv file path
        Expected column order: tile_id, x, y, north(ing), east(ing), south, west, tile_url
        """
        with open(csv_path, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            count = 0
            try:
                for row in reader:
                    # transfer rows to list except first row i.e. column labels
                    if count > 0:
                            a = {"id":row[0],"x":row[1],"y":row[2],"north":float(row[3]),"east":float(row[4]),"south":float(row[5]),"west":float(row[6]),"tile_url":row[7]}
                            self.tile_list.append(a)
                    count = count + 1
            except:
                tile_list = []
                print "Could not load CSV"
                
    def stateplane_for_latlong(self,latlong,epsg="2908"):
        """
        Function accepts a latlong co-ordinate and returns a stateplane co-ordinate
        -- latlong is a set in the form of (latitude,longitude)
        -- stateplane is a set in the form of (easting,northing)
        -- EPSG is the stateplane identifier which defaults to the identifier for Manhattan:
                EPSG:2908: NAD83(HARN) / New York Long Island (ftUS)
        """
        lat,lng = latlong[0], latlong[1]
        sp_epsg = "EPSG:"+epsg 
        # Preserve units keeps projection in ftUS
        stateplane_projection = pyproj.Proj(init=sp_epsg, preserve_units=True) 
        wgs84_projection = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
        stateplane = pyproj.transform(wgs84_projection,stateplane_projection,lng,lat)
        return stateplane
        
    
    def latlong_for_stateplane(self,stateplane,epsg="2908"):
        """
        Function accepts a stateplane co-ordinate and returns a latlong coordinate set
        -- latlong is a set in the form of (latitude,longitude)
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
        # flip longLat to latlong
        return (longlat[1],longlat[0])
        
    def tile_for_latlong(self,latlong):
        """Returns the tile ID for the tile which contains the specified latlong coordinate
           CSV file should be loaded before use
           """
        if len(self.tile_list) > 0:
            stateplane = self.stateplane_for_latlong(latlong)
            tile = self.tile_for_stateplane(stateplane)       
            return tile
        else:
            print "Load CSV first"
            return None
        
    def tile_for_stateplane(self,stateplane):
        """Returns the tile object that contains the specified latlong coordinate
           Uses shameful O(N^2) brute force search. #TODO: Improve
           CSV file should be loaded before use
           """
        if len(self.tile_list) > 0:
            easting, northing = stateplane[0], stateplane[1]
            for tile in self.tile_list:
                if tile['west'] <= easting <= tile['east']:
                    if tile['south'] <= northing <= tile['north']:
                        return tile
            print "Tile Not found"
            return None
        else:
            print "Load CSV first"
            return None
    
    def pixel_for_stateplane(self,stateplane):
        """Finds the pixel in the image corresponding to the stateplane coordinate
        pixel_x = distance from cartesian origin along x axis
        pixel_y = distance from cartesian origin along y axis
        """
        pixels = self.PIXELS
        tile = self.tile_for_stateplane(stateplane)
        if tile == None:
            return None
        else:
            easting, northing = stateplane[0], stateplane[1]
            x_range = tile['east'] - tile['west']
            x_offset = easting - tile['west']
            pixel_x = pixels/x_range*x_offset
            y_range = tile['north'] - tile['south']
            y_offset = northing - tile['south']
            pixel_y = pixels/y_range*y_offset
            return {"tile_id":tile['id'],"pixel_x":int(pixel_x),"pixel_y":int(pixel_y)}
            
    def pixel_for_latlong(self,latlong):
        """Finds the pixel in the image corresponding to the latlong coordinate
        pixel_x = distance from cartesian origin along x axis
        pixel_y = distance from cartesian origin along y axis
        """
        stateplane = self.stateplane_for_latlong(latlong)
        return self.pixel_for_stateplane(stateplane)
