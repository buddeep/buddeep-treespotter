import pyproj

class CoordUtils:
    @staticmethod
    def stateplane_for_latlng(latlng,epsg="2908"):
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

    @staticmethod
    def latlng_for_stateplane(stateplane,epsg="2908"):
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
